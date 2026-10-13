"""Validate the exact small decay sample used to check this installation."""
import gzip
import json
import math
from pathlib import Path
import re
import sys

source, output = map(Path, sys.argv[1:])
with gzip.open(source, 'rt', encoding='utf-8') as f:
    text = f.read()
init = re.search(r'<init>\s*(.*?)</init>', text, re.S)
if not init:
    raise ValueError('Missing LHE init block')
lines = init.group(1).strip().splitlines()
if int(lines[0].split()[8]) != -4:
    raise ValueError('This validator expects the MG decay sample with IDWTUP=-4')
rate, integration_error = map(float, lines[1].split()[:2])
blocks = re.findall(r'<event>\s*(.*?)</event>', text, re.S)
if len(blocks) != 2000:
    raise ValueError(f'Expected 2000 complete events, got {len(blocks)}')
direct, linear, max_residual = [], [], 0.0
for block in blocks:
    lines = block.strip().splitlines()
    head = lines[0].split()
    n = int(head[0])
    direct.append(float(head[2]))
    incoming, outgoing, ids = [], [], []
    for line in lines[1:n + 1]:
        fields = line.split()
        pid, status = int(fields[0]), int(fields[1])
        p = list(map(float, fields[6:10]))
        if not all(map(math.isfinite, p)):
            raise ValueError('Nonfinite four-momentum')
        if status == -1:
            incoming.append(p)
        if status == 1:
            outgoing.append(p)
            ids.append(pid)
    if sorted(ids) != sorted([11, -12, -13, 14]):
        raise ValueError(f'Unexpected final state: {ids}')
    residual = max(abs(sum(p[i] for p in incoming) - sum(p[i] for p in outgoing)) for i in range(4))
    max_residual = max(max_residual, residual)
    values = re.findall(r'<wgt\s+id=[\'\"]cHl3[\'\"]\s*>\s*([^<]+)</wgt>', block)
    if len(values) != 1:
        raise ValueError('Expected one cHl3 weight in every event')
    linear.append(float(values[0]))
if not all(math.isfinite(x) for x in direct + linear):
    raise ValueError('Nonfinite event weights')
if max_residual > 1e-6:
    raise ValueError('Four-momentum conservation failed')
mean_direct = sum(direct) / len(direct)
mean_linear = sum(linear) / len(linear)
if not math.isclose(mean_direct, rate, rel_tol=1e-5, abs_tol=1e-12):
    raise ValueError('LHE weight normalization does not match the init rate')
if not rate > 0 or not mean_linear < 0:
    raise ValueError('Unexpected SM / cHl3 linear rate signs for this tutorial setup')
report = {
    'status': 'passed', 'events': len(blocks), 'source': str(source.resolve()),
    'SM_width_GeV': rate, 'SM_integration_error_GeV': integration_error,
    'cHl3_linear_mean_weight_GeV': mean_linear,
    'max_four_momentum_residual_GeV': max_residual,
    'checks': ['2000 complete events', 'expected four-lepton final state',
               'finite momenta and SM/reweight event weights', 'four-momentum conservation',
               'SM LHE normalization agrees with init', 'cHl3 linear reweight exists in every event'],
    'scope': 'Installation smoke test; not a direct-vs-reweighted closure or a full physics validation',
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
