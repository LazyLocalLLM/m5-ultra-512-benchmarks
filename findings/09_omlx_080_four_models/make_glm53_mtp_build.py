#!/usr/bin/env python3
"""Make a GLM-5.3 4-bit build folder that carries an MTP draft head.

Python 3.9, standard library only. It runs no model code and imports no
third-party package.

What it does:
  1. Hard-links every weight shard of the trunk build into OUT. No bytes are
     copied, so OUT costs no disk beyond the head.
  2. Copies the trunk's small text files, and sets num_nextn_predict_layers
     to 1 in config.json.
  3. Writes the standalone MTP head into one new file with the tensor names
     and layout oMLX 0.7.3 reads for a pre-remapped head. Tensor bytes are
     copied unchanged and checked by SHA-256.
  4. Adds the head's tensors to model.safetensors.index.json.

Name map, from omlx/patches/mlx_lm_mtp/glm_moe_dsa_model.py in oMLX 0.7.3:
  mtp.eh_proj.*               -> mtp.0.eh_proj.*
  mtp.enorm.weight            -> mtp.0.enorm.weight
  mtp.hnorm.weight            -> mtp.0.hnorm.weight
  mtp.shared_head_norm.weight -> mtp.0.norm.weight
  mtp.<anything else>         -> mtp.0.block.<anything else>

One layout change, from omlx/patches/glm_moe_dsa/deepseek_v32.py. oMLX keeps
the routed experts' gate and up projections as one tensor, gate_up_proj,
which is concatenate([gate_proj, up_proj], axis=1). Its loader does that
join for the trunk and not for a pre-remapped head. So this script does the
same join for the head's weight, scales and biases. Each expert's rows are
copied byte for byte, gate rows first, then up rows.

Version 1 of this script, 05:08 SGT on 15 Nov 2026, only renamed. oMLX 0.7.3
refused that folder with "Received 6 parameters not in model", the six
gate_proj and up_proj tensors of mtp.0.block.mlp.switch_mlp, run d4be16163f42.

Usage:
  make_glm53_mtp_build.py TRUNK_DIR HEAD_DIR OUT_DIR
"""
import hashlib
import json
import os
import shutil
import struct
import sys
from pathlib import Path

SPECIAL = {
    'enorm.weight': 'enorm.weight',
    'hnorm.weight': 'hnorm.weight',
    'shared_head_norm.weight': 'norm.weight',
}
SWITCH = 'mtp.mlp.switch_mlp.'
BLOCK = 16 * 1024 * 1024


def new_name(key):
    if not key.startswith('mtp.'):
        raise SystemExit('unexpected tensor name in the head: ' + key)
    rest = key[len('mtp.'):]
    if rest.startswith('eh_proj.'):
        return 'mtp.0.' + rest
    if rest in SPECIAL:
        return 'mtp.0.' + SPECIAL[rest]
    return 'mtp.0.block.' + rest


def read_headers(head):
    """Return {tensor name: (path, absolute start, absolute end, dtype, shape)}."""
    found = {}
    for shard in sorted(head.glob('model-*.safetensors')):
        with open(shard, 'rb') as handle:
            size = struct.unpack('<Q', handle.read(8))[0]
            header = json.loads(handle.read(size).decode('utf-8'))
        base = 8 + size
        for key, value in header.items():
            if key == '__metadata__':
                continue
            start, end = value['data_offsets']
            found[key] = (shard, base + start, base + end, value['dtype'], value['shape'])
    return found


def copy_range(path, start, end, out, digest):
    with open(path, 'rb') as handle:
        handle.seek(start)
        left = end - start
        while left:
            block = handle.read(min(BLOCK, left))
            if not block:
                raise SystemExit('short read in ' + str(path))
            out.write(block)
            digest.update(block)
            left -= len(block)


def range_hash(path, start, end):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        handle.seek(start)
        left = end - start
        while left:
            block = handle.read(min(BLOCK, left))
            digest.update(block)
            left -= len(block)
    return digest.hexdigest()


