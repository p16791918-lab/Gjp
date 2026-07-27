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
    """페이지에서 '사진 N' 캡션 목록을 (label, cx, cy, x0, x1) 형태로 수집."""
    words = page.get_text('words')  # (x0,y0,x1,y1, text, block,line,word)
    caps = []
    for i, w in enumerate(words):
        if w[4] == '사진':
            # 같은 줄(y 근접)에서 바로 뒤 숫자 토큰을 라벨로
            for j in range(i + 1, min(i + 3, len(words))):
                wj = words[j]
                if abs(wj[1] - w[1]) < 6 and LABEL_RE.match(wj[4]):
                    label = wj[4]
                    x0 = min(w[0], wj[0]); x1 = max(w[2], wj[2])
                    caps.append((label, (x0 + x1) / 2, w[1], x0, x1))
                    break
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
        for label, cx, cy, cx0, cx1 in caps:
            # 캡션 바로 위의 이미지 블록 찾기 (bottom < cy, x범위 포함, 가장 가까운)
            best, best_gap = None, 1e9
            for bb in blocks:
                bx0, by0, bx1, by1 = bb
                if by1 <= cy + 2 and bx0 - 20 <= cx <= bx1 + 20:
                    gap = cy - by1
                    if 0 <= gap < best_gap:
                        best, best_gap = bb, gap
            if best is None:
                continue
            pad = 3
            clip = fitz.Rect(best[0] - pad, best[1] - pad, best[2] + pad, best[3] + pad)
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
