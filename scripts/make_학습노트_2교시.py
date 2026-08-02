#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2021~2025 기종평 2교시(생화학) 빈출유형 학습노트 PDF 생성."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle,
    PageBreak, Image as RLImage
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

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
    'core': ParagraphStyle('co', fontName='Nanum', fontSize=9.3, leading=15, leftIndent=6,
        spaceAfter=3, textColor=colors.HexColor('#20303d')),
    'trap': ParagraphStyle('tr', fontName='Nanum', fontSize=8.8, leading=14, leftIndent=8,
        spaceBefore=2, spaceAfter=2, textColor=colors.HexColor('#8a4b08'),
        backColor=colors.HexColor('#fff5e6'), borderPad=4),
    'cell': ParagraphStyle('cell', fontName='Nanum', fontSize=8.3, leading=11.5,
        textColor=colors.HexColor('#20303d')),
    'cellh': ParagraphStyle('cellh', fontName='NanumB', fontSize=8.3, leading=11.5,
        textColor=colors.white, alignment=1),
    'tip': ParagraphStyle('tip', fontName='Nanum', fontSize=9, leading=15, leftIndent=6,
        spaceAfter=3, textColor=colors.HexColor('#234e52')),
    'cap': ParagraphStyle('cap', fontName='Nanum', fontSize=7.5, leading=10, alignment=1,
        spaceBefore=1, spaceAfter=1, textColor=colors.HexColor('#6b7b8b')),
}


def esc(t):
    # NanumGothic에 없는 글리프 치환 (아래첨자·수학기호)
    for a, b in (('₂', '2'), ('₁', '1'), ('₃', '3'), ('−', '-'), ('–', '-')):
        t = t.replace(a, b)
    t = t.replace('&', '&amp;')
    t = t.replace('<b>', '\x01').replace('</b>', '\x02')
    t = t.replace('<', '〈').replace('>', '〉')
    t = t.replace('\x01', '<b>').replace('\x02', '</b>')
    return t


def P(t, st):
    return Paragraph(esc(t), S[st])


def make_img(path, cap, max_w=72 * mm, max_h=92 * mm):
    iw, ih = PILImage.open(path).size
    s = min(max_w / iw, max_h / ih)
    img = RLImage(path, width=iw * s, height=ih * s)
    img.hAlign = 'CENTER'
    return KeepTogether([Spacer(1, 1 * mm), img, P(cap, 'cap')])


def header_widths(n):
    if n == 2: return [0.30, 0.70]
    if n == 3: return [0.26, 0.37, 0.37]
    return [1.0 / n] * n


def make_table(header, rows):
    data = [[Paragraph(esc(h), S['cellh']) for h in header]]
    for r in rows:
        data.append([Paragraph(esc(c), S['cell']) for c in r])
    col_w = [CONTENT_W * x for x in header_widths(len(header))]
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