def write_head(head, target):
    source = read_headers(head)
    plan = []  # (new name, dtype, shape, [(path, start, end), ...])
    for key in sorted(source):
        path, start, end, dtype, shape = source[key]
        if key.startswith(SWITCH + 'up_proj.'):
            continue
        if key.startswith(SWITCH + 'gate_proj.'):
            kind = key.rsplit('.', 1)[1]
            up_path, up_start, up_end, up_dtype, up_shape = source[SWITCH + 'up_proj.' + kind]
            if up_dtype != dtype or up_shape != shape:
                raise SystemExit('gate and up differ for ' + kind)
            experts = shape[0]
            gate_step = (end - start) // experts
            up_step = (up_end - up_start) // experts
            pieces = []
            for expert in range(experts):
                pieces.append((path, start + expert * gate_step, start + (expert + 1) * gate_step))
                pieces.append((up_path, up_start + expert * up_step, up_start + (expert + 1) * up_step))
            fused = [shape[0], shape[1] * 2] + list(shape[2:])
            plan.append(('mtp.0.block.mlp.switch_mlp.gate_up_proj.' + kind, dtype, fused, pieces))
        else:
            plan.append((new_name(key), dtype, shape, [(path, start, end)]))

    header = {'__metadata__': {'format': 'mlx'}}
    offset = 0
    for name, dtype, shape, pieces in plan:
        length = sum(end - start for _, start, end in pieces)
        header[name] = {'dtype': dtype, 'shape': shape, 'data_offsets': [offset, offset + length]}
        offset += length
    raw = json.dumps(header, separators=(',', ':')).encode('utf-8')
    raw += b' ' * ((8 - len(raw) % 8) % 8)

    written = {}
    with open(target, 'wb') as out:
        out.write(struct.pack('<Q', len(raw)))
        out.write(raw)
        for name, dtype, shape, pieces in plan:
            digest = hashlib.sha256()
            for path, start, end in pieces:
                copy_range(path, start, end, out, digest)
            written[name] = digest.hexdigest()

    # Read the new file back and compare every tensor with its source bytes.
    base = 8 + len(raw)
    for name, dtype, shape, pieces in plan:
        start, end = header[name]['data_offsets']
        if range_hash(target, base + start, base + end) != written[name]:
            raise SystemExit('read-back differs for ' + name)
        if len(pieces) == 1:
            path, s, e = pieces[0]
            if range_hash(path, s, e) != written[name]:
                raise SystemExit('source differs for ' + name)
    return [name for name, _, _, _ in plan]


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    trunk, head, out = (Path(p).expanduser() for p in sys.argv[1:])
    if out.exists():
        raise SystemExit(str(out) + ' already exists. Nothing done.')
    out.mkdir(parents=True)

    shards = sorted(trunk.glob('model-*.safetensors'))
    for shard in shards:
        os.link(str(shard), str(out / shard.name))
    for name in ('chat_template.jinja', 'generation_config.json', 'tokenizer.json', 'tokenizer_config.json'):
        shutil.copy2(str(trunk / name), str(out / name))

    config = json.loads((trunk / 'config.json').read_text())
    if config.get('num_nextn_predict_layers') not in (0, None):
        raise SystemExit('the trunk already names an MTP layer')
    config['num_nextn_predict_layers'] = 1
    (out / 'config.json').write_text(json.dumps(config, indent=4) + '\n')

    name = 'model-mtp-00001-of-00001.safetensors'
    keys = write_head(head, out / name)
    index = json.loads((trunk / 'model.safetensors.index.json').read_text())
    for key in keys:
        index['weight_map'][key] = name
    (out / 'model.safetensors.index.json').write_text(json.dumps(index, indent=4) + '\n')

    print('trunk shards linked:', len(shards))
    print('head file', name, 'with', len(keys), 'tensors, every tensor read back and matched to its source bytes')
    print('gate_proj and up_proj of the routed experts joined into gate_up_proj, 3 tensors')
    print('num_nextn_predict_layers set to 1 in', out / 'config.json')


if __name__ == '__main__':
    main()
