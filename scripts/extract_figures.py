#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""기종평 '사진자료' PDF에서 문항별 사진을 개별 이미지로 추출한다.

각 페이지의 임베디드 이미지 배치 사각형과 그 아래 '사진 N' 캡션을 매칭하여
사진 라벨별 PNG를 figures/ 아래에 저장하고, 라벨→파일 경로 맵(JSON)을 남긴다.

사용:  python3 extract_figures.py <사진PDF> <출력접두사>
예:    python3 extract_figures.py 2021/2021_기종평_사진_1교시.pdf 2021_1
"""
import sys, os, re, json
import fitz

LABEL_RE = re.compile(r'^\d+(?:-\d+)?$')  # 1, 1-1, 28-3 ...
DPI = 150
JPG_QUALITY = 80
OUT_DIR = 'figures'


def collect_captions(page):
    """페이지에서 '사진 N' / '사진 N - M' 캡션을 (label, cx, cy, x0, x1)로 수집.

    캡션이 '사진 29 - 1'처럼 대시·숫자가 공백으로 분리돼 여러 토큰으로 쪼개져도
    이어 붙여 '29-1' 형태의 라벨로 인식한다(하위번호 붙은 사진 분리).
    """
    words = page.get_text('words')  # (x0,y0,x1,y1, text, block,line,word)
    n = len(words)
    caps = []
    for i, w in enumerate(words):
        if w[4] != '사진':
            continue
        y = w[1]
        # 같은 줄에서 '사진' 뒤로 이어지는 토큰을 모은다(다음 '사진' 전까지)
        grp = []
        for j in range(i + 1, min(i + 6, n)):
            wj = words[j]
            if abs(wj[1] - y) >= 6 or wj[4] == '사진':
                break
            grp.append(wj)
        joined = ''.join(t[4] for t in grp)
        m = re.match(r'(\d+(?:\s*-\s*\d+)?)', joined)
        if not m:
            continue
        label = re.sub(r'\s*-\s*', '-', m.group(1))   # '29-1'
        # 라벨 문자를 이루는 토큰까지만 x범위에 포함
        used, acc = [w], ''
        for t in grp:
            if len(acc) >= len(m.group(1).replace(' ', '')):
                break
            acc += t[4]; used.append(t)
        x0 = min(t[0] for t in used); x1 = max(t[2] for t in used)
        caps.append((label, (x0 + x1) / 2, y, x0, x1))
    return caps


def extract(pdf_path, prefix):
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = fitz.open(pdf_path)
    mapping = {}
    for pno in range(len(doc)):
        page = doc[pno]
        caps = collect_captions(page)
        if not caps:
            continue
        blocks = [b['bbox'] for b in page.get_image_info()]
        zoom = DPI / 72.0
        H_TOL = 24     # 캡션-이미지 가로 정렬 허용치(pt)
        MAX_GAP = 450  # 이미지 아래 캡션까지 허용 세로 간격(pt).
                       # 스캔 이미지가 2px 줄무늬 수십 개로 쪼개진 경우 상단 줄무늬가
                       # 캡션에서 멀어도 포함되도록 크게 잡는다. "가장 가까운 캡션 배정"
                       # 규칙이 이미 아래쪽 다른 사진과의 경계를 막아준다.

        # 각 이미지 블록을 "바로 아래 가장 가까운(가로로 겹치는) 캡션"에 배정한다.
        # 한 사진이 여러 타일로 쪼개져 있어도 같은 캡션에 모여 union 되고,
        # 전폭/가운데정렬 캡션이나 2열 배치도 안전하게 분리된다.
        assign = {label: [] for (label, *_ ) in caps}
        for bb in blocks:
            bx0, by0, bx1, by1 = bb
            best, best_gap = None, 1e9
            for (label, cx, cy, cx0, cx1) in caps:
                gap = cy - by1
                if gap < -3 or gap > MAX_GAP:      # 캡션은 이미지 아래·너무 멀지 않게
                    continue
                h_overlap = not (bx1 < cx0 - H_TOL or bx0 > cx1 + H_TOL) or (bx0 <= cx <= bx1)
                if not h_overlap:
                    continue
                if gap < best_gap:
                    best_gap, best = gap, label
            if best is not None:
                assign[best].append(bb)

        for (label, cx, cy, cx0, cx1) in caps:
            sel = assign.get(label, [])
            if sel:
                ux0 = min(b[0] for b in sel); uy0 = min(b[1] for b in sel)
                ux1 = max(b[2] for b in sel); uy1 = max(b[3] for b in sel)
            else:
                # 이미지 블록을 못 찾으면 캡션 바로 위 가장 가까운 블록으로 대체
                best, best_gap = None, 1e9
                for bb in blocks:
                    if bb[3] <= cy + 2 and bb[0] - 20 <= cx <= bb[2] + 20:
                        gap = cy - bb[3]
                        if 0 <= gap < best_gap:
                            best, best_gap = bb, gap
                if best is None:
                    continue
                ux0, uy0, ux1, uy1 = best

            pad = 4
            clip = fitz.Rect(ux0 - pad, uy0 - pad, ux1 + pad, uy1 + pad)
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
            fname = f'{prefix}_사진{label}.jpg'
            fpath = os.path.join(OUT_DIR, fname)
            pix.pil_save(fpath, format='JPEG', quality=JPG_QUALITY, optimize=True)
            mapping[label] = fpath
    map_path = os.path.join(OUT_DIR, f'{prefix}_map.json')
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f'{prefix}: 사진 {len(mapping)}개 추출 → {OUT_DIR}/  (map: {map_path})')
    return mapping


if __name__ == '__main__':
    extract(sys.argv[1], sys.argv[2])
