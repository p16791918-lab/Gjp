#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""해설 모듈의 보기(①~⑤)를 실제 시험지 보기와 대조해 순서/내용 불일치를 찾는다.
사용: python3 scripts/검수_보기대조.py <YYYY> <교시>  (루트에서 실행)
"""
import sys, os, re, glob, unicodedata, importlib

def norm(s): return unicodedata.normalize('NFC', s)

def find_problem(year, kyo):
    for p in glob.glob(f'문제/{year}/*.pdf'):
        n = norm(os.path.basename(p))
        if f'_{kyo}교시' in n and '사진' not in n:
            return p
    return None

def actual_options(year, kyo):
    import fitz
    p = find_problem(year, kyo)
    d = fitz.open(p)
    txt = norm('\n'.join(d[i].get_text() for i in range(d.page_count)))
    pat = re.compile(r'(?:^|\n)\s*(\d{1,2})\.\s')
    idxs = [(int(m.group(1)), m.start()) for m in pat.finditer(txt)]
    qs = {}
    for i, (num, st) in enumerate(idxs):
        end = idxs[i+1][1] if i+1 < len(idxs) else len(txt)
        block = txt[st:end]
        opts = re.findall(r'[①②③④⑤]\s*([^\n①②③④⑤]+)', block)
        if len(opts) >= 5:
            qs[num] = [o.strip() for o in opts[:5]]
    return qs

def kw(text):
    """보기 텍스트에서 앞쪽 핵심어(한글/영문 토큰) 추출."""
    t = re.split(r'[—\-(·,]', text.strip())[0].strip()
    t = re.sub(r'\s+', '', t)
    return t

def main(year, kyo):
    sys.path.insert(0, 'scripts')
    mod = importlib.import_module(f'make_해설_{year}_{kyo}교시')
    QS = mod.QUESTIONS
    actual = actual_options(year, kyo)
    problems = []
    for item in QS:
        if 'num' not in item: continue
        num = item['num']; opts = item.get('options', {})
        if num not in actual or not opts: continue
        act = actual[num]
        mism = []
        for i in range(5):
            a = kw(act[i]); h = kw(opts.get(i+1, ''))
            # 매칭: 해설 핵심어가 실제 보기 핵심어를 포함/일치
            if not (a and h and (a[:3] in h or h[:3] in a or a in h or h in a)):
                mism.append((i+1, a, h))
        if mism:
            problems.append((num, mism))
    print(f'=== {year} {kyo}교시 : 총 {len(actual)}문항 중 {len(problems)}문항 보기 불일치 ===')
    for num, mism in problems:
        print(f'  [{num}번]')
        for pos, a, h in mism:
            print(f'     ⑤{pos}: 실제〈{a}〉  vs  해설〈{h}〉'.replace('⑤','보기'))
    return len(problems)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
