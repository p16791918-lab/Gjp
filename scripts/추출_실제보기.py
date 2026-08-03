#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문제 PDF에서 각 문항의 실제 보기(①~⑤)를 verbatim 추출 + 정답지 정답 읽기."""
import re, os, glob, unicodedata, json, sys
import fitz, openpyxl

def norm(s): return unicodedata.normalize('NFC', s)

def find(pat_dir, kyo, want_photo=False):
    for p in glob.glob(os.path.join(pat_dir, '*.pdf')):
        n = norm(os.path.basename(p))
        isph = '사진' in n
        if f'_{kyo}교시' in n and (isph == want_photo):
            return p
    return None

CIRC = '①②③④⑤'
def extract_options(year, kyo):
    p = find(f'문제/{year}', kyo, False)
    d = fitz.open(p)
    txt = norm('\n'.join(d[i].get_text() for i in range(d.page_count)))
    # 문항 시작: 줄 맨앞 "N." (1~2자리)
    pat = re.compile(r'(?:^|\n)\s*(\d{1,2})\.[\t ]')
    idxs = [(int(m.group(1)), m.start(), m.end()) for m in pat.finditer(txt)]
    qs = {}
    for i, (num, st, en) in enumerate(idxs):
        end = idxs[i+1][1] if i+1 < len(idxs) else len(txt)
        block = txt[en:end]
        # 첫 번째 ① 위치부터가 보기, 그 앞이 질문
        m1 = block.find('①')
        if m1 < 0:
            qs[num] = {'q': ' '.join(block.split()), 'opts': []}
            continue
        stem = ' '.join(block[:m1].split())
        optzone = block[m1:]
        # 각 마커에서 다음 마커 전까지
        opts = []
        for j, c in enumerate(CIRC):
            a = optzone.find(c)
            if a < 0: opts.append(''); continue
            b = len(optzone)
            for c2 in CIRC[j+1:]:
                bb = optzone.find(c2, a+1)
                if bb >= 0: b = bb; break
            opts.append(' '.join(optzone[a+1:b].split()))
        qs[num] = {'q': stem, 'opts': opts}
    return qs

def answer_key(year, kyo):
    xlsx = None
    for p in glob.glob(f'문제/{year}/*.xlsx'):
        xlsx = p; break
    if not xlsx: return {}
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    circ = {'①':1,'②':2,'③':3,'④':4,'⑤':5,'1':1,'2':2,'3':3,'4':4,'5':5}
    ans = {}
    for ws in wb.worksheets:
        rows = [[norm(str(c)).strip() if c is not None else '' for c in r]
                for r in ws.iter_rows(values_only=True)]
        for ri, row in enumerate(rows):
            # 헤더행: '번호' + 숫자들
            if any(x == '번호' for x in row):
                nums = {ci: int(v) for ci, v in enumerate(row) if v.isdigit()}
                if not nums: continue
                for r2 in rows[ri+1:ri+9]:
                    if r2 and r2[0] == f'{kyo}교시':
                        for ci, qn in nums.items():
                            v = r2[ci] if ci < len(r2) else ''
                            if v in circ: ans[qn] = circ[v]
                        break
    return ans

if __name__ == '__main__':
    y, k = sys.argv[1], sys.argv[2]
    qs = extract_options(y, k); ak = answer_key(y, k)
    for n in sorted(qs):
        o = qs[n]['opts']
        print(f"{n}. (정답 {ak.get(n,'?')}) {qs[n]['q'][:55]}")
        for i, t in enumerate(o, 1):
            mark = ' ★' if ak.get(n) == i else ''
            print(f"    {i}. {t}{mark}")
