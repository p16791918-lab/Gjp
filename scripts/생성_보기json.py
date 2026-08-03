#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문제 PDF에서 실제 보기를 추출·정제해 data_보기/{연도}_{교시}.json 저장.
 - 페이지 꼬리말/헤더 제거
 - 이미지형(보기가 A~E, 가나다라마, 조합) 판별 플래그
"""
import sys, os, re, glob, unicodedata, json
sys.path.insert(0, os.path.dirname(__file__))
import fitz

def norm(s): return unicodedata.normalize('NFC', s)
CIRC = '①②③④⑤'

FOOTER = re.compile(r'\s*20\d\d\s*학년도.*$|\s*기초의학종합평가.*$|\s*\d+\s*/\s*\d+\s*$|\s*\(\s*\d교시\s*\).*$')

def clean(t):
    t = FOOTER.sub('', t)
    return ' '.join(t.split()).strip()

def find(year, kyo):
    for p in glob.glob(f'문제/{year}/*.pdf'):
        n = norm(os.path.basename(p))
        if f'_{kyo}교시' in n and '사진' not in n:
            return p
    return None

def is_imagelike(opts):
    labs = {'A','B','C','D','E','가','나','다','라','마'}
    def bare(o):
        o = o.strip()
        return (o in labs) or bool(re.fullmatch(r'[A-E가-마]\s*[-~]\s*[A-E가-마]', o)) \
               or bool(re.fullmatch(r'[①-⑤A-E가-마\s,·]+', o))
    return sum(1 for o in opts if o and bare(o)) >= 3

def _segments(block):
    """block 에서 ①~⑤ 마커 위치로 (pre, [s1..s5]) 분리. s_k = 마커 k 다음~다음 마커 전."""
    idx = [block.find(c) for c in CIRC]
    if idx[0] < 0:
        return None, None
    pre = block[:idx[0]]
    segs = []
    for j in range(5):
        a = idx[j]
        if a < 0:
            segs.append('')
            continue
        b = len(block)
        for jj in range(j + 1, 5):
            if idx[jj] >= 0:
                b = idx[jj]; break
        segs.append(block[a + 1:b])
    return pre, segs


def extract(year, kyo):
    p = find(year, kyo)
    d = fitz.open(p)
    txt = norm('\n'.join(d[i].get_text() for i in range(d.page_count)))
    pat = re.compile(r'(?:^|\n)\s*(\d{1,2})\.[\t ]')
    idxs = [(int(m.group(1)), m.start(), m.end()) for m in pat.finditer(txt)]
    out = {}
    for i, (num, st, en) in enumerate(idxs):
        end = idxs[i+1][1] if i+1 < len(idxs) else len(txt)
        block = txt[en:end]
        pre, segs = _segments(block)
        if segs is None:
            continue
        after5 = clean(segs[4])
        if after5:
            # 레이아웃 A: 번호가 보기 텍스트 '앞'  →  s_k = 보기 k
            opts = [clean(x) for x in segs]
        else:
            # 레이아웃 B: 번호가 보기 텍스트 '뒤'  →  보기1은 pre(질문 뒤), 보기2~5는 s1~s4
            m = re.split(r'\?', pre)
            opt1 = clean(m[-1]) if len(m) > 1 else clean(pre.split('\n')[-1])
            opts = [opt1] + [clean(x) for x in segs[:4]]
        if sum(1 for o in opts if o) >= 4:
            out[num] = {'opts': opts, 'image': is_imagelike(opts)}
    return out

if __name__ == '__main__':
    tot=0
    for y in ['2021','2022','2023','2024','2025']:
        for k in ['1','2','3','4','5','6']:
            try: data = extract(y, k)
            except Exception as e: print('SKIP', y, k, e); continue
            json.dump(data, open(f'data_보기/{y}_{k}.json','w'), ensure_ascii=False, indent=0)
            img = sum(1 for v in data.values() if v['image'])
            tot += len(data)
            print(f'{y}_{k}: {len(data)}문항 (이미지형 {img})')
    print('총', tot, '문항 저장')
