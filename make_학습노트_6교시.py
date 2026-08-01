#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2021~2025 기종평 6교시(약리학) 빈출유형 학습노트 PDF 생성."""
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
    for a, b in (('₂', '2'), ('₁', '1'), ('₃', '3'), ('−', '-'), ('–', '-')):
        t = t.replace(a, b)
    t = t.replace('&', '&amp;')
    t = t.replace('<b>', '\x01').replace('</b>', '\x02')
    t = t.replace('<', '〈').replace('>', '〉')
    t = t.replace('\x01', '<b>').replace('\x02', '</b>')
    return t


def P(t, st):
    return Paragraph(esc(t), S[st])


def make_img(path, cap, max_w=80 * mm, max_h=95 * mm):
    iw, ih = PILImage.open(path).size
    s = min(max_w / iw, max_h / ih)
    img = RLImage(path, width=iw * s, height=ih * s)
    img.hAlign = 'CENTER'
    return KeepTogether([Spacer(1, 1 * mm), img, P(cap, 'cap')])


def header_widths(n):
    if n == 2: return [0.30, 0.70]
    if n == 3: return [0.22, 0.30, 0.48]
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
    ('Ⅰ. 약동학 (흡수·분포·대사·배설)', [
        {
            'title': '흡수 · 이온화 · 초회통과 · 생체이용률', 'stars': '★★★ 5년(21·23·24·25)',
            'core': [
                '약물은 <b>비이온형(지용성)</b>일 때 세포막을 잘 통과하며, 헨더슨-하셀바흐 식에 따라 약산은 산성 '
                '환경(위)에서, 약염기는 염기성 환경에서 비이온형이 늘어 흡수가 좋아진다.',
                '경구약은 장에서 흡수돼 <b>간문맥을 거치며 대사(초회통과효과)</b>되어 전신에 도달하는 양이 줄고, '
                '설하·직장·정맥은 이 초회통과를 피한다.',
                '생체이용률(F)은 투여량 중 전신순환에 도달한 비율로, <b>정맥주사는 F=1</b>이고 경구는 흡수·초회통과에 '
                '따라 낮아진다.',
                '나이트로글리세린을 설하로 주는 이유가 바로 큰 초회통과를 피하기 위해서다.'],
            'table': None,
            'img': ('diagrams/pk_curves.png', '▲ 혈중농도-시간곡선 — 정맥(F=1) vs 경구(초회통과), 치료역'),
            'trap': '⚠ 함정 — 초회통과를 신장 배설로 낚거나, 약염기가 산성 위에서 잘 흡수된다고 낚는다(이온화돼 흡수 '
                    '저하).'},
        {
            'title': '분포용적 · 부하/유지용량 · 항정상태', 'stars': '★★★ 5년(21·23·24·25)',
            'core': [
                '분포용적(Vd) = 총 약물량 ÷ 혈장농도이며, Vd가 크면 조직으로 많이 빠져나가 혈장농도가 낮다는 '
                '뜻이다.',
                '<b>부하용량 = 목표농도 × Vd</b>로 목표농도에 빨리 도달시키고, 유지용량 = 목표농도 × 청소율로 그 '
                '농도를 유지한다(생체이용률로 보정).',
                '반복 투여 시 약 <b>4~5 반감기</b>가 지나면 투여량과 제거량이 같아지는 항정상태에 도달한다.',
                '반감기는 소실을 결정하고, 청소율(clearance)은 단위시간에 약물이 제거되는 혈장 부피를 뜻한다.'],
            'table': {'header': ['개념', '공식/의미'],
                      'rows': [
                          ['분포용적 Vd', '총량 ÷ 혈장농도'],
                          ['부하용량', '목표농도 × Vd'],
                          ['유지용량', '목표농도 × 청소율 ÷ F'],
                          ['항정상태', '4~5 반감기 후 도달']]},
            'img': None,
            'trap': '⚠ 함정 — 부하용량 계산에 청소율을 쓰거나(Vd를 씀), 항정상태 도달을 1 반감기로 낚는다(4~5 '
                    '반감기).'},
        {
            'title': '약물대사 · CYP · 효소유도/억제 · 영차', 'stars': '★★★ 4년(22·23·24·25)',
            'core': [
                '대사는 1상(CYP450의 산화·환원·가수분해로 반응기 노출)과 2상(포합으로 수용성↑·배설)으로 나뉜다.',
                '<b>효소유도제(리팜핀·페니토인·카바마제핀·흡연)</b>는 CYP를 늘려 병용약 농도를 낮추고, '
                '<b>억제제(그레이프프루트·마크로라이드·아졸)</b>는 농도를 올려 독성을 유발한다.',
                '대부분 약물은 농도에 비례해 제거되는 <b>1차(선형) 약동학</b>이나, 에탄올·페니토인·아스피린(고용량)은 '
                '효소가 포화돼 일정량씩 제거되는 <b>0차 약동학</b>을 보인다.',
                '아세트아미노펜은 CYP2E1로 독성대사물(NAPQI)을 만들어 과량에서 간독성을 일으키며, N-아세틸시스테인이 '
                '해독제다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 효소유도가 병용약 농도를 "올린다"고 낚는다(내려 효과↓). 에탄올을 1차 약동학으로 '
                    '낚는다(0차).'},
    ]),
    ('Ⅱ. 약력학 (용량-반응 · 수용체)', [
        {
            'title': '용량-반응 · 효력 vs 효능 · 치료지수', 'stars': '★★★ 5년(21·22·23·24·25)',
            'core': [
                '<b>효력(potency)</b>은 같은 반응을 내는 데 필요한 용량(EC50이 작을수록 강함)이고, <b>효능(efficacy)</b>은 '
                '낼 수 있는 최대 반응(Emax)이다.',
                '치료지수(TI) = TD50 / ED50이며, 클수록 안전역이 넓다(디곡신·리튬·와파린은 TI가 좁아 혈중농도 감시가 '
                '필요하다).',
                '용량-반응곡선에서 왼쪽에 있을수록 효력이 크고, 위로 높을수록 효능이 크다.',
                '부분작용제는 최대효능이 완전작용제보다 낮고, 완전작용제가 함께 있으면 오히려 길항제처럼 작용한다'
                '(바레니클린).'],
            'table': None,
            'img': ('diagrams/therapeutic_index.png', '▲ 치료지수 = TD50 / ED50 (클수록 안전)'),
            'trap': '⚠ 함정 — 효력(potency)과 효능(efficacy)을 뒤바꾼다. 치료지수가 클수록 위험하다고 낚는다'
                    '(클수록 안전).'},
        {
            'title': '작용제 · 길항제 · 상승작용', 'stars': '★★★ 4년(21·22·24·25)',
            'core': [
                '<b>경쟁적 길항제</b>는 작용제와 같은 자리를 다퉈 용량-반응곡선을 오른쪽으로 밀지만(EC50↑) 용량을 '
                '늘리면 최대반응은 회복된다(극복 가능).',
                '<b>비경쟁적(불가역) 길항제</b>는 다른 자리에 붙거나 비가역 결합해 최대반응 자체를 낮춘다(Emax↓, '
                '극복 불가).',
                '생리적 길항은 서로 반대 작용을 하는 두 약이 다른 수용체로 상쇄되는 것(아나필락시스에서 히스타민 vs '
                '에피네프린)이다.',
                '여분수용체가 있으면 일부만 점유해도 최대반응이 나며, 상승작용은 합보다 큰 효과(1+1〉2)를 뜻한다.'],
            'table': {'header': ['길항 유형', '곡선 변화', '극복'],
                      'rows': [
                          ['경쟁적', 'EC50↑(우측이동)·Emax 유지', '가능(용량↑)'],
                          ['비경쟁/불가역', 'Emax↓', '불가'],
                          ['생리적', '반대작용 상쇄', '-']]},
            'img': ('diagrams/antagonist_curves.png', '▲ 경쟁적(우측이동) vs 비경쟁적(Emax 감소) 길항제'),
            'trap': '⚠ 함정 — 경쟁적 길항을 Emax 감소로 낚는다(우측이동·Emax 유지). 비경쟁적 길항을 용량으로 '
                    '극복한다고 낚는다(불가).'},
    ]),
    ('Ⅲ. 자율신경 약물', [
        {
            'title': '자율신경 수용체 개요', 'stars': '★★★ 5년(21·22·23·24·25)',
            'core': [
                '교감신경은 절후에서 <b>노르에피네프린</b>을, 부교감신경은 <b>아세틸콜린</b>을 내며 각각 아드레날린·'
                '콜린 수용체에 작용한다.',
                '<b>α1</b>은 혈관수축·산동·전립샘/방광목 수축(차단=프라조신·탐수로신), <b>β1</b>은 심박·수축력↑·레닌'
                '(차단=베타차단제), <b>β2</b>는 기관지·자궁 이완(작용=살부타몰·리토드린)을 맡는다.',
                '<b>M3</b>은 분비·평활근 수축·축동·조절수축(작용=필로카르핀), <b>M2</b>는 심박·전도를 늦춘다.',
                '콜린에스터분해효소 억제제(네오스티그민·도네페질)는 아세틸콜린을 늘려 중증근무력증·알츠하이머에 '
                '쓰이고, 유기인제 중독의 해독은 아트로핀·프랄리독심이다.'],
            'table': None,
            'img': ('diagrams/autonomic_receptors.png', '▲ 자율신경 수용체 지도 — 교감(α·β) vs 부교감(M·N)'),
            'trap': '⚠ 함정 — β2(기관지 확장)와 β1(심장)을 뒤바꾸거나, α1 차단의 부작용(기립저혈압)을 놓친다.'},
        {
            'title': '교감·부교감 작용약과 부작용', 'stars': '★★★ 4년(21·23·24·25)',
            'core': [
                '비선택 β차단제는 β2 차단으로 기관지수축·저혈당 은폐를 일으켜 천식·당뇨에서 주의하고, α1차단제는 '
                '첫 투여 시 <b>기립저혈압</b>을 잘 일으킨다.',
                '에피네프린은 아나필락시스의 1차 약으로 α1(혈관수축)·β1(심장)·β2(기관지확장)를 모두 자극한다.',
                '필로카르핀(M 작용제)은 섬모체근을 수축시켜 방수 유출을 늘려 <b>녹내장</b>을 치료한다.',
                '항무스카린제(스코폴라민)는 멀미에, 아트로핀은 서맥·유기인제 중독에 쓰인다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 아나필락시스 1차약을 항히스타민으로 낚는다(에피네프린). 녹내장에 산동제를 쓴다고 '
                    '낚는다(축동·유출↑).'},
    ]),
    ('Ⅳ. 중추신경 약물', [
        {
            'title': '항정신병약 · 추체외로(EPS) · 파킨슨', 'stars': '★★★ 5년(21·22·23·24·25)',
            'core': [
                '정형 항정신병약(할로페리돌)은 <b>도파민 D2 차단</b>으로 양성증상을 줄이지만 흑질선조체 차단으로 '
                '<b>추체외로증후군(EPS: 급성근긴장이상·좌불안석·파킨슨증·지연운동이상)</b>과 프로락틴 상승을 '
                '일으킨다.',
                '비정형 항정신병약(올란자핀·클로자핀)은 세로토닌·도파민을 함께 조절해 EPS가 적으나 대사증후군·'
                '체중증가가 문제다.',
                '메토클로프라미드도 D2 차단제라 제토 작용과 함께 추체외로 부작용을 낼 수 있다.',
                '파킨슨병은 도파민이 부족하므로 <b>레보도파</b>를 주며, 말초에서 도파민으로 바뀌지 않게 <b>카르비도파'
                '(말초 탈탄산효소 억제)</b>를 함께 쓴다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 파킨슨에 도파민 차단제를 쓴다고 낚거나(악화), 카르비도파가 중추로 들어간다고 낚는다'
                    '(말초 작용).'},
        {
            'title': '항우울(SSRI) · 세로토닌증후군 · 진정수면', 'stars': '★★★ 4년(22·23·24·25)',
            'core': [
                'SSRI는 시냅스에서 세로토닌 재흡수를 막아 우울·불안에 쓰이며 위장장애·성기능장애가 흔하고 효과가 '
                '수주 뒤 나타난다.',
                '여러 세로토닌 약을 병용하면 <b>세로토닌증후군(고열·발한·근경련·자율신경 항진)</b>이 생길 수 있다.',
                '벤조디아제핀·졸피뎀은 <b>GABA-A 수용체</b>에서 염소이온 통로 열림을 촉진해 진정·항불안·항경련 작용을 '
                '하며, 해독제는 플루마제닐이다.',
                '삼환계 항우울제는 항콜린·심독성 부작용과 과량 위험이 크다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 벤조디아제핀이 GABA를 직접 여는 작용제라고 낚는다(GABA 있어야 하는 양성 조절제). '
                    'SSRI 효과가 즉시 난다고 낚는다(수주 소요).'},
        {
            'title': '마취 — 흡입(MAC) · 국소 · 신경근차단', 'stars': '★★★ 5년(21·22·23·24·25)',
            'core': [
                '흡입마취제의 역가는 <b>MAC(최소폐포농도)</b>로 나타내며, MAC이 낮을수록 강력하다. 혈액용해도가 '
                '낮은 마취제가 유도·회복이 빠르다.',
                '국소마취제는 <b>전압의존 나트륨통로</b>를 막아 신경전도를 차단하며, 에피네프린을 섞으면 혈관수축으로 '
                '작용이 길어지고 전신흡수가 준다.',
                '탈분극성 신경근차단제(숙시닐콜린)는 지속 탈분극으로, 비탈분극성(로쿠로늄)은 경쟁적으로 아세틸콜린 '
                '수용체를 막아 근이완을 일으킨다.',
                '숙시닐콜린은 악성고열·고칼륨혈증 위험이 있다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — MAC이 높을수록 강력하다고 낚는다(낮을수록 강력). 국소마취 표적을 칼슘통로로 낚는다'
                    '(나트륨통로).'},
        {
            'title': '오피오이드 · 중독 · 금연', 'stars': '★★★ 4년(21·22·23·24)',
            'core': [
                '오피오이드는 μ수용체에 작용해 진통·호흡억제·변비·축동·의존을 일으키며, 과량은 <b>날록손</b>으로 '
                '역전한다.',
                '금단은 생명을 위협하진 않지만 심한 불쾌감을 주며, 메타돈·부프레노르핀으로 완화·유지치료를 한다.',
                '말초 오피오이드 길항제(메틸날트렉손)는 중추 진통은 유지하며 변비만 완화한다.',
                '금연에는 니코틴 부분작용제 <b>바레니클린</b>을 쓰며, 알코올 의존에는 디설피람(ALDH 억제로 홍조·불쾌)이 '
                '있다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 오피오이드 과량 해독제를 플루마제닐로 낚는다(날록손). 축동을 산동으로 낚는다(오피오이드는 '
                    '축동).'},
    ]),
    ('Ⅴ. 심혈관 · 혈액 · 소화기', [
        {
            'title': '강심배당체 · RAAS · 이뇨제', 'stars': '★★★ 4년(21·22·23·24·25)',
            'core': [
                '디곡신은 <b>Na/K-ATPase를 억제</b>해 세포내 칼슘을 늘려 수축력을 키우고 미주신경 자극으로 심박을 '
                '늦추며, 치료지수가 좁고 <b>저칼륨혈증에서 독성</b>이 커진다.',
                'ACE억제제(-프릴)는 안지오텐신 II 생성을 막아 혈압을 낮추고 신장을 보호하나 마른기침·고칼륨혈증·'
                '혈관부종을, ARB(-사르탄)는 기침이 적다.',
                '이뇨제는 작용 부위별로 나뉜다: 고리(푸로세미드)·티아지드는 칼륨을 잃고, 알도스테론길항제·아밀로라이드는 '
                '<b>칼륨을 보존</b>한다.',
                '아세타졸아미드(탄산탈수효소 억제)는 중탄산염 이뇨로 대사성 산증·녹내장에 쓰인다.'],
            'table': {'header': ['약', '기전', '주의'],
                      'rows': [
                          ['디곡신', 'Na/K-ATPase 억제', '저K혈증서 독성↑'],
                          ['ACE억제제', 'A-II 생성↓', '기침·고K·혈관부종'],
                          ['티아지드/고리', 'Na 재흡수↓', '저칼륨혈증'],
                          ['칼륨보존이뇨제', '알도스테론 길항', '고칼륨혈증']]},
            'img': None,
            'trap': '⚠ 함정 — 디곡신 독성을 고칼륨에서 낚는다(저칼륨에서 악화). 칼륨보존이뇨제를 저칼륨 위험으로 '
                    '낚는다(고칼륨).'},
        {
            'title': '항협심증(나이트로글리세린·PDE5) · 이상지질', 'stars': '★★★ 3년(22·23·25)',
            'core': [
                '나이트로글리세린은 <b>산화질소(NO)를 내어 cGMP를 올려</b> 혈관(특히 정맥)을 확장해 전부하를 줄여 '
                '협심증을 완화하며, 초회통과 때문에 설하로 준다.',
                'PDE-5 억제제(실데나필)는 cGMP 분해를 막아 혈관을 확장하며, <b>질산염과 함께 쓰면 심한 저혈압</b>이 '
                '생겨 금기다.',
                '스타틴은 HMG-CoA 환원효소를 억제해 LDL을 낮추고 간 LDL 수용체를 늘리며, 근병증·간효소 상승이 '
                '부작용이다.',
                '에제티미브는 장에서 콜레스테롤 흡수를 막아 스타틴과 병용한다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 나이트로글리세린과 PDE-5 억제제 병용을 안전하다고 낚는다(저혈압 금기). 스타틴 작용을 '
                    '흡수억제로 낚는다(합성억제; 흡수억제는 에제티미브).'},
        {
            'title': '항혈소판 · 항응고 · 해독제', 'stars': '★★★ 4년(21·22·24·25)',
            'core': [
                '아스피린은 <b>COX를 비가역적으로 아세틸화</b>해 트롬복산 A2 생성을 막아 혈소판 응집을 억제하며, '
                '혈소판은 새 효소를 못 만들어 효과가 수명 내내 간다.',
                '헤파린은 안티트롬빈을 활성화해 즉시 항응고하며 aPTT로 감시하고, 과량은 <b>프로타민</b>으로 역전한다.',
                '와파린은 비타민 K 의존 인자(II·VII·IX·X) 합성을 막아 며칠 뒤 효과가 나며 PT/INR로 감시하고, '
                '해독은 비타민 K다.',
                'P2Y12 억제제(클로피도그렐) 등도 항혈소판제로 쓰인다.'],
            'table': {'header': ['약', '기전', '해독/감시'],
                      'rows': [
                          ['아스피린', 'COX 비가역 억제', '-(혈소판 수명)'],
                          ['헤파린', '안티트롬빈 활성', '프로타민 / aPTT'],
                          ['와파린', '비타민K 인자↓', '비타민K / PT-INR']]},
            'img': None,
            'trap': '⚠ 함정 — 헤파린 해독제를 비타민K로 낚는다(프로타민). 아스피린의 COX 억제를 가역적으로 낚는다'
                    '(비가역).'},
        {
            'title': 'NSAID · COX · 아세트아미노펜 · 제토제', 'stars': '★★★ 4년(21·22·24·25)',
            'core': [
                'NSAID는 COX를 억제해 프로스타글란딘을 줄여 소염·진통·해열하지만, <b>COX-1 억제</b>로 위점막 '
                '손상·신장 부작용을 낸다.',
                'COX-2 선택억제제(세레콕시브)는 위장장애가 적으나 <b>혈전·심혈관 위험</b>이 있다.',
                '아세트아미노펜은 해열·진통은 있으나 말초 소염 작용이 약하고 위장장애가 적으며, 과량은 간독성을 '
                '일으킨다.',
                '제토제는 표적이 다르다: 온단세트론(5-HT3 차단, 항암 구토), 메토클로프라미드(D2 차단, 위장운동↑·EPS), '
                '스코폴라민(멀미).'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 아세트아미노펜을 강한 소염제로 낚는다(소염 약함). COX-2 선택제를 심혈관에 안전하다고 '
                    '낚는다(혈전 위험).'},
    ]),
    ('Ⅵ. 내분비 · 항감염 · 항암 · 임상시험', [
        {
            'title': '당뇨약 · 코르티코스테로이드 · 통풍', 'stars': '★★★ 4년(22·23·24·25)',
            'core': [
                '인슐린은 초속효·속효·중간형·지속형으로 나뉘고, 설포닐유레아는 β세포 KATP 통로를 닫아 인슐린 분비를 '
                '늘려 <b>저혈당</b> 위험이 있다.',
                '티아졸리딘디온(TZD)은 <b>PPARγ</b>를 자극해 인슐린 감수성을 높이고, 메트포민은 간 당신생을 줄인다.',
                '코르티코스테로이드는 강력한 소염·면역억제제로 장기 사용 시 쿠싱양 부작용·감염·골다공증이 생기고, '
                '<b>갑자기 끊으면 부신위기</b>가 오므로 서서히 감량한다.',
                '통풍은 급성기에 NSAID·콜히친을, 예방에 <b>알로퓨리놀(잔틴산화효소 억제)</b>을 쓴다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 코르티코스테로이드를 급중단해도 된다고 낚는다(부신위기). 알로퓨리놀을 급성 발작 즉시 '
                    '시작한다고 낚는다(급성기엔 오히려 악화 가능).'},
        {
            'title': '항생제 — 작용기전 · MRSA · 항결핵', 'stars': '★★★ 5년(21·22·23·24·25)',
            'core': [
                '베타락탐(페니실린·세팔로스포린)은 세포벽 합성(PBP)을 막고, 반코마이신도 세포벽을, 아미노글리코시드·'
                '마크로라이드는 리보솜(단백합성)을, 퀴놀론은 DNA 자이라제를 막는다.',
                'MRSA는 변형 PBP2a로 베타락탐에 듣지 않아 <b>반코마이신</b>으로 치료하고, 반코마이신 내성은 '
                'D-Ala-D-Lac 변형으로 생긴다.',
                '페니실린 알레르기(제I형)가 있으면 교차반응 적은 계열로 대체한다.',
                '항결핵제 이소니아지드는 <b>비타민 B6(피리독신) 결핍성 말초신경병</b>을 일으켜 B6를 함께 주고, '
                '리팜핀은 강력한 <b>CYP 유도제</b>이며 체액을 주황색으로 물들인다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — MRSA에 베타락탐을 쓴다고 낚는다(PBP2a 내성·반코마이신). 이소니아지드 부작용 보충을 '
                    'B12로 낚는다(B6).'},
        {
            'title': '항바이러스 · 항진균 · 항암제 내성', 'stars': '★★★ 4년(23·24·25)',
            'core': [
                '아시클로버는 바이러스 티미딘키나제로 활성화돼 헤르페스 DNA중합효소를 막고, 오셀타미비르는 '
                '인플루엔자 <b>뉴라미니다제</b>를 억제한다.',
                '아졸·암포테리신B는 진균 세포막 <b>에르고스테롤</b> 합성·기능을 표적으로 한다.',
                '항암제는 세포주기에 작용한다: 메토트렉세이트·5-FU는 S기 대사길항제, 빈크리스틴·탁센은 M기 방추사에 '
                '작용한다.',
                '항암제 내성의 주요 기전은 <b>다약제내성 유출펌프(P-당단백/MDR1)</b>가 약을 세포 밖으로 퍼내는 '
                '것이다.'],
            'table': None,
            'img': None,
            'trap': '⚠ 함정 — 오셀타미비르 표적을 DNA중합효소로 낚거나(뉴라미니다제), 항진균 표적을 콜레스테롤로 '
                    '낚는다(에르고스테롤).'},
        {
            'title': '임상시험 단계 · 윤리(IRB) · 위약', 'stars': '★★★ 5년(21·22·23·24·25)',
            'core': [
                '1상은 소수 <b>건강한 지원자</b>에서 안전성·약동학을, 2상은 소규모 환자에서 유효성·용량을, 3상은 '
                '대규모 환자에서 기존 치료와 비교(무작위·이중맹검)를 한 뒤 시판 후 4상으로 감시한다.',
                '임상시험은 <b>기관윤리심의위원회(IRB)</b> 승인과 충분한 설명 후 동의(피험자 자율성)를 거쳐야 한다.',
                '위약효과는 약효가 없는 처치에도 반응이 나는 현상으로, 이중맹검·위약대조로 통제한다.',
                '이상반응 중 예측 불가능한 <b>특이체질반응</b>은 용량과 무관하게 소수에서 나타난다.'],
            'table': {'header': ['상', '대상', '목적'],
                      'rows': [
                          ['1상', '건강한 지원자(소수)', '안전성·약동학'],
                          ['2상', '환자(소규모)', '유효성·용량'],
                          ['3상', '환자(대규모)', '비교·확증(RCT)'],
                          ['4상', '시판 후', '장기 감시']]},
            'img': None,
            'trap': '⚠ 함정 — 1상 대상을 환자로 낚는다(건강한 지원자). 특이체질반응을 용량의존으로 낚는다(용량 '
                    '무관).'},
    ]),
]

TIPS = [
    '약동학 계산은 공식을 손에 익힌다 — 부하용량=농도×Vd, 유지용량=농도×청소율, 항정=4~5 반감기, TI=TD50/ED50.',
    '수용체는 방향으로 외운다 — α1 수축·β1 심장·β2 확장, M3 분비·수축, MHC처럼 "짝"으로 대비한다.',
    '"뒤바꾸기" 함정 — 효력vs효능, 경쟁적vs비경쟁적, 소변이vs대변이, 초회통과, 디곡신은 저칼륨서 독성.',
    '약물 한 개당 대표 부작용·해독제를 붙여 외운다 — 헤파린=프로타민, 오피오이드=날록손, 아세트아미노펜=NAC, INH=B6.',
    '기전 표적을 정확히 — 나이트로글리세린 cGMP, 국소마취 Na통로, 오셀타미비르 뉴라미니다제, 알로퓨리놀 잔틴산화효소.',
]


def build():
    doc = SimpleDocTemplate('기종평_6교시_빈출유형_학습노트.pdf', pagesize=A4,
                            leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=14 * mm, bottomMargin=14 * mm)
    story = []
    story.append(Spacer(1, 40 * mm))
    story.append(P('기초의학종합평가 6교시', 'title'))
    story.append(P('빈출유형 학습노트 (약리학)', 'title'))
    story.append(Spacer(1, 6 * mm))
    story.append(P('2021 · 2022 · 2023 · 2024 · 2025 — 5개 연도 교차 분석', 'sub'))
    story.append(P('문제를 풀기 위해 필요한 핵심 개념 · 감별 표 · 모식도 · 반복 오답 함정', 'sub'))
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
    print('학습노트 생성 완료: 기종평_6교시_빈출유형_학습노트.pdf')


if __name__ == '__main__':
    build()
