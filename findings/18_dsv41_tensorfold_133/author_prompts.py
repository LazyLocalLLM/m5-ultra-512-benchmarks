"""Send a list of short prompts the way TensorFold's own bench tool sends them, and time the decode.

    python3 -I -B m5_bench/recipes/author_prompts.py PORT PROMPTS.json OUT.json [REPS] [sampled]

Why. The author's pull requests for DeepSeek-V4.1 on Metal quote tok/s on "16 prompts" and on "prose", measured with
tools/bench_prompts.json of the TensorFold repository. To test that claim on this Mac the prompts have to be his, not
the bench's own reading text. This script reads that file as data and runs none of the repository's code. The request
body follows tools/bench_concurrent.py as read on 21 Nov 2026. The prompt file is the same at main commit 1093b795. max_tokens 512, temperature 0,
stream, usage in the stream, ignore_eos true. A "chat" item goes to /v1/chat/completions with thinking switched
off. A "completion" item goes to /v1/completions as a raw prompt. With "sampled" the temperature is 1.0 and the
seed 1234, as pull request 3288 states.
Decode tok/s is (tokens - 1) / (last piece - first piece), the tool's own rule. Tokens come from the reply's usage.
A reply with fewer than 4 text pieces is not timed. Nothing is written to the bench database. Python 3.9, standard
library only. The API key, if the server needs one, is read from the M5_API_KEY variable.
"""
import hashlib
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request

TOKENS = 512
MIN_PIECES = 4


def one(port, model, item, sampled):
    body = {'model': model, 'max_tokens': TOKENS, 'temperature': 1.0 if sampled else 0, 'stream': True,
            'stream_options': {'include_usage': True}, 'ignore_eos': True}
    if sampled:
        body['seed'] = 1234
    if item.get('kind') == 'chat':
        url = 'http://127.0.0.1:{}/v1/chat/completions'.format(port)
        body['messages'] = [{'role': 'user', 'content': item['prompt']}]
        body['chat_template_kwargs'] = {'enable_thinking': False}
    else:
        url = 'http://127.0.0.1:{}/v1/completions'.format(port)
        body['prompt'] = item['prompt']
    headers = {'Content-Type': 'application/json'}
    key = os.environ.get('M5_API_KEY')
    if key:
        headers['Authorization'] = 'Bearer ' + key
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    sent = time.perf_counter()
    first = last = None
    pieces, text, think, usage = 0, [], 0, {}
    try:
        with urllib.request.urlopen(request, timeout=900) as reply:
            for raw in reply:
                line = raw.decode('utf-8', 'replace').strip()
                if not line.startswith('data:'):
                    continue
                data = line[5:].strip()
                if data == '[DONE]':
                    break
                try:
                    event = json.loads(data)
                except ValueError:
                    continue
                if event.get('usage'):
                    usage = event['usage']
                for choice in event.get('choices') or []:
                    delta = choice.get('delta') or {}
                    piece = delta.get('content') or choice.get('text') or ''
                    reasoning = delta.get('reasoning_content') or delta.get('reasoning') or ''
                    if piece or reasoning:
                        now = time.perf_counter()
                        first = now if first is None else first
                        last = now
                        pieces += 1
                        text.append(piece)
                        think += len(reasoning)
    except urllib.error.HTTPError as error:
        return {'name': item.get('name'), 'kind': item.get('kind'), 'error': 'HTTP {} {}'.format(error.code, error.read()[:200].decode('utf-8', 'replace'))}
    except Exception as error:  # a dropped stream is a result to report, not a crash
        return {'name': item.get('name'), 'kind': item.get('kind'), 'error': type(error).__name__}
    joined = ''.join(text)
    tokens = usage.get('completion_tokens')
    out = {'name': item.get('name'), 'kind': item.get('kind'), 'tokens': tokens, 'prompt_tokens': usage.get('prompt_tokens'),
           'pieces': pieces, 'first_s': None if first is None else first - sent, 'reasoning_chars': think,
           'text_sha256': hashlib.sha256(joined.encode()).hexdigest()[:16], 'preview': joined[:120]}
    if tokens and pieces >= MIN_PIECES and last > first:
        out['decode_tps'] = (tokens - 1) / (last - first)
    return out


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 1
    port, prompts_path, out_path = int(argv[1]), argv[2], argv[3]
    reps = int(argv[4]) if len(argv) > 4 and argv[4].isdigit() else 2
    sampled = 'sampled' in argv[4:]
    items = json.load(open(prompts_path, encoding='utf-8'))
    if not isinstance(items, list) or not all(isinstance(i, dict) and isinstance(i.get('prompt'), str) for i in items):
        print('error: the prompts file is not a list of items with a prompt')
        return 1
    headers = {}
    if os.environ.get('M5_API_KEY'):
        headers['Authorization'] = 'Bearer ' + os.environ['M5_API_KEY']
    with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:{}/v1/models'.format(port), headers=headers), timeout=30) as reply:
        listed = [entry['id'] for entry in json.load(reply)['data']]
    if len(listed) != 1:
        print('error: the server lists {} models'.format(len(listed)))
        return 1
    one(port, listed[0], {'kind': 'chat', 'name': 'warm-up', 'prompt': 'Say hello.'}, False)
    rows = []
    for rep in range(reps):
        for item in items:
            row = one(port, listed[0], item, sampled)
            row['rep'] = rep
            rows.append(row)
    per = {}
    for row in rows:
        if 'decode_tps' in row:
            per.setdefault(row['name'], []).append(row['decode_tps'])
    medians = {name: statistics.median(values) for name, values in per.items()}
    same = sum(1 for item in items if len({r['text_sha256'] for r in rows if r['name'] == item.get('name') and 'text_sha256' in r}) == 1)
    summary = {'prompts': len(items), 'reps': reps, 'sampled': sampled, 'timed_prompts': len(medians),
               'errors': sum(1 for r in rows if 'error' in r), 'untimed': sum(1 for r in rows if 'error' not in r and 'decode_tps' not in r),
               'short_replies': sum(1 for r in rows if r.get('tokens') not in (None, TOKENS)),
               'with_reasoning': sum(1 for r in rows if r.get('reasoning_chars')),
               'same_text_across_reps': same}
    if medians:
        summary['mean_of_prompt_medians'] = statistics.mean(medians.values())
        summary['median_of_prompt_medians'] = statistics.median(medians.values())
        summary['lowest'] = min(medians.values())
        summary['highest'] = max(medians.values())
    json.dump({'model': listed[0], 'prompts_sha256': hashlib.sha256(open(prompts_path, 'rb').read()).hexdigest()[:16],
               'summary': summary, 'per_prompt_median': medians, 'rows': rows}, open(out_path, 'w'), indent=1)
    print('author prompts: ' + json.dumps({k: (round(v, 1) if isinstance(v, float) else v) for k, v in summary.items()}))
    for name in sorted(medians, key=medians.get):
        kind = [i.get('kind') for i in items if i.get('name') == name][0]
        print('  {:>6.1f} tok/s  {}  {}'.format(medians[name], kind, name))
    for row in rows:
        if 'error' in row:
            print('  ERROR {} {}'.format(row['name'], row['error'][:160]))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
