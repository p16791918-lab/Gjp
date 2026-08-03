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

# 페이지 꼬리말/구역 종료 표시 — 추출 시 어절 순서가 뒤섞여도 잡히게 함
FOOTER = re.compile(
    r'\s*(?:20\d\d\s*)?학년도.*$'          # ...학년도 기초의학종합평가 (N교시) p
    r'|\s*기초의학종합평가.*$'
    r'|\s*교시\s*\d*\s*종료.*$'            # (N)교시 N 종료 ...
    r'|\s*\(\s*\d교시\s*\).*$'
    r'|\s*\d+\s*/\s*\d+\s*$', re.S)
# 다음 문항 지문·검사치·보기표가 마지막 보기(주로 ⑤)에 딸려 들어온 것을 잘라냄
JUNK = re.compile(
    r'(?:혈액|혈청|소변|검사|혈압|맥박|체온|백혈구|혈소판|요단백|호흡수|참고치)\s*[:：]'
    r'|참고치|정상치|정상\s*범위'
    r'|[가-힣]*효소\s*[:：]'                # 다음 문항 검사(효소: 정상 범위 ...)
    r'|HBsAg|HBcAg|anti-HCV|HBV\s*DNA'      # 다음 문항 혈청검사 나열
    r'|(?:당화혈색소|요단백|신사구체여과율|사구체여과율)\s*[(:：+\d]'  # 다음 문항 임상검사
    r'|(?:^|[\s(])[a-e]\)\s|\*\s'
    r'|환자\s*[:：]'                        # 다음 문항 임상 지문
    r'|혈압\s*맥박|혈압\s*심박수'          # 다음 문항 활력징후 표
    r'|(?:^|\s)(?:PaO2|PaCO2|PACO2|pH)\s*[:：]'  # 다음 문항 검사 지문
    r'|(?:^|\s)[가나다라마]\)\s'           # 다음 문항 보기표(가) 나) ..)
    r'|(?:^|\s)[가나다라마]\s?[가-힣]{1,10}\s*\.'  # "가신생아 . 나광범위..." 뒤섞인 보기표
    r'|(?:^|\s)[A-E]\.\s'                  # 다음 문항 보기표(A. B. ..)
    r'|[①②③④⑤]|[A-E]\s[A-E]\s[A-E]')   # 다음 문항 보기표(①.. / A B C ..)
# 영문 검사치(이름 + 숫자 + 단위)
ENG_LAB = re.compile(
    r'[A-Za-z][A-Za-z0-9/().·\s-]{0,22}?[\s(]\d[\d.,~/]*\s*'
    r'(?:mg/dL|IU/L|mmHg|/mm3|μg/dL|ng/mL|g/dL|mmol|mEq|%)')
# 한글 검사치(임상 단위만 — 생리 값 보기 mmHg·mL 등은 건드리지 않음)
KOR_LAB = re.compile(
    r'[가-힣A-Za-z][가-힣A-Za-z0-9/\s]{0,7}?\s?\d[\d.,~/]*\s*'
    r'(?:μg/dL|mg/dL|IU/L|ng/mL|mEq|IU/mL)')
# 검사명 키워드로 시작하는 검사치(실제 보기어를 먹지 않도록 이름 앵커링)
KOR_LAB2 = re.compile(
    r'(?:혈색소|백혈구|적혈구|혈소판|혈장|혈청|헤모글로빈|알부민|크레아티닌|빌리루빈|요단백)\s*\d')
# 검사명(호르몬·지질 등) + 값 + 단위 형태의 누출(중간에 괄호·영문 허용).
# '중성지방' 같은 단어는 실제 보기이기도 하므로 반드시 숫자+단위가 뒤따를 때만 절단.
LAB_NAME_VAL = re.compile(
    r'(?:중성지방|콜레스테롤|난포자극호르몬|황체형성호르몬|에스트라디올|에스트로겐|프로락틴'
    r'|코티솔|갑상샘자극호르몬|성장호르몬|인슐린유사성장인자|아포지단백|ApoC[^\s]*)'
    r'[^0-9\n]{0,22}\d[\d.,~/]*\s*'
    r'(?:mg/dL|μg/dL|ng/dL|ng/mL|pg/mL|mIU/mL|IU/mL|mIU/L|IU/L|mEq|%)')

# 그림에서 추출된 잡기호(체크·프사이·따옴표 등)가 마지막 보기에 붙은 것
ARTIFACT = re.compile(r'[\d\s]*[√Ψ、｀´{}∙_].*$', re.S)
# 지문 가정문( "(단, ...)" 이 "( , ...)" 로 깨져 앞에 붙은 것 )
PREFIX_JUNK = re.compile(r'^\s*\(\s*,[^)]*\)\s*')
TAIL_JUNK = re.compile(r"[\s'\"√Ψ_·(]+$")   # 꼬리의 잡기호·미완결 여는괄호 제거

def dash_leak(t):
    """'옵션 - 서술문. - 서술문.' 형태로 다음 문항 서술이 딸려온 것 절단.
    정상 매칭보기(A - B - C, 1 - 7 - 98)는 세그먼트가 짧아 보존."""
    if ' - ' not in t:
        return t
    head, _, rest = t.partition(' - ')
    rest_segs = rest.split(' - ')
    long_seg = any(len(s.strip()) > 25 for s in rest_segs)
    sentence = len(rest_segs) >= 3 and re.search(r'다\.?(?:\s|$)|이다|있다|없다', rest)
    return head.strip() if (long_seg or sentence) else t

def clean(t):
    t = ' '.join(t.split())                   # 공백·줄바꿈 정규화(대시 누출 판별 위해)
    t = re.split(r'20\d\d\s*학년도', t)[0]   # 연도 꼬리말 + 이후 전부 제거
    t = dash_leak(t)
    t = FOOTER.sub('', t)
    t = PREFIX_JUNK.sub('', t)
    t = ARTIFACT.sub('', t)
    t = JUNK.split(t)[0]
    cut = len(t)
    for rx in (ENG_LAB, KOR_LAB, KOR_LAB2, LAB_NAME_VAL):
        m = rx.search(t)
        if m:
            cut = min(cut, m.start())
    return TAIL_JUNK.sub('', ' '.join(t[:cut].split())).strip()

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
               or bool(re.fullmatch(r'[①-⑤A-E가-마\s,·]+', o)) \
               or bool(re.fullmatch(r'[ㄱ-ㅎA-E→\s,·]+', o))   # ㄱ-ㄷ 조합·순서나열형
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

def load_override():
    p = 'data_보기_override.json'
    return json.load(open(p)) if os.path.exists(p) else {}

if __name__ == '__main__':
    OV = load_override()
    tot=0
    for y in ['2021','2022','2023','2024','2025']:
        for k in ['1','2','3','4','5','6']:
            try: data = extract(y, k)
            except Exception as e: print('SKIP', y, k, e); continue
            # 추출기가 원 문자 마커를 놓쳐 보기가 병합된 문항 수동 보정
            for num, opts in OV.get(f'{y}_{k}', {}).items():
                data[num] = {'opts': opts, 'image': is_imagelike(opts)}
            json.dump(data, open(f'data_보기/{y}_{k}.json','w'), ensure_ascii=False, indent=0)
            img = sum(1 for v in data.values() if v['image'])
            tot += len(data)
            print(f'{y}_{k}: {len(data)}문항 (이미지형 {img})')
    print('총', tot, '문항 저장')
