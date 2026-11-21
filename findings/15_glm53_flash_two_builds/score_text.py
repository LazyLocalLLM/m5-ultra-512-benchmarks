"""Score how well a build predicts fixed text, with no server, through oMLX's own model code.

    <oMLX venv>/bin/python -I -B score_text.py score TEXTS.json MODEL_DIR OUT.json
    python3 -B score_text.py compare A.json B.json

The script behind the text-prediction figures of finding 15. It loads a build with the model code oMLX 0.8.1 ships
(omlx.utils.model_loading.load_text_model) and scores each text in one forward pass, the way mlx_lm/perplexity.py
does it. The figure is the mean negative log-likelihood per token, in nats, of raw text with no chat template. Lower
means the build gives the real next token more probability. It is text prediction, not task quality.
  score    TEXTS.json is a list of objects with kind, seed, text and text_sha256. The first text is scored twice
           and the largest gap between the two passes is printed. Every token's loss goes to OUT.json.
  compare  paired differences text by text, B minus A.
My texts are pieces of the bench's reading text, open-source code and prose, about 5,250 characters each. I do not
publish them here. scores.csv gives each text's SHA-256, token count and both scores. Python 3.9 syntax.
"""
import hashlib
import json
import math
import sys


def score(texts_path, model_dir, out):
    import mlx.core as mx
    import mlx.nn as nn
    from omlx.utils.model_loading import load_text_model
    rows = json.load(open(texts_path))
    model, tokenizer = load_text_model(model_dir)
    model.eval()
    print('loaded', model_dir.rstrip('/').split('/')[-1], '| model class', type(model).__module__, type(model).__name__)

    def one(ids):
        logits = model(mx.array([ids[:-1]])).astype(mx.float32)
        targets = mx.array([ids[1:]])
        losses = nn.losses.cross_entropy(logits, targets, reduction='none')
        hits = (mx.argmax(logits, axis=-1) == targets)
        mx.eval(losses, hits)
        return [float(v) for v in losses.flatten().tolist()], int(hits.sum().item())

    done, total, count, hits_all = [], 0.0, 0, 0
    for k, row in enumerate(rows):
        ids = [int(t) for t in tokenizer.encode(row['text'])]
        losses, hits = one(ids)
        if k == 0:
            again, _ = one(ids)
            worst = max(abs(a - b) for a, b in zip(losses, again))
            print('repeat check, first text scored twice: largest per-token gap {:.6f} nats'.format(worst))
        if any(math.isnan(v) or math.isinf(v) for v in losses):
            print('NLL OFFLINE FAILED, non-finite loss on {} {}'.format(row['kind'], row['seed']))
            return 2
        nll = sum(losses) / len(losses)
        done.append({'kind': row['kind'], 'seed': row['seed'], 'text_sha256': row['text_sha256'],
                     'ids_sha256': hashlib.sha256(json.dumps(ids).encode()).hexdigest()[:16],
                     'tokens': len(ids), 'scored_tokens': len(losses), 'nll': nll, 'top1': hits, 'losses': losses})
        total += sum(losses)
        count += len(losses)
        hits_all += hits
        print('nll {} {} | tokens {} | nll {:.4f} | top-1 {} of {}'.format(row['kind'], row['seed'], len(losses), nll, hits, len(losses)))
    by_kind = {}
    for kind in sorted({r['kind'] for r in done}):
        picked = [r for r in done if r['kind'] == kind]
        tokens = sum(r['scored_tokens'] for r in picked)
        by_kind[kind] = {'tokens': tokens, 'nll': sum(sum(r['losses']) for r in picked) / tokens,
                         'top1': sum(r['top1'] for r in picked)}
    json.dump({'model_dir': model_dir.rstrip('/').split('/')[-1], 'texts': done, 'by_kind': by_kind,
               'overall_nll': total / count, 'scored_tokens': count, 'top1': hits_all}, open(out, 'w'))
    print('NLL OVERALL {:.4f} over {} tokens | {} | top-1 {} of {}'.format(
        total / count, count, ' | '.join('{} {:.4f}'.format(k, v['nll']) for k, v in sorted(by_kind.items())), hits_all, count))
    return 0


def compare(path_a, path_b):
    a, b = json.load(open(path_a)), json.load(open(path_b))
    print('A', a['model_dir'], '| B', b['model_dir'])
    rows_a = {(r['kind'], r['seed']): r for r in a['texts']}
    diffs, same_ids = [], 0
    for row in b['texts']:
        other = rows_a[(row['kind'], row['seed'])]
        same_ids += other['ids_sha256'] == row['ids_sha256']
        diffs.append(row['nll'] - other['nll'])
        print('{} {} | A {:.4f} | B {:.4f} | B minus A {:+.4f}'.format(row['kind'], row['seed'], other['nll'], row['nll'], diffs[-1]))
    n = len(diffs)
    mean = sum(diffs) / n
    spread = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1))
    print('texts with the same token ids in both: {} of {}'.format(same_ids, n))
    print('B lower on {} of {} texts | mean of B minus A {:+.4f} nats | spread across texts (sample sd) {:.4f} | smallest {:+.4f} largest {:+.4f}'.format(
        sum(1 for d in diffs if d < 0), n, mean, spread, min(diffs), max(diffs)))
    print('overall A {:.4f} B {:.4f} | top-1 A {} B {} of {}'.format(a['overall_nll'], b['overall_nll'], a['top1'], b['top1'], a['scored_tokens']))
    return 0


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'score' and len(sys.argv) == 5:
        sys.exit(score(*sys.argv[2:5]))
    if mode == 'compare' and len(sys.argv) == 4:
        sys.exit(compare(sys.argv[2], sys.argv[3]))
    print(__doc__)
    sys.exit(1)
