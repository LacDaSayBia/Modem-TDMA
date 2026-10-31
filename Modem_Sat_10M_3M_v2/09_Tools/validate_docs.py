#!/usr/bin/env python3
"""Validate this documentation package; does not verify modem hardware performance."""
from pathlib import Path
import argparse
import json
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]

def crc32c(data):
    crc = 0xffffffff
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0x82f63b78 if crc & 1 else 0)
    return crc ^ 0xffffffff

def validate():
    errors = []
    modules = sorted((ROOT / '03_Mo_dun').glob('M*.md'))
    if len(modules) != 20:
        errors.append('Exactly 20 module files required')
    for i, path in enumerate(modules, 1):
        txt = path.read_text(encoding='utf-8')
        if not path.name.startswith(f'M{i:02}_'):
            errors.append('Module numbering: ' + path.name)
        for n in range(1, 12):
            if not re.search(r'^## ' + str(n) + r'\.', txt, re.M):
                errors.append(f'{path.name}: missing section {n}')
        if len(txt.split()) < 500:
            errors.append(path.name + ': unexpectedly short module')
    for p in ROOT.rglob('*.md'):
        txt = p.read_text(encoding='utf-8')
        if '\ufffd' in txt:
            errors.append(p.name + ': replacement character')
        if txt.count('```') % 2:
            errors.append(p.name + ': unmatched fence')
        for href in re.findall(r'\]\(([^)]+)\)', txt):
            if re.match(r'^(https?://|mailto:|#)', href):
                continue
            target = href.split('#', 1)[0]
            if target and not (p.parent / target).exists():
                errors.append(f'{p.relative_to(ROOT)}: broken link {href}')
    for p in ROOT.rglob('*.json'):
        try:
            json.loads(p.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'{p.name}: invalid JSON: {exc}')
    b = json.loads((ROOT/'08_Cau_hinh/baseline_v2.json').read_text())
    req = b['requirements']
    expected = {'hub_downstream_ip_peak_min_bps': 10000000,
                'vsat_upstream_ip_peak_bps': 3000000,
                'hub_upstream_aggregate_proposed_min_bps': 6000000}
    for key, value in expected.items():
        if req[key] != value:
            errors.append('Baseline mismatch: ' + key)
    ts_error_ns = 1e9 * b['timing']['arrival_error_target_symbol_fraction'] / b['profiles']['upstream']['symbol_rate_hz']
    if abs(ts_error_ns - 50) > 1e-9:
        errors.append('Timing arithmetic must produce 50 ns at max upstream rate')
    if crc32c(b'123456789') != 0xe3069283:
        errors.append('CRC-32C convention mismatch')
    # Header is the inner private control proposal; not a production protocol implementation.
    header = struct.pack('!4sBBHIIIIQII', b'SM01', 1, 0, 2, 0, 1, 0, 1, 1, 1, 0)
    if len(header) != 40:
        errors.append('Control-header layout must be 40 bytes')
    if not (1000-240-240 == 520 and 1002-245-245 == 512):
        errors.append('Timing example arithmetic')
    if abs(30.72e6 * 2 * 16 / 8 / 1e6 - 122.88) > 1e-8:
        errors.append('IQ bandwidth example arithmetic')
    report = {'status': 'PASS' if not errors else 'FAIL', 'errors': errors,
              'module_count': len(modules), 'markdown_count': len(list(ROOT.rglob('*.md'))),
              'scope': 'documentation structure, links, JSON, selected arithmetic and inner-header CRC/layout only',
              'hardware_performance_verified': False}
    return report

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    args = ap.parse_args()
    result = validate()
    if args.report:
        out = ROOT/'05_Ke_hoach_va_Kiem_thu/Ket_qua_kiem_tra_ho_so_v2.md'
        lines = ['# Kết quả kiểm tra hồ sơ v2', '',
                 '**Trạng thái kiểm tra cấu trúc hồ sơ:** ' + result['status'], '',
                 f"Số file mô-đun: {result['module_count']}; số file Markdown: {result['markdown_count']}.", '',
                 'Đã kiểm: đủ 20 mô-đun, mỗi file 11 phần; liên kết tương đối; JSON; các giá trị baseline 10M/3M và proposed aggregate6M; timing50ns; ví dụ băng thôngIQ; header40byte và CRC32C golden check.', '',
                 '**Chưa kiểm chứng phần cứng modem:** resource/Fmax/FER/RF/latency/throughput thực và conformance. PASS ở đây không phải sản phẩm đạt chỉ tiêu. Các test nghiệm thu hệ thống vẫn NOT_RUN cho đến khi có thiết bị và evidence.', '',
                 'Lặp lại: `python3 09_Tools/validate_docs.py --report` sau khi giải nén. Công cụ dùng thư viện chuẩn Python3.']
        if result['errors']:
            lines += ['', '## Lỗi'] + ['- '+e for e in result['errors']]
        out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result['status'] == 'PASS' else 1)
