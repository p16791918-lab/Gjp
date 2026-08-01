#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2021~2025 기종평 1교시(해부·조직·발생) 빈출유형 학습노트 PDF 생성.

각 빈출유형마다 '문제를 풀기 위해 필요한 내용'만 담는다.
  core  : 핵심 개념(반드시 알아야 풀리는 것)
  table : 감별 비교표(헷갈리는 것 나란히)
  trap  : 반복 출제 오답 함정
"""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Nanum', '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'))
pdfmetrics.registerFont(TTFont('NanumB', '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'))

CONTENT_W = (210 - 30) * mm

S = {
    'title': ParagraphStyle('t', fontName='NanumB', fontSize=20, leading=26, alignment=1,
        textColor=colors.HexColor('#12263a'), spaceAfter=4),
    'sub': ParagraphStyle('s', fontName='Nanum', fontSize=10.5, leading=15, alignment=1,
        textColor=colors.HexColor('#5a6b7b'), spaceAfter=3),
    'sec': ParagraphStyle('sec', fontName='NanumB', fontSize=13, leading=18, spaceBefore=12,
        spaceAfter=6, textColor=colors.white, backColor=colors.HexColor('#0f3460'),
        borderPad=6, leftIndent=3),
    'card': ParagraphStyle('c', fontName='NanumB', fontSize=11, leading=15, spaceBefore=2,
        spaceAfter=3, textColor=colors.HexColor('#0f3460')),
    'stars': ParagraphStyle('st', fontName='NanumB', fontSize=9, leading=12,
        textColor=colors.HexColor('#c0392b'), spaceAfter=3),
    'core': ParagraphStyle('co', fontName='Nanum', fontSize=9.3, leading=14.5, leftIndent=6,
        spaceAfter=2, textColor=colors.HexColor('#20303d')),
    'trap': ParagraphStyle('tr', fontName='Nanum', fontSize=8.8, leading=13.5, leftIndent=8,
        spaceBefore=2, spaceAfter=2, textColor=colors.HexColor('#8a4b08'),
        backColor=colors.HexColor('#fff5e6'), borderPad=4),
    'cell': ParagraphStyle('cell', fontName='Nanum', fontSize=8.3, leading=11.5,
        textColor=colors.HexColor('#20303d')),
    'cellh': ParagraphStyle('cellh', fontName='NanumB', fontSize=8.3, leading=11.5,
        textColor=colors.white, alignment=1),
    'tip': ParagraphStyle('tip', fontName='Nanum', fontSize=9, leading=14.5, leftIndent=6,
        spaceAfter=2, textColor=colors.HexColor('#234e52')),
}


def esc(t):
    # ReportLab 미니마크업에서 홑화살괄호 오류 방지: <b>..</b>만 허용
    t = t.replace('&', '&amp;')
    # 보호: <b> </b>
    t = t.replace('<b>', '\x01').replace('</b>', '\x02')
    t = t.replace('<', '〈').replace('>', '〉')
    t = t.replace('\x01', '<b>').replace('\x02', '</b>')
    return t


def P(t, st):
    return Paragraph(esc(t), S[st])


def make_table(header, rows):
    data = [[Paragraph(esc(h), S['cellh']) for h in header]]
    for r in rows:
        data.append([Paragraph(esc(c), S['cell']) for c in r])
    n = len(header)
    w = CONTENT_W
    col_w = [w * x for x in header_widths(n)]
    t = Table(data, colWidths=col_w, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34617f')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f4f8fb'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c3d3df')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


def header_widths(n):
    if n == 2: return [0.28, 0.72]
    if n == 3: return [0.24, 0.38, 0.38]
    if n == 4: return [0.12, 0.33, 0.30, 0.25]
    return [1.0 / n] * n


# ─────────────────────────────────────────────────────────────────────────────
# 학습 카드 데이터 : 문제 풀이에 필요한 내용만
# ─────────────────────────────────────────────────────────────────────────────
SECTIONS = [
    ('Ⅰ. 콩팥·비뇨 — 매년 최다 출제 구역', [
        {
            'title': '콩팥 토리곁장치 · 치밀반 · 레닌', 'stars': '★★★ 5년 연속(21·22·23·24·25)',
            'core': [
                '<b>토리곁세포(방사구체세포)</b> = 들세동맥 벽의 변형 평활근세포 → <b>레닌 분비</b>.',
                '<b>치밀반(macula densa)</b> = 먼쪽세관 벽 세포 → 세관 내 <b>NaCl 농도 감지</b>.',
                '레닌 분비 자극 3가지: ①들세동맥압 저하 ②치밀반 NaCl 저하 ③교감신경(β1) 항진.',
                '레닌은 <b>단백분해효소</b>(호르몬 아님) → 안지오텐신Ⅰ 생성 → ACE → 안지오텐신Ⅱ(혈관수축·알도스테론).',
                '그림 문제: 들세동맥 벽에 붙은 과립세포(레닌) 위치를 고르는 것이 핵심.'],
            'table': None,
            'trap': '⚠ 함정: 치밀반(감지)과 토리곁세포(분비)를 바꿔 제시 / 레닌을 "호르몬"이라 함(실제는 효소) / '
                    '메산지움세포(지지·수축)를 레닌 분비세포로 낚음.'},
        {
            'title': '사구체 여과장벽(여과틈새막 · 토리기저막)', 'stars': '★★★ 3년(21·22·23)',
            'core': [
                '여과장벽 3층: <b>창내피</b> → <b>토리기저막(GBM)</b> → <b>발세포 여과틈새막(슬릿막)</b>.',
                'GBM = IV형 콜라겐 + 라미닌 + <b>음전하 헤파란황산</b> → 크기·전하로 선택여과.',
                '여과틈새막의 핵심 단백 = <b>네프린</b>(발돌기 사이 지퍼).',
                '<b>발돌기 소실(융합)</b> → 단백뇨 → 미세변화병(소아 신증후군).'],
            'table': {'header': ['구조', '기능/특징'],
                      'rows': [
                          ['창내피', '큰 혈구 차단(창=fenestra)'],
                          ['토리기저막(GBM)', 'IV형 콜라겐·라미닌·음전하 → 알부민 차단'],
                          ['발세포 여과틈새', '네프린 슬릿막, 소실 시 단백뇨']]},
            'trap': '⚠ 함정: "음전하·IV형콜라겐·라미닌" 지문 → 무조건 <b>기저막(GBM)</b>이지 내피/발세포 아님.'},
        {
            'title': '항이뇨호르몬(ADH) 작용부위', 'stars': '★★★ 3년(22·23·24)',
            'core': [
                'ADH = 시상하부(시각위핵·뇌실옆핵) 생산 → <b>뇌하수체 뒤엽</b>에서 분비.',
                '작용부위 = <b>집합관</b> 주세포 → 아쿠아포린-2를 막으로 이동 → 물 재흡수↑.',
                '결핍/무반응 = 요붕증(희석뇨·고나트륨·다갈). 그림에서 "집합관"을 고른다.'],
            'table': None,
            'trap': '⚠ 함정: ADH 작용부위를 토리(여과)·헨레고리·먼쪽세관으로 낚음 → 정답은 <b>집합관</b>.'},
    ]),
    ('Ⅱ. 내분비 — 부신이 절대 빈출', [
        {
            'title': '부신겉질 3층 · 쿠싱 · 코티솔', 'stars': '★★★ 5년 연속(21·22·23·24·25)',
            'core': [
                '겉질 바깥→안: <b>토리층(알도스테론)·다발층(코티솔)·그물층(안드로젠)</b> / 속질=카테콜아민.',
                '쿠싱증후군 = 코티솔↑ → 중심비만·달덩이얼굴·목뒤지방·피부선조·고혈당.',
                'ACTH↑(뇌하수체·이소성)면 색소침착 동반 / 부신성이면 ACTH 억제.',
                '그림: 넓은 다발층(코티솔) 위치를 고르는 문제가 반복.'],
            'table': {'header': ['층', '분비', '조절'],
                      'rows': [
                          ['토리층(겉)', '알도스테론', '레닌-안지오텐신·K⁺'],
                          ['다발층(중)', '코티솔', 'ACTH'],
                          ['그물층(속)', '안드로젠', 'ACTH'],
                          ['속질', '에피/노르에피네프린', '교감신경절이전']]},
            'trap': '⚠ 함정: 알도스테론(토리층)과 코티솔(다발층) 층 위치 바꿈 / 속질(카테콜아민)을 코티솔로 낚음.'},
        {
            'title': 'hCG · 태반 · 황체 유지', 'stars': '★★★ 3년(22·23·25)',
            'core': [
                'hCG = 태반 <b>융합영양막세포</b> 분비 → <b>황체 유지</b> → 프로게스테론 지속.',
                '소변 hCG로 임신 진단. 황체는 hCG의 표적이지 생산처가 아님.',
                '태반 <b>모체부분 = 바닥탈락막</b> / 태아부분 = 융모막융모·융모막판.'],
            'table': None,
            'trap': '⚠ 함정: hCG 생산 장기를 난소·뇌하수체로 낚음 → 정답은 <b>태반</b>.'},
    ]),
    ('Ⅲ. 뇌·신경 — 뇌혈관과 척수', [
        {
            'title': '대뇌동맥 · 동맥류 · 거미막밑출혈', 'stars': '★★★ 5년 연속(21·22·23·24·25)',
            'core': [
                '윌리스고리(대뇌동맥고리). 동맥류 호발: <b>앞교통 〉 뒤교통 〉 중대뇌동맥 갈림</b>.',
                '동맥류 파열 → <b>거미막밑출혈</b>(벼락두통, 목경직).',
                '중대뇌동맥 = 가장 흔한 폐색 → 반대쪽 <b>얼굴·팔</b> 마비, 우성반구면 실어증.',
                '앞대뇌동맥 = 반대쪽 <b>다리</b> 마비. 뒤대뇌동맥 = 시각(뒤통수엽).'],
            'table': {'header': ['동맥', '지배·증상'],
                      'rows': [
                          ['앞대뇌', '안쪽면 → 반대쪽 다리 마비·감각저하'],
                          ['중대뇌', '가쪽면 → 반대쪽 얼굴·팔, 우성반구 실어증'],
                          ['뒤대뇌', '뒤통수엽 → 반대쪽 시야결손'],
                          ['앞교통/뒤교통', '동맥류 최호발 → 거미막밑출혈']]},
            'trap': '⚠ 함정: 다리(앞대뇌)와 팔·얼굴(중대뇌) 지배영역 바꿈 / 동맥류 파열을 경막밑·경막바깥으로 낚음.'},
        {
            'title': '척수원뿔 · 허리천자 높이', 'stars': '★★★ 4년(22·23·24·25)',
            'core': [
                '성인 척수는 <b>L1~L2</b>에서 원뿔(척수원뿔)로 끝남 → 아래는 말총·종말끈.',
                '허리천자는 척수 손상 피해 <b>L3-4 또는 L4-5</b>(원뿔보다 아래)에서 시행.',
                '신생아는 척수가 더 아래(L3)까지 → 천자 높이 주의.'],
            'table': None,
            'trap': '⚠ 함정: 원뿔 끝(L1~2)과 천자 위치(L3~5)를 섞어 출제.'},
        {
            'title': '별아교세포 · 혈액뇌장벽(BBB)', 'stars': '★★★ 3년(21·24·25)',
            'core': [
                '별아교세포 <b>발끝(end-foot)</b>이 뇌 모세혈관을 감싸 <b>혈액뇌장벽</b> 형성·유지.',
                '표지자 = <b>GFAP</b>. 손상 시 반흔(신경아교증) 형성.',
                'BBB의 밀착이음은 내피세포가 만들고, 별아교세포가 유도·유지.'],
            'table': None,
            'trap': '⚠ 함정: BBB "밀착이음 자체"는 내피가 만듦 / GFAP를 희소돌기·미세아교 표지로 낚음.'},
    ]),
    ('Ⅳ. 말초신경 · 근골격', [
        {
            'title': '팔신경 손상 감별(자·정중·노신경)', 'stars': '★★★ 자신경 4년(21·23·24·25)',
            'core': [
                '세 신경의 <b>운동(근육)·감각(피부) 지배 영역</b>과 손상부위·증상을 함께 외운다.',
                '노신경 = <b>모든 폄근(extensor)</b> 담당 → 손상 시 못 폄(손목처짐). "노신경=펴는 신경".',
                '정중신경 엄지두덩 운동 = <b>LOAF</b>(벌레근1·2, 반대근, 짧은벌림근, 짧은굽힘근).',
                '자신경 = <b>손 속(내재근) 대부분</b>(뼈사이근·셋째넷째벌레근·새끼두덩) → 손상 시 갈퀴손.'],
            'table': {'header': ['신경', '운동 지배(근육)', '감각 지배(피부)', '손상부위 → 증상'],
                      'rows': [
                          ['노신경',
                           '위팔·아래팔 폄근 전체(세갈래근·손목/손가락 폄근·뒤침근)',
                           '손등 가쪽(엄지~중지 근위)·위팔/아래팔 뒤',
                           '위팔뼈 몸통(노신경고랑) → 손목처짐'],
                          ['정중신경',
                           '아래팔 굽힘근 대부분·엄지두덩(LOAF)·원엎침근',
                           '손바닥 가쪽 3.5손가락(엄지·검지·중지·약지½)·손끝 손등쪽',
                           '손목굴 → 원숭이손·엄지두덩 위축'],
                          ['자신경',
                           '손 내재근 대부분(뼈사이근·벌레근3·4·새끼두덩)·자쪽손목굽힘근',
                           '손 안쪽 1.5손가락(새끼·약지½) 손바닥·손등',
                           '팔꿉 안쪽위관절융기·기욤관 → 갈퀴손']]},
            'trap': '⚠ 함정: 엄지두덩 운동=정중신경 / 손 내재근·새끼두덩=자신경 / 폄근·손목처짐=노신경. '
                    '감각도 엄지쪽(정중)·새끼쪽(자)·손등(노)로 바꿔 낚음. "갈퀴손=자신경, 원숭이손=정중신경".'},
        {
            'title': '중간볼기근 · Trendelenburg 징후', 'stars': '★★★ 4년(21·22·23·25)',
            'core': [
                '중간·작은볼기근(<b>위볼기신경</b>) = 한다리 지지 때 <b>디딤다리쪽 골반을 수평 유지</b>.',
                '약화·신경손상 → 디딤다리 반대쪽 골반이 <b>처짐</b>(Trendelenburg 양성).',
                '벌림(외전) 근육. 큰볼기근(폄)·궁둥구멍근(가쪽돌림)과 구별.'],
            'table': None,
            'trap': '⚠ 함정: 처지는 쪽이 "디딤다리 반대쪽"임을 반대로 서술 / 큰볼기근(폄)으로 낚음.'},
        {
            'title': '무릎 십자인대(앞 vs 뒤)', 'stars': '★★★ 3년(22·24·25)',
            'core': [
                '<b>앞십자인대(ACL)</b> = 정강뼈 앞이동 방지 → 손상 시 <b>앞당김검사 양성</b>.',
                '<b>뒤십자인대(PCL)</b> = 정강뼈 뒤이동 방지 → 손상 시 <b>뒤당김검사 양성</b>(종아리 뒤로 빠짐).'],
            'table': None,
            'trap': '⚠ 함정: 앞/뒤 당김검사 방향을 바꿔 제시. "종아리가 뒤로 빠짐"=뒤십자.'},
        {
            'title': '손목굴증후군 · 손배뼈 골절', 'stars': '★★★ 3년(22·23·24)',
            'core': [
                '손목굴증후군 = 손목굴에서 <b>정중신경 압박</b> → 엄지두덩 위축·가쪽 손가락 저림.',
                '손배뼈(주상골) 골절 = <b>해부학코담배갑 압통</b>, 넘어질 때 손 짚음 → <b>무혈성괴사</b> 위험(근위부 혈류).'],
            'table': None,
            'trap': '⚠ 함정: 손배뼈 골절의 합병증(무혈성괴사)·압통 위치(코담배갑) 혼동.'},
        {
            'title': '심장 판막 청진부위', 'stars': '★★★ 4년(22·23·24·25)',
            'core': ['판막별 최적 청진부위를 정확히. 그림에서 A~E 위치 고르기가 반복.'],
            'table': {'header': ['판막', '청진 부위'],
                      'rows': [
                          ['대동맥판', '오른쪽 2번째 갈비사이'],
                          ['폐동맥판', '왼쪽 2번째 갈비사이'],
                          ['삼첨판', '왼쪽 복장뼈 아래(4~5번째)'],
                          ['승모판', '심장꼭대기(왼쪽 중간빗장선 5번째)']]},
            'trap': '⚠ 함정: 대동맥(오른쪽)·폐동맥(왼쪽) 위쪽 2늑간 좌우 바꿈.'},
    ]),
    ('Ⅴ. 순환 · 소화 · 호흡 조직', [
        {
            'title': '지라(지라동맥 · 붉은속질)', 'stars': '★★★ 4년(21·23·24·25)',
            'core': [
                '지라동맥 = <b>복강동맥</b> 가지 → 이자(몸통·꼬리)·위바닥(<b>짧은위동맥</b>) 공급.',
                '<b>붉은속질</b> = 오래된·비정상 적혈구 제거(혈액 여과). <b>흰속질</b> = 림프조직(면역).'],
            'table': None,
            'trap': '⚠ 함정: 붉은속질(적혈구 제거) vs 흰속질(면역) 기능 바꿈 / 짧은위동맥 기원(지라동맥) 낚음.'},
        {
            'title': '작은창자 부위 감별(돌창자·빈창자·샘창자)', 'stars': '★★★ 돌창자 3년(21·22·23)',
            'core': ['조직 사진에서 "어느 창자"인지 특징 구조로 판별.'],
            'table': {'header': ['부위', '특징 구조'],
                      'rows': [
                          ['샘창자', '점막밑 <b>브루너샘</b>'],
                          ['빈창자', '길고 촘촘한 융모, 파이어판 드묾'],
                          ['돌창자', '<b>파이어판</b>(집합림프소절)']]},
            'trap': '⚠ 함정: 파이어판=돌창자 / 브루너샘=샘창자. 융모만 보고 헷갈리게 함.'},
        {
            'title': '허파꽈리 세포(1형 vs 2형 폐포세포)', 'stars': '★★★ 3년(22·23·24)',
            'core': [
                '<b>1형 폐포세포</b> = 얇고 넓음, 가스교환.',
                '<b>2형 폐포세포</b> = 통통, <b>표면활성물질(surfactant)</b> 분비, 층판소체.',
                '2형 미성숙 → 표면활성물질 부족 → <b>신생아호흡곤란증후군</b>.'],
            'table': None,
            'trap': '⚠ 함정: 가스교환=1형, 표면활성물질=2형. 큰포식세포(먼지세포)와도 구별.'},
        {
            'title': '모세혈관 3유형', 'stars': '★★★ 3년(23·24·25)',
            'core': ['내피 구조로 유형을 나누고 장기를 연결.'],
            'table': {'header': ['유형', '특징', '장기'],
                      'rows': [
                          ['연속형', '내피 연속·밀착', '뇌(BBB)·근육·폐·피부'],
                          ['창형(fenestrated)', '내피에 창(구멍)', '콩팥토리·내분비샘·창자'],
                          ['굴모양(sinusoid)', '큰 틈·불연속', '간·지라·골수']]},
            'trap': '⚠ 함정: 콩팥토리=창형(여과), 간·지라=굴모양. 뇌=연속형(BBB).'},
    ]),
    ('Ⅵ. 생식 · 발생', [
        {
            'title': '고환 세포(세르톨리 vs 라이디히)', 'stars': '★★★ 4년(21·23·24·25)',
            'core': ['정세관 안/밖과 기능·자극호르몬으로 감별.'],
            'table': {'header': ['세포', '위치', '기능·조절'],
                      'rows': [
                          ['세르톨리(버팀)', '정세관 안', '혈액고환장벽, 인히빈·AMH, FSH 반응, 지지·영양'],
                          ['라이디히(사이질)', '정세관 사이', '테스토스테론, LH 반응']]},
            'trap': '⚠ 함정: 테스토스테론=라이디히(사이질) / 혈액고환장벽·인히빈=세르톨리. "분열 안 함·핵소체 뚜렷"=세르톨리.'},
        {
            'title': '여성생식 인대 · 혈관(난소걸이·자궁동맥)', 'stars': '★★★ 4년(21·22·24·25)',
            'core': [
                '<b>난소걸이인대(깔때기골반인대)</b> = <b>난소 동·정맥</b> 통과 → 난소절제 시 결찰.',
                '<b>자궁동맥</b>(속엉덩동맥 가지) = <b>요관 위로 교차</b>("water under the bridge") → 자궁 수술 시 요관 손상 주의.',
                '<b>기본인대(가로자궁목인대)</b> = 자궁 주된 지지 + 자궁동맥 통과(자궁탈출과 관련).',
                '고유난소인대=난소↔자궁 / 자궁원인대=자궁↔샅굴.'],
            'table': None,
            'trap': '⚠ 함정: 난소동맥 통과=난소걸이인대(고유난소인대·자궁원인대 아님) / 자궁동맥이 요관 "위"를 지남.'},
        {
            'title': '신경능선 유래 구조 · 이상', 'stars': '★★★ 3년(23·24·25)',
            'core': [
                '신경능선 유래: 말초신경절·<b>슈반세포</b>·<b>부신속질</b>·<b>멜라닌세포</b>·치아상아질·연수막·인두굽이 연골.',
                '이주 실패 → <b>히르슈슈프룽병(선천거대결장)</b>: 원위 장 신경절세포 결여.'],
            'table': None,
            'trap': '⚠ 함정: 부신속질(신경능선)과 부신겉질(중배엽) 유래 다름 / 거대결장 원인=신경절세포 결여.'},
    ]),
]

TIPS = [
    '① 콩팥(토리곁장치·여과장벽·ADH)·부신겉질·뇌혈관은 매년 고정 출제 → 최우선 암기.',
    '② 그림 A~E 문제는 "구조의 위치"를 묻는다 → 각 층·부위의 상대적 위치를 그림으로 기억.',
    '③ 신경/근육은 "손상부위 → 증상" 또는 "증상 → 손상부위" 양방향으로 감별 연습.',
    '④ 오답은 대개 "짝을 바꿔치기"(레닌↔치밀반, 1형↔2형 폐포, 앞↔뒤 십자) → 비교표로 대비.',
    '⑤ 세포/조직 감별은 표지자·특징 구조 한 개로 결판 → GFAP=별아교, 파이어판=돌창자, 네프린=슬릿막.',
]


def build():
    doc = SimpleDocTemplate('기종평_1교시_빈출유형_학습노트.pdf', pagesize=A4,
                            leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=14 * mm, bottomMargin=14 * mm)
    story = []
    story.append(Spacer(1, 40 * mm))
    story.append(P('기초의학종합평가 1교시', 'title'))
    story.append(P('빈출유형 학습노트 (해부·조직·발생)', 'title'))
    story.append(Spacer(1, 6 * mm))
    story.append(P('2021 · 2022 · 2023 · 2024 · 2025 — 5개 연도 교차 분석', 'sub'))
    story.append(P('문제를 풀기 위해 필요한 핵심 개념 · 감별 비교표 · 반복 오답 함정', 'sub'))
    story.append(Spacer(1, 10 * mm))
    story.append(P('★★★ = 3년 이상 출제(최빈출)  ·  등급 옆 괄호는 출제 연도', 'sub'))
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    for sec_title, cards in SECTIONS:
        story.append(P(sec_title, 'sec'))
        for c in cards:
            block = [P(c['title'], 'card'), P(c['stars'], 'stars')]
            for line in c['core']:
                block.append(P('• ' + line, 'core'))
            if c.get('table'):
                block.append(Spacer(1, 2 * mm))
                block.append(make_table(c['table']['header'], c['table']['rows']))
            block.append(Spacer(1, 1.5 * mm))
            block.append(P(c['trap'], 'trap'))
            block.append(Spacer(1, 3 * mm))
            block.append(HRFlowable(width='100%', thickness=0.4,
                                    color=colors.HexColor('#d5dee6'), spaceAfter=3))
            story.append(KeepTogether(block))

    story.append(P('시험 전략 TIP', 'sec'))
    for t in TIPS:
        story.append(P(t, 'tip'))

    doc.build(story)
    print('학습노트 생성 완료: 기종평_1교시_빈출유형_학습노트.pdf')


if __name__ == '__main__':
    build()