SECTIONS = [
    ('Ⅰ. 에너지대사 — 매년 다수 출제', [
        {
            'title': '전자전달계와 그 억제제(CO·청산가리)', 'stars': '★★★ 5년 연속(21·22·23·24·25)',
            'core': [
                '전자전달계는 미토콘드리아 속막에서 복합체 I(NADH)·II(숙신산/FADH₂)·III·IV를 거쳐 전자를 산소로 넘기고, '
                '그 에너지로 양성자를 퍼내 ATP 합성효소가 ATP를 만든다.',
                '<b>일산화탄소·청산가리는 복합체 IV(시토크롬 c 산화효소)</b>를 막아 세포호흡을 정지시키므로, 상류의 '
                'FMN·CoQ·시토크롬은 환원형으로 정체되고 복합체 II의 FAD는 상대적으로 산화형으로 남는다.',
                '짝풀림제(2,4-DNP·UCP1)는 양성자를 새게 해 전자전달은 계속되나 ATP 대신 열이 난다.'],
            'table': {'header': ['표적', '억제제/작용'],
                      'rows': [
                          ['복합체 I', '로테논·아미탈'],
                          ['복합체 III', '안티마이신 A'],
                          ['복합체 IV', '청산가리·일산화탄소·아자이드'],
                          ['ATP 합성효소', '올리고마이신'],
                          ['짝풀림(막 누출)', '2,4-DNP·UCP1(열 발생)']]},
            'img': ('diagrams/electron_transport.png', '▲ 전자전달계와 억제 지점'),
            'trap': '⚠ 함정 — CO·청산가리를 복합체 I·III로 낚는다(정답은 복합체 IV). 짝풀림제는 전자전달을 "멈춘다"가 '
                    '아니라 오히려 계속되며 열로 빠진다.'},
        {
            'title': '금식 연료대사와 케톤체', 'stars': '★★★ 5년 연속(21·22·23·24·25)',
            'core': [
                '금식이 진행되면 간은 연료 공급 방식을 <b>글리코겐 분해(수 시간) → 당신생(하루 안팎) → 케톤생성(수 일)</b> '
                '순으로 바꾼다.',
                '지방조직에서 나온 지방산이 간에서 β-산화되어 생긴 아세틸CoA가 케톤체가 되고, 이 케톤체가 포도당을 아껴 '
                '뇌의 주 연료가 된다.',
                '간은 케톤체를 만들지만 케톤체를 이용하는 효소(SCOT)가 없어 <b>자기가 만든 케톤체는 쓰지 못하고</b> 전량 '
                '말초로 보낸다.'],
            'table': {'header': ['시기', '주 연료·공급'],
                      'rows': [
                          ['식후~수 시간', '혈당·간 글리코겐 분해'],
                          ['하루 안팎', '당신생(아미노산·젖산·글리세롤)'],
                          ['수 일 이상 금식', '지방산·케톤체(뇌는 케톤체)']]},
            'img': ('diagrams/fasting_fuel.png', '▲ 금식 진행에 따른 연료 전환'),
            'trap': '⚠ 함정 — 간이 케톤체를 "이용한다"고 낚는다(간은 SCOT가 없어 못 씀). 장기 금식의 뇌 주연료를 '
                    '포도당으로 낚지만 케톤체다.'},
        {
            'title': '해당작용(Glycolysis) — 조절효소와 젖산·아세틸CoA 분기', 'stars': '★★★ 기본 필수 · 조절단계 빈출',
            'core': [
                '해당작용은 <b>세포질</b>에서 포도당 1개를 피루브산 2개로 쪼개는 과정으로, 산소가 없어도 진행되어 '
                '순생성으로 <b>ATP 2개·NADH 2개</b>를 만든다.',
                '되돌릴 수 없는 3개 조절단계는 <b>헥소키나스(간에서는 글루코키나스)</b>, <b>포스포프룩토키나스-1(PFK-1)</b>, '
                '<b>피루브산키나스</b>이며, 이 중 PFK-1이 전체 속도를 정하는 <b>속도조절 효소</b>다.',
                'PFK-1은 <b>과당-2,6-2인산(F2,6BP)과 AMP로 활성화</b>되고 <b>ATP·시트르산으로 억제</b>되어, '
                '세포 에너지가 부족할 때 해당을 촉진하고 남을 때 멈춘다.',
                '무산소 조건에서는 피루브산이 젖산탈수소효소로 <b>젖산</b>이 되어 NAD+를 재생(적혈구·격한 운동)하고, '
                '유산소에서는 피루브산이 미토콘드리아로 들어가 <b>아세틸CoA</b>가 되어 TCA로 이어진다.',
                '포도당 1개를 완전 산화하면 해당 + 피루브산 산화 + TCA + 전자전달계를 합쳐 최신 계산으로 '
                '<b>약 30~32 ATP</b>가 나온다.'],
            'table': {'header': ['비가역 단계', '효소 / 조절'],
                      'rows': [
                          ['포도당 → G6P', '헥소키나스(간·인슐린은 글루코키나스 유도)'],
                          ['F6P → F1,6BP', 'PFK-1(속도조절): F2,6BP·AMP 활성 / ATP·시트르산 억제'],
                          ['PEP → 피루브산', '피루브산키나스(F1,6BP가 전방활성화)']]},
            'img': ('diagrams/glycolysis.png', '▲ 해당작용 모식도 — 3개 조절효소(★)와 피루브산의 젖산/아세틸CoA 분기'),
            'trap': '⚠ 함정 — 해당작용의 속도조절 효소를 헥소키나스로 낚는다(정답은 PFK-1). 무산소 해당에서 젖산을 '
                    '만드는 목적을 "ATP 생산"으로 낚지만, 실제 목적은 <b>NAD+ 재생</b>이라 해당이 계속 돌 수 있게 하는 것이다.'},
        {
            'title': 'TCA 회로 · 시트르산 셔틀 · 글루타민 유입', 'stars': '★★★ 5년(21·22·23·24·25)',
            'core': [
                'TCA 회로는 <b>미토콘드리아 기질</b>에서 아세틸CoA(2C)가 옥살아세트산(4C)과 합쳐 시트르산(6C)이 되며 '
                '시작하고, 두 번의 탈탄산으로 CO₂ 2개를 내보내며 다시 옥살아세트산으로 돌아온다.',
                '한 바퀴에 <b>NADH 3·FADH₂ 1·GTP 1</b>을 만들며(전자전달계까지 가면 약 10 ATP), GTP는 '
                '숙시닐CoA→숙신산 단계의 기질수준 인산화에서 나온다.',
                '속도조절은 <b>이소시트르산 탈수소효소</b>(및 α-케토글루타르산 탈수소효소)가 맡아, NADH·ATP가 많으면 '
                '억제되고 ADP·Ca2+가 많으면 촉진된다.',
                '에너지가 남으면 시트르산이 세포질로 나가(시트르산 셔틀) 아세틸CoA를 내놓아 <b>지방산 합성</b>의 재료가 되고, '
                '글루타민은 글루탐산을 거쳐 <b>알파케토글루타르산</b>으로 TCA를 보충(anaplerosis)한다(표지 글루타민은 '
                'α-케토글루타르산이 가장 먼저 표지됨).'],
            'table': {'header': ['항목', '한 바퀴 산출'],
                      'rows': [
                          ['탈탄산(CO₂)', '2개 (이소시트르산·α-KG 단계)'],
                          ['환원조효소', 'NADH 3 · FADH₂ 1'],
                          ['기질수준 인산화', 'GTP 1 (숙시닐CoA→숙신산)'],
                          ['전자전달 포함 ATP', '약 10 ATP']]},
            'img': ('diagrams/tca_energy.png', '▲ TCA 회로 모식도 — 각 단계에서 나오는 NADH·FADH2·GTP·CO2'),
            'trap': '⚠ 함정 — 속도조절 효소를 시트르산 합성효소로 낚는다(정답은 이소시트르산 탈수소효소). GTP 생성 '
                    '단계를 다른 단계로 낚거나, 글루타민의 TCA 진입점을 시트르산·옥살아세트산으로 낚는다(정답은 α-케토글루타르산).'},
        {
            'title': 'β-산화 ATP 계산', 'stars': '★★★ 3년(21·23·25)',
            'core': [
                '지방산은 카르니틴 셔틀로 미토콘드리아에 들어가 β-산화된다. 탄소 2개씩 잘려 아세틸CoA가 되고 회마다 '
                'FADH₂ 1·NADH 1이 나온다.',
                '탄소수 n인 포화지방산은 β-산화를 <b>(n/2 − 1)회</b> 하여 아세틸CoA <b>n/2개</b>를 만든다.',
                '팔미트산(C16) 예: 7회 β-산화 → 아세틸CoA 8 + FADH₂ 7 + NADH 7. ATP = 8×10 + 7×1.5 + 7×2.5 − 2(활성화) '
                '= <b>108</b>.'],
            'table': {'header': ['항목', '값(팔미트산 C16)'],
                      'rows': [
                          ['β-산화 횟수', '7회 (= 16/2 − 1)'],
                          ['생성물', '아세틸CoA 8 · FADH₂ 7 · NADH 7'],
                          ['ATP(P/O 최신)', '8×10 + 7×1.5 + 7×2.5 − 2 = 108']]},
            'img': None,
            'trap': '⚠ 함정 — 활성화에 쓴 ATP 2개(실제 2 고에너지결합)를 빼지 않거나, β-산화 횟수를 n/2로 낚는다'
                    '(정답은 n/2 − 1).'},
        {
            'title': '운동 시 에너지원(크레아틴인산)', 'stars': '★★★ 3년(22·23·25)',
            'core': [
                '운동 시간에 따라 주 연료가 바뀐다. 처음 수 초는 <b>크레아틴인산</b>이 ADP에 인산을 즉시 넘겨 ATP를 '
                '재생한다.',
                '이후 격렬한 무산소 구간에서는 <b>근 글리코겐의 무산소 해당</b>(젖산 생성)이, 지속 운동에서는 지방산 '
                '산화가 주가 된다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — "역기들기 같은 초단기"의 즉시 공급원을 포도당·지방산으로 낚는다(정답은 크레아틴인산).'},
    ]),
    ('Ⅱ. 산화스트레스 · 산소운반', [
        {
            'title': '글루타치온 · G6PD · 오탄당인산경로', 'stars': '★★★ 5년(21·22·23·24·25)',
            'core': [
                '오탄당인산경로(G6PD가 속도조절)는 <b>NADPH</b>를 만든다. NADPH는 산화된 글루타치온을 환원형으로 '
                '되돌려 세포를 활성산소로부터 지키고, 호중구의 산화폭발(NADPH 산화효소)에 쓰인다.',
                'G6PD가 결핍되면 NADPH가 부족해 환원글루타치온이 고갈되어, 잠두·감염·산화성 약물에서 <b>용혈</b>이 '
                '일어난다(하인츠소체).'],
            'table': None,
            'img': ('figures/2022_2_사진1.jpg', '▲ 호중구 산화폭발 — NADPH 산화효소 · 오탄당인산경로가 NADPH 공급 (2022 2교시)'),
            'trap': '⚠ 함정 — NADPH(합성·환원력)와 NADH(이화·ATP 생성)를 바꾼다. 글루타치온 재생에 쓰이는 것은 '
                    'NADPH다.'},
        {
            'title': '산소운반 — 2,3-BPG · 미오글로빈', 'stars': '★★★ 4년(21·22·24·25)',
            'core': [
                '2,3-BPG는 헤모글로빈의 탈산소형에 결합해 산소친화도를 낮춰 해리곡선을 <b>오른쪽으로 이동</b>시키고 '
                '조직에 산소를 더 내준다(저산소·빈혈·고지대에서 증가).',
                '2,3-BPG는 헤모글로빈 β사슬의 <b>양전하 라이신</b>과 염다리를 이루므로, 이 라이신이 전하 없는 '
                '메티오닌으로 바뀌면 2,3-BPG 결합이 약해져 오히려 산소친화도가 올라간다.',
                '미오글로빈은 단량체라 협조성이 없어 산소분압에만 반응하는 <b>쌍곡선</b>을, 헤모글로빈은 사량체라 '
                '협조성·pH·2,3-BPG·CO₂ 영향을 받는 <b>S자 곡선</b>을 그린다.'],
            'table': {'header': ['구분', '미오글로빈 vs 헤모글로빈'],
                      'rows': [
                          ['구조', '단량체 / 사량체'],
                          ['곡선', '쌍곡선(협조성 없음) / S자(협조성 있음)'],
                          ['조절인자', '산소분압만 / pH·2,3-BPG·CO₂도']]},
            'img': ('figures/2022_2_사진4.jpg', '▲ 라이신·메티오닌·2,3-BPG 구조 — 라이신 양전하가 2,3-BPG와 결합 (2022 2교시)'),
            'trap': '⚠ 함정 — 2,3-BPG 증가를 "좌측이동·친화도 증가"로 낚는다(실제는 우측이동·친화도 감소). '
                    '협조성은 헤모글로빈에만 있다.'},
    ]),
    ('Ⅲ. 아미노산 · 질소대사', [
        {
            'title': '요소회로 · 고암모니아혈증', 'stars': '★★★ 4년(21·22·24·25)',
            'core': [
                '요소회로는 미토콘드리아의 <b>카바모일인산 합성효소 I(CPS-I)</b>가 암모니아를 카바모일인산으로 바꾸며 '
                '시작되고, 이 효소는 <b>N-아세틸글루탐산</b>이 있어야 활성화된다(속도조절 단계).',
                '아르지닌은 회로 중간체(오르니틴)를 보충하고 N-아세틸글루탐산 생성을 도와, 요소회로 효소결핍의 '
                '고암모니아혈증 치료에 쓰인다.',
                '회로 순서: CPS-I → 오르니틴 → 시트룰린 → 아르지니노숙신산 → 아르지닌 → (아르지네이스) 요소 + 오르니틴.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — CPS-I의 알로스테릭 활성인자를 시트룰린·cAMP로 낚는다(정답은 N-아세틸글루탐산).'},
        {
            'title': '아미노산 pKa · 등전점 · 전기영동', 'stars': '★★★ 4년(21·22·23·25)',
            'core': [
                '등전점(pI)은 아미노산·단백질의 순전하가 0이 되는 pH이고, 그 pH에서는 전기장에서 이동하지 않는다.',
                '2차원 전기영동은 1차원에서 <b>등전점집중(pI 차이)</b>으로, 2차원에서 <b>SDS-PAGE(분자량 차이)</b>로 '
                '단백질을 점으로 분리한다.',
                '산성 아미노산(아스파트산·글루탐산)은 곁사슬 카복실기 때문에 pKa가 낮고 pI도 낮다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 2D 전기영동의 두 분리 기준을 "분자량 + 소수성"으로 낚는다(정답은 등전점 + 분자량).'},
        {
            'title': '페닐케톤뇨증(PKU)', 'stars': '★★★ 3년(22·23·24)',
            'core': [
                '페닐알라닌 수산화효소가 결핍되어 <b>페닐알라닌이 축적</b>(신경독성)되고 <b>티로신이 부족</b>해져 멜라닌·'
                '카테콜아민이 준다(밝은 피부).',
                '이 효소가 만드는 산물은 티로신이며, 저페닐알라닌 식이로 관리하고 <b>아스파탐(페닐알라닌 함유)은 금기</b>다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 결핍 효소의 산물을 페닐알라닌·멜라닌으로 낚는다(직접 산물은 티로신).'},
        {
            'title': '통풍 · 요산(퓨린 분해)', 'stars': '★★★ 3년(21·23·25)',
            'core': [
                '사람의 퓨린 분해 최종산물은 <b>요산</b>이며, 크산틴 → 요산 단계를 <b>크산틴 산화효소</b>가 담당한다'
                '(알로퓨리놀이 억제).',
                '요산나트륨 결정이 관절에 쌓이면 통풍이 되고, 결정은 편광에서 <b>바늘 모양·음성 복굴절</b>을 보인다.',
                '레시-나이한증후군(HGPRT 결핍)은 퓨린 재활용이 안 돼 요산이 과다 생성된다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 통풍 결정(요산염, 바늘·음성복굴절)과 가성통풍(칼슘피로인산, 마름모·양성복굴절)을 바꾼다.'},
    ]),
    ('Ⅳ. 지질 · 콜레스테롤', [
        {
            'title': '콜레스테롤 · 스타틴 · LCAT/HDL', 'stars': '★★★ 4년(21·22·23·25)',
            'core': [
                '콜레스테롤 합성의 속도조절 효소는 <b>HMG-CoA 환원효소</b>이고, 스타틴이 이를 억제하면 세포내 '
                '콜레스테롤이 줄어 간의 <b>LDL 수용체가 늘어</b> 혈중 LDL을 더 끌어들인다.',
                'LCAT는 HDL에서 콜레스테롤을 에스터화해 HDL 중심으로 채워 넣어 말초 콜레스테롤을 간으로 되돌린다'
                '(역수송). LCAT 결핍이면 이 과정이 막힌다.',
                '콜레스테롤은 스테로이드 고리 4개에 히드록실기와 곁사슬을 가진 양친매성 막 성분이자 스테로이드호르몬·'
                '담즙산·비타민 D의 전구체다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 스타틴 투여 시 LDL 수용체가 "감소"한다고 낚는다(실제는 증가). LCAT의 작용 부위를 '
                    'LDL로 낚는다(HDL이다).'},
        {
            'title': '지방산 — 합성·산화·명명', 'stars': '★★★ 3년(23·24·25)',
            'core': [
                '지방산 합성은 <b>세포질</b>에서 NADPH를 써서 일어나고, 아세틸CoA 카복실화효소(ACC)가 속도조절'
                '(말로닐CoA 생성)을 한다. β-산화는 <b>미토콘드리아</b>에서 일어난다.',
                '말로닐CoA는 카르니틴 셔틀(CPT-I)을 막아 지방산 합성과 산화가 동시에 일어나지 않게 한다.',
                '사람이 못 만드는 필수지방산은 리놀레산(ω-6)·α-리놀렌산(ω-3)이다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 합성(세포질·NADPH)과 산화(미토콘드리아·FADH₂/NADH)의 장소·조효소를 바꾼다.'},
        {
            'title': '인지질 · 폐 계면활성제(레시틴)', 'stars': '★★ 2년(21·25)',
            'core': [
                '인지질은 <b>글리세롤 + 지방산 2개 + 인산 + 머리기(콜린 등)</b>로 된 양친매성 분자로 세포막 이중층의 '
                '주성분이다.',
                '레시틴(다이팔미토일포스파티딜콜린)은 <b>2형 폐포세포</b>가 만드는 폐 계면활성제의 핵심으로 폐포 '
                '표면장력을 낮춰 허탈을 막는다.',
                '태아 폐성숙 지표로 양수 <b>L/S 비(레시틴/스핑고미엘린) ≥ 2</b>면 성숙으로 보며, 미숙아는 계면활성제 '
                '부족으로 신생아호흡곤란증후군이 온다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 계면활성제가 표면장력을 높인다고 낚거나(낮춤), 만드는 세포를 1형 폐포세포로 낚는다(2형).'},
    ]),
    ('Ⅴ. 분자생물학 · 세포주기', [
        {
            'title': 'RNA 간섭(siRNA · RISC)', 'stars': '★★★ 4년(21·22·23·24)',
            'core': [
                'siRNA는 <b>RNA유도침묵복합체(RISC)</b>에 실려 상보적 mRNA에 결합해 그 mRNA를 절단·분해함으로써 '
                '표적 단백 발현을 억제한다.',
                '파티시란처럼 특정 단백(트랜스타이레틴) 발현을 낮추는 치료제로 쓰이며, 작용 단계는 전사·번역이 아니라 '
                '<b>mRNA 분해</b>다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — siRNA의 작용을 전사 억제·단백질 분해로 낚는다(정답은 mRNA 분해).'},
        {
            'title': 'mRNA 가공(5′ 캡 · 스플라이싱)', 'stars': '★★★ 3년(21·22·23)',
            'core': [
                '진핵 mRNA는 5′ 말단에 <b>7-메틸구아노신 캡</b>, 3′ 말단에 <b>폴리A 꼬리</b>가 붙고 인트론이 잘려나가는 '
                '스플라이싱을 거친다.',
                '인트론의 5′ 말단은 거의 항상 <b>GU</b>, 3′ 말단은 <b>AG</b>가 스플라이싱 신호이므로, 인트론 5′ 공여부위 '
                '변이는 스플라이싱을 망가뜨린다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 인트론 5′ 공여부위(GU) 변이를 캡 형성·폴리A·RNA 편집 이상으로 낚는다(정답은 스플라이싱).'},
        {
            'title': '핵산 염기조성(Chargaff 법칙)', 'stars': '★★★ 3년(21·23·25)',
            'core': [
                '이중가닥 DNA에서는 <b>A = T, G = C</b>이므로 퓨린 합(A+G)과 피리미딘 합(T+C)이 같다.',
                '한 염기의 비율을 주면 상보 염기와 나머지를 계산할 수 있고, GC 함량이 높을수록 이중가닥이 안정하다'
                '(수소결합 3개).'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 단일가닥 RNA·비상보 상황에 Chargaff 등식을 그대로 적용하도록 낚는다(A=T·G=C는 '
                    '이중가닥 DNA 규칙).'},
        {
            'title': '세포주기 · 항암제 표적', 'stars': '★★★ 4년(22·23·24·25)',
            'core': [
                '세포주기는 G1 제한점에서 사이클린D-CDK4/6가 RB를 인산화해 E2F를 풀어 S기로 진입하며, p53은 손상 시 '
                '주기를 멈춘다.',
                '항암제는 작용 시기가 다르다. <b>S기</b>는 5-FU·메토트렉세이트(항대사), <b>M기</b>는 빈크리스틴·'
                '파클리탁셀(방추사)이 표적한다.',
                '유사분열 후기에는 후기촉진복합체(APC/C)가 <b>세큐린</b>을 분해해 자매염색분체를 분리한다.'],
            'table': None,
            'img': ('figures/2022_2_사진3.jpg', '▲ 유사분열 중기 — 염색체가 적도판에 정렬 (2022 2교시)'),
            'trap': '⚠ 함정 — 5-FU·MTX(S기)와 빈크리스틴·탁센(M기)의 작용 시기를 바꾼다. 중기(적도판 정렬)와 '
                    '후기(분리)를 혼동한다.'},
    ]),
    ('Ⅵ. 임상표지자 · 효소 · 신호', [
        {
            'title': '심근경색 표지자(트로포닌 · CK)', 'stars': '★★★ 3년(22·23·25)',
            'core': [
                '심장트로포닌(cTnI·cTnT)은 심장에 특이적이고 손상 4~6시간 뒤 올라 <b>3~10일 지속</b>되어 심근경색 진단·'
                '경과 판정의 표준이다.',
                'CK-MB는 조기에 오르지만 빨리 정상화되어 재경색 판정에 유용하다. 젖산탈수소효소는 비특이적이며 늦게 '
                '오른다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 오래 지속(수일)되는 특이 표지자를 CK-MB·LDH로 낚는다(정답은 트로포닌).'},
        {
            'title': '당화혈색소(HbA1c)', 'stars': '★★★ 3년(21·22·23)',
            'core': [
                '당화혈색소는 포도당이 헤모글로빈에 <b>비효소적으로</b> 붙은 것으로, 적혈구 수명(약 120일)에 걸친 '
                '<b>지난 2~3개월 평균 혈당</b>을 반영한다.',
                '조절 목표는 대개 6.5% 미만이며, 값이 높으면 그동안 혈당이 높았음을 뜻한다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 당화를 "효소 반응"으로 낚거나, HbA1c를 순간 혈당·합병증 지표로 해석한다(평균 혈당 지표).'},
        {
            'title': '효소 억제 · 동역학(경쟁적 vs 비경쟁적)', 'stars': '★★★ 3년(22·23·25)',
            'core': [
                '경쟁적 억제제는 활성부위를 두고 기질과 경쟁하므로 <b>Km은 커지고 Vmax는 그대로</b>이며, 기질 농도를 '
                '높이면 극복된다.',
                '비경쟁적 억제제는 다른 부위에 결합해 <b>Vmax를 낮추고</b> 기질로 극복되지 않는다.',
                'Km은 반응속도가 최대의 절반이 되는 기질 농도로, 효소-기질 친화도가 높을수록 작다.'],
            'table': {'header': ['구분', 'Km', 'Vmax', '기질로 극복'],
                      'rows': [
                          ['경쟁적 억제', '증가', '불변', '가능'],
                          ['비경쟁적 억제', '불변', '감소', '불가']]},
            'img': None,
            'trap': '⚠ 함정 — 경쟁적(Km↑·Vmax유지)과 비경쟁적(Vmax↓)의 지표를 바꾼다. "기질을 늘려 억제 완화"는 '
                    '경쟁적 억제다.'},
        {
            'title': '빈혈과 비타민(B12 · 철)', 'stars': '★★★ 3년(22·24·25)',
            'core': [
                '비타민 B12는 위 내인자와 결합해 <b>회장</b> 끝에서 흡수되며, 위·회장 수술이나 악성빈혈로 부족하면 '
                '거대적혈모구빈혈과 신경증상(아탈수초성)이 생긴다.',
                '철결핍빈혈은 소적혈구·저색소이며 페리틴·혈청철은 낮고 <b>총철결합능(TIBC)·트랜스페린은 증가</b>한다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 철결핍에서 TIBC가 "감소"한다고 낚는다(실제는 증가). B12 결핍(신경증상 동반)과 엽산 '
                    '결핍(신경증상 없음)을 혼동한다.'},
        {
            'title': '산화질소(NO) 신호', 'stars': '★★★ 3년(21·24·25)',
            'core': [
                '산화질소는 NO 합성효소가 <b>아르지닌</b>을 NO와 시트룰린으로 바꿔 만들며, 반감기가 짧아 주변분비로 '
                '이웃 평활근에 작용한다.',
                'NO는 구아닐산고리화효소를 켜 <b>cGMP</b>를 올려 혈관을 확장하고, 나이트로글리세린은 몸속에서 NO를 '
                '내놓아 협심증에 쓰인다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — NO의 이차전령을 cAMP·IP₃로 낚는다(정답은 cGMP). 전구 아미노산은 아르지닌이다.'},
        {
            'title': '당뇨병케토산증(DKA)', 'stars': '★★ 2년(22·23)',
            'core': [
                '인슐린이 크게 부족한 1형 당뇨(감염·인슐린 중단이 유발)에서 지방분해가 폭주해 간이 케톤체(아세토아세트산·'
                'β-히드록시뷰티르산)를 대량 만들어 <b>고음이온차 대사성 산증</b>이 생긴다.',
                '고혈당으로 삼투이뇨가 일어나 탈수·전해질 소실이 오고, 보상성 과호흡(쿠스마울 호흡)과 아세톤 냄새가 '
                '난다.',
                '치료는 수액·인슐린·칼륨 보충이며, 인슐린을 주면 칼륨이 세포로 들어가 <b>저칼륨혈증</b>에 주의한다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — DKA의 산증을 정상음이온차로 낚거나(고음이온차), 초기 혈청칼륨이 정상·상승이어도 몸 전체 '
                    '칼륨은 부족함을 놓친다.'},
    ]),
]

TIPS = [
    '에너지대사(전자전달·금식케톤·TCA·β산화)는 매년 여러 문항이 나오므로 경로의 위치(세포질/미토콘드리아)와 조효소를 함께 외운다.',
    '"짝 바꿔치기" 함정이 많다 — NADPH↔NADH, 합성↔산화, 경쟁적↔비경쟁적, 2,3-BPG 좌↔우 이동을 표로 대비한다.',
    '계산 문제(β-산화 ATP, 등전점, Chargaff)는 공식과 예제 한 개를 손으로 풀어 두면 변형돼도 풀린다.',
    '임상 연결(심근경색=트로포닌, PKU=아스파탐 금기, G6PD=잠두 용혈, 통풍=요산)은 키워드 한 개로 답이 갈린다.',
    '분자생물학은 "어느 단계"를 묻는다 — siRNA=mRNA 분해, 스플라이싱=인트론 GU-AG, 항암제 S기/M기를 구분한다.',
]


def build():
    doc = SimpleDocTemplate('학습노트_pdf/기종평_2교시_빈출유형_학습노트.pdf', pagesize=A4,
                            leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=14 * mm, bottomMargin=14 * mm)
    story = []
    story.append(Spacer(1, 40 * mm))
    story.append(P('기초의학종합평가 2교시', 'title'))
    story.append(P('빈출유형 학습노트 (생화학)', 'title'))
    story.append(Spacer(1, 6 * mm))
    story.append(P('2021 · 2022 · 2023 · 2024 · 2025 — 5개 연도 교차 분석', 'sub'))
    story.append(P('문제를 풀기 위해 필요한 핵심 개념 · 감별/계산 표 · 반복 오답 함정', 'sub'))
    story.append(Spacer(1, 10 * mm))
    story.append(P('★★★ = 3년 이상 출제(최빈출)  ·  ★★ = 2년(준빈출)  ·  괄호는 출제 연도', 'sub'))
    story.append(PageBreak())

    for sec_title, cards in SECTIONS:
        story.append(P(sec_title, 'sec'))
        for c in cards:
            core = c['core']
            story.append(KeepTogether([P(c['title'], 'card'), P(c['stars'], 'stars'),
                                       P('• ' + core[0], 'core')]))
            for line in core[1:]:
                story.append(P('• ' + line, 'core'))
            if c.get('table'):
                story.append(Spacer(1, 2 * mm))
                story.append(make_table(c['table']['header'], c['table']['rows']))
            if c.get('img'):
                story.append(make_img(c['img'][0], c['img'][1]))
            story.append(Spacer(1, 1.5 * mm))
            story.append(P(c['trap'], 'trap'))
            story.append(Spacer(1, 3 * mm))
            story.append(HRFlowable(width='100%', thickness=0.4,
                                    color=colors.HexColor('#d5dee6'), spaceAfter=3))

    story.append(P('시험 전략 TIP', 'sec'))
    for t in TIPS:
        story.append(P('• ' + t, 'tip'))

    doc.build(story)
    print('학습노트 생성 완료: 기종평_2교시_빈출유형_학습노트.pdf')


if __name__ == '__main__':
    build()
