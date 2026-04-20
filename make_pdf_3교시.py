#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('NanumGothic', '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'))
pdfmetrics.registerFont(TTFont('NanumGothicBold', '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'))

def make_styles():
    title_style = ParagraphStyle(
        'Title', fontName='NanumGothicBold', fontSize=16,
        textColor=colors.HexColor('#1a1a2e'), spaceAfter=6, spaceBefore=4,
        leading=22, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', fontName='NanumGothic', fontSize=10,
        textColor=colors.HexColor('#555555'), spaceAfter=12,
        leading=14, alignment=1
    )
    h1_style = ParagraphStyle(
        'H1', fontName='NanumGothicBold', fontSize=13,
        textColor=colors.HexColor('#16213e'), spaceAfter=6, spaceBefore=14,
        leading=18, borderPad=4
    )
    h2_style = ParagraphStyle(
        'H2', fontName='NanumGothicBold', fontSize=11,
        textColor=colors.HexColor('#0f3460'), spaceAfter=4, spaceBefore=10,
        leading=16
    )
    body_style = ParagraphStyle(
        'Body', fontName='NanumGothic', fontSize=9,
        textColor=colors.HexColor('#333333'), spaceAfter=3, spaceBefore=2,
        leading=14
    )
    bullet_style = ParagraphStyle(
        'Bullet', fontName='NanumGothic', fontSize=9,
        textColor=colors.HexColor('#333333'), spaceAfter=2, spaceBefore=1,
        leading=13, leftIndent=12, bulletIndent=0
    )
    small_style = ParagraphStyle(
        'Small', fontName='NanumGothic', fontSize=8,
        textColor=colors.HexColor('#666666'), spaceAfter=2,
        leading=12
    )
    note_style = ParagraphStyle(
        'Note', fontName='NanumGothic', fontSize=8.5,
        textColor=colors.HexColor('#555555'), spaceAfter=4, spaceBefore=4,
        leading=13, leftIndent=8
    )
    return {
        'title': title_style, 'subtitle': subtitle_style,
        'h1': h1_style, 'h2': h2_style, 'body': body_style,
        'bullet': bullet_style, 'small': small_style, 'note': note_style
    }

def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=18*mm, leftMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm
    )
    s = make_styles()
    story = []

    # ── 표지 ──────────────────────────────────────────────
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph('기초의학종합평가 (KAMC)', s['subtitle']))
    story.append(Paragraph('3교시 빈출 유형 분석', s['title']))
    story.append(Paragraph('2021 · 2023 · 2024 · 2025년도 | 과목: 생리학', s['subtitle']))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#0f3460')))
    story.append(Spacer(1, 6*mm))

    # ── 섹션 1: 최빈출 유형 ────────────────────────────────
    story.append(Paragraph('★★★ 최빈출 유형 (3~4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_items = [
        ('1', '1L 출혈 → 바소프레신 분비 증가',
         '2021·2024 (완전 동일 문구)',
         '40세 남자, 키 170 cm / 체중 70 kg, 약 1 L 혈액 소실 시 일어나는 생리적 변화\n'
         '→ 바소프레신(ADH) 분비 증가 ← 혈압↓·혈액량↓ 자극\n'
         '※ 레닌↑, 코티솔↑, 에피네프린↑도 모두 증가 — 오답 선지로 제시\n'
         '※ 심방나트륨이뇨펩타이드(ANP)는 감소 — 혈액량 감소 시 분비 줄어듦'),

        ('2', '위점막 D세포 손상 → 소마토스타틴 감소 → 위산분비 증가',
         '2021·2024 (완전 동일 문구)',
         '35세 남자, 공복 시 타는 듯한 속쓰림과 통증, 위산분비 증가 + D세포 손상 발견\n'
         '→ 소마토스타틴 분비 감소 → D세포가 손상되면 가스트린·HCl 억제 기능 소실\n'
         '※ GIP·가스트린·아세틸콜린·PGE2는 오답'),

        ('3', '산염기 균형 / ABG 해석',
         '2021·2023·2024·2025 (4년 전부)',
         'pH↓ + PCO2↑ → 호흡산증 / pH↓ + HCO3-↓ → 대사성산증\n'
         '음이온 차이 = Na+ − (Cl- + HCO3-) → 정상 12 mEq/L\n'
         'A-a gradient = PAO2 − PaO2 (정상 <15 mmHg)\n'
         '→ 2021: 호흡산증(PCO2 73) / 2024: DKA 급성 대사성산증 / 2025: A-a gradient 50 mmHg, 환기-관류 불균형\n'
         '※ PAO2 = (760−47)×FiO2 − PaCO2/0.8 공식 암기 필수'),

        ('4', 'ADH(바소프레신) 분비 조건',
         '2021·2023·2025',
         '분비 촉진: 혈장 삼투압↑, 혈압↓, 혈액량↓, 안지오텐신II↑\n'
         '분비 억제: 혈장 삼투압↓, 가슴안 혈액량 증가, 알코올\n'
         '→ 2021: 분비 감소 조건 = 가슴안 혈액량 증가\n'
         '→ 2023: 분비 촉진 조건 = 안지오텐신II 증가\n'
         '※ 집합관 수분 재흡수 → 소변 농축 → 삼투압 정상화'),

        ('5', 'CO2 운반 주요 형태 = 적혈구 내 HCO3-',
         '2023·2024 (동일)',
         '조직 → 폐로 운반되는 CO2의 약 70%는 적혈구 내 HCO3- 형태\n'
         '순서: CO2 → 적혈구 유입 → carbonic anhydrase → H2CO3 → H+ + HCO3-\n'
         '→ HCO3- 혈장으로 방출 (Cl- shift), H+는 Hb와 결합\n'
         '※ 혈장 HCO3-(~23%), 카바미노화합물(~7%)은 오답으로 제시'),

        ('6', '나이 증가 → 맥박압 증가 = 혈관 순응도(신전성) 감소',
         '2021·2023',
         '혈관이 딱딱해질수록(순응도↓) → 수축기혈압↑, 이완기혈압 불변 → 맥박압↑\n'
         '→ 동맥경화, 노화로 대동맥 탄성↓\n'
         '※ 2021: 맥박압 그래프에서 혈관 순응도 감소 선택\n'
         '※ 2023: 혈관 신전성 감소 → 맥압 증가'),

        ('7', 'EEG 뇌파 특징',
         '2021·2024',
         '알파파(8~13 Hz): 눈 감은 안정 상태 → 눈 뜨면 베타파로 전환\n'
         '베타파(13~30 Hz): 각성·집중·눈 뜸\n'
         '델타파(<4 Hz): 깊은 수면, 진폭 가장 큼\n'
         '세타파(4~8 Hz): 졸음·얕은 수면\n'
         '※ 2021: 눈 감음=알파파, 눈 뜸=베타파 선택 문제\n'
         '※ 2024: 델타파 특징 = 깊은 수면, 진폭 가장 큼'),

        ('8', '폐경 → FSH 분비 증가',
         '2021·2023',
         '난소 노화 → 정상 난포 수 감소 → 에스트로겐↓ → 음성되먹임 감소\n'
         '→ FSH·LH 분비 증가 (뇌하수체 전엽)\n'
         '→ 2021: 45세 여자 FSH 60 mIU/mL↑, 에스트라디올↓ → 정상 난포 수 감소\n'
         '→ 2023: 60세 여자 골다공증 → FSH 분비 증가\n'
         '※ 에스트로겐 감소 → 골다공증, 혈관운동증상(안면홍조) 연결'),
    ]

    for no, title, years, desc in top_items:
        row_data = [[
            Paragraph(f'<b>{no}.</b>', s['body']),
            Paragraph(f'<b>{title}</b>', s['h2']),
            Paragraph(years, s['small'])
        ]]
        t = Table(row_data, colWidths=[8*mm, 110*mm, 46*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f0fe')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#c0c8e0')),
        ]))
        story.append(t)
        for line in desc.split('\n'):
            story.append(Paragraph('• ' + line if not line.startswith('※') and not line.startswith('→') else line, s['bullet']))
        story.append(Spacer(1, 2*mm))

    # ── 섹션 2: 준빈출 유형 ────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('★★ 준빈출 유형 (2년 이상 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    table_header = ['유형', '핵심 포인트', '출제연도']
    table_data = [table_header] + [
        ['SGLT2 기능 / 억제제',
         '신장 근위세관에서 포도당 재흡수 촉진\n억제제 → 포도당 재흡수 억제 → 당뇨 치료',
         '2023, 2025'],
        ['중증근무력증(MG)',
         '아세틸콜린 + 니코틴수용체 자가항체\n치료: 콜린에스터라제 억제제 투여',
         '2023, 2024'],
        ['글루카곤 작용',
         '간의 당신생(gluconeogenesis) 촉진\n※ 근육 당신생 X / 지방분해↑ / 간 단백합성 X',
         '2023, 2024'],
        ['PAG 통증 억제',
         '수도관주위회색질(PAG) 자극 → 내인성 오피오이드\n척수후각 substantia gelatinosa 연결',
         '2024, 2025'],
        ['시상하부 체온조절',
         '앞쪽 = 방열(발한·혈관확장) / 뒤쪽 = 발열(떨림·혈관수축·갈색지방)\n체온↓ → 갈색지방 대사 촉진·골격근 떨림',
         '2024, 2025'],
        ['글루코코르티코이드 작용',
         '간 당신생↑ / 염증반응 억제 / 단백분해↑(근육위축)\n골격근 포도당흡수↓ / 지방재분포(복부·얼굴)',
         '2024, 2025'],
        ['Frank-Starling 법칙',
         '전부하(중심정맥압)↑ → 이완기말 용적↑ → 일회박출량 증가\n심박출량곡선 상방이동 = 심근수축력 증가',
         '2024, 2025'],
        ['시각 — 암순응 / 시각색소',
         '암순응 핵심 = 시각색소 활성과 변성\n비타민A 결핍 → 11-cis-retinal 감소 → 야맹증',
         '2023, 2025'],
        ['내이 청각',
         '소리 증폭 가장 큰 곳 = 이소골(ossicles)\n소리 크기(세기) 감지 = 기저막 진폭 증가',
         '2023, 2024'],
        ['심전도(ECG) 이상',
         '방실결절 이상(2023) / 좌심실 재분극 지연 = QT 연장(2024)\n심전도 사진 제시 후 이상 부위 식별',
         '2023, 2024'],
        ['혈액응고',
         '트롬빈 ↔ 응고인자V 양성되먹임(2021)\n응고 순서: 조직인자→프로트롬빈분해효소→트롬빈→피브리노겐→피브린(2023)',
         '2021, 2023'],
        ['바닥핵 회로',
         '파킨슨: 흑질(substantia nigra) 도파민↓ → 그림에서 부위 식별(2021)\n헌팅턴: 줄무늬체 위축 → 간접회로 억제 감소 → 과운동(2025)',
         '2021, 2025'],
        ['혈색소 산소해리곡선 이동',
         '오른쪽 이동(P50↑): 젖산·CO2↑·체온↑·2,3-BPG↑ → 조직 O2 방출↑\n왼쪽 이동: 과호흡·알칼리증 → 산소 결합능 증가',
         '2023, 2025'],
        ['GLP-1 인크레틴 효과',
         '구강 포도당 > 정맥 포도당 시 인슐린 반응 현저히 큼\n매개물질 = 글루카곤유사펩티드-1(GLP-1)',
         '2024'],
    ]

    col_w = [50*mm, 90*mm, 26*mm]
    t2 = Table(table_data, colWidths=col_w, repeatRows=1)
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'NanumGothicBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'NanumGothic'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f4f6fb')]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c0c8e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)

    # ── 섹션 3: 주제별 핵심 포인트 요약 ───────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('주제별 핵심 포인트 요약', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    sections = [
        ('신경생리', [
            'EEG: 알파파(눈감음·안정) → 베타파(눈뜸·각성) / 델타파(깊은수면, 진폭 최대)',
            '바닥핵: 파킨슨=흑질 도파민↓ / 헌팅턴=줄무늬체↓→간접회로 억제↓→과운동',
            '소뇌 손상: 협동운동소실(ataxia), 측정과대(past-pointing)',
            '통증 억제: PAG → 내인성 오피오이드 / substantia gelatinosa 경유',
            'Nernst 평형전위: 농도경사에 의해 결정 (투과성과 무관)',
        ]),
        ('심장·순환생리', [
            'Frank-Starling: 전부하(중심정맥압·이완기말 용적)↑ → 일회박출량 증가',
            '나이 → 혈관 순응도↓ → 수축기혈압↑ → 맥박압 증가',
            '심전도: 방실결절 이상(PR 연장) / QT 연장=좌심실 재분극 지연',
            'ACE억제제: 안지오텐신II↓ → 혈관이완 → 후부하 감소',
            '혈액응고: 조직인자→프로트롬빈분해효소→트롬빈(양성되먹임)→피브린',
        ]),
        ('호흡생리', [
            'CO2 운반: 적혈구 내 HCO3-(~70%) > 혈장 HCO3- > 카바미노화합물',
            '산염기: pH↓+PCO2↑=호흡산증 / pH↓+HCO3-↓=대사성산증 / 음이온차이=Na-(Cl+HCO3)=정상12',
            'A-a gradient = PAO2-PaO2 (정상<15) / 상승 시 폐내 이상',
            'COPD + 산소치료 → 호흡저하: 말초화학수용체 PO2↑ 감지 → 저산소 구동 소실',
            '맥박산소측정기: 고지대 주민 = 적혈구용적률↑, PO2↓, 동맥혈산소함량 변화없음',
        ]),
        ('신장·체액생리', [
            'SGLT2: 근위세관 포도당 재흡수 / 억제제=2형 당뇨 치료',
            'ADH 촉진: 삼투압↑·혈압↓·혈액량↓·안지오텐신II↑ / 억제: 가슴안 혈액량↑',
            '자유수분청소율 = V - Cosm (Cosm=UOsm×V/POsm) / 음수=농축뇨',
            '삼투압 계산: 총삼투질 변화량 / 총체액 변화량',
            '중탄산염 재흡수: 근위세관(~80%) > 헨레고리 > 원위·집합세관',
        ]),
        ('내분비·소화생리', [
            '1L 출혈: ADH↑·레닌↑·코티솔↑·에피네프린↑ / ANP↓',
            '위산 분비: D세포→소마토스타틴 억제 / 가스트린·ACh·히스타민 자극',
            '글루카곤: 간 당신생↑·간 글리코겐분해↑·지방분해↑ / 근육 당신생 X',
            '글루코코르티코이드: 간 당신생↑·염증억제·단백분해↑·지방재분포',
            '폐경: 난포수↓→에스트로겐↓→FSH·LH↑(음성되먹임 소실)→골다공증',
            'GLP-1: 구강섭취 시 장에서 분비 → 인슐린↑ (인크레틴 효과)',
        ]),
        ('특수감각', [
            '시각: 암순응=시각색소 활성·변성 / 비타민A 결핍=11-cis-retinal↓=야맹증',
            '청각: 소리 증폭 최대=이소골 / 소리 크기=기저막 진폭 증가 / 소리 높낮이=기저막 위치',
            '혈색소 산소해리곡선: 우측이동(젖산·CO2·체온·2,3-BPG↑)=조직 O2방출↑',
            '전정기관: 오른쪽 회전 → 오른쪽 팽대능선 탈분극',
        ]),
    ]

    for sec_title, bullets in sections:
        story.append(Paragraph(sec_title, s['h2']))
        for b in bullets:
            story.append(Paragraph('• ' + b, s['bullet']))
        story.append(Spacer(1, 2*mm))

    # ── 섹션 4: 연도별 출제 현황표 ────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('연도별 출제 현황 요약표', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    yearly_header = ['주제', '2021', '2023', '2024', '2025']
    yearly_data = [yearly_header] + [
        ['1L 출혈 → 바소프레신 분비 증가', '○', '-', '○', '-'],
        ['D세포 → 소마토스타틴 감소 → 위산↑', '○', '-', '○', '-'],
        ['산염기/ABG 해석', '○', '○', '○', '○'],
        ['ADH 분비 조건', '○', '○', '-', '○'],
        ['CO2 운반 = 적혈구 내 HCO3-', '-', '○', '○', '-'],
        ['맥박압 = 혈관 순응도 감소', '○', '○', '-', '-'],
        ['EEG 뇌파 특징', '○', '-', '○', '-'],
        ['폐경 → FSH 분비 증가', '○', '○', '-', '-'],
        ['SGLT2 기능/억제제', '-', '○', '-', '○'],
        ['중증근무력증(MG)', '-', '○', '○', '-'],
        ['글루카곤 — 간의 당신생 촉진', '-', '○', '○', '-'],
        ['PAG 통증 억제 (내인성 오피오이드)', '-', '-', '○', '○'],
        ['시상하부 체온조절 중추', '-', '-', '○', '○'],
        ['글루코코르티코이드 작용', '-', '-', '○', '○'],
        ['Frank-Starling 법칙', '-', '-', '○', '○'],
        ['시각 (암순응 / 비타민A)', '-', '○', '-', '○'],
        ['내이 청각 (이소골 / 기저막)', '-', '○', '○', '-'],
        ['심전도 이상', '-', '○', '○', '-'],
        ['혈액응고', '○', '○', '-', '-'],
        ['바닥핵 회로 (파킨슨/헌팅턴)', '○', '-', '-', '○'],
        ['혈색소 산소해리곡선 이동', '-', '○', '-', '○'],
        ['폐기능 / 환기 관련', '○', '○', '○', '○'],
        ['GLP-1 인크레틴 효과', '-', '-', '○', '-'],
        ['SNARE 단백질 (시냅스 소포)', '-', '-', '○', '-'],
        ['자유수분청소율 / 삼투압 계산', '-', '-', '-', '○'],
    ]

    col_w2 = [82*mm, 18*mm, 18*mm, 18*mm, 18*mm]
    t3 = Table(yearly_data, colWidths=col_w2, repeatRows=1)

    cell_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'NanumGothicBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('FONTNAME', (0, 1), (-1, -1), 'NanumGothic'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f4f6fb')]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c0c8e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]

    for row_idx in range(1, len(yearly_data)):
        for col_idx in range(1, 5):
            if yearly_data[row_idx][col_idx] == '○':
                cell_styles.append(
                    ('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx),
                     colors.HexColor('#d4edda'))
                )

    t3.setStyle(TableStyle(cell_styles))
    story.append(t3)

    # ── 섹션 5: 시험 전략 ──────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#0f3460')))
    tip_data = [[
        Paragraph('<b>시험 전략 TIP</b>', s['h2']),
        Paragraph(
            '① "40세 남자 키170/70kg 1L 출혈"과 "35세 남자 공복 속쓰림 D세포 손상"은 '
            '2021·2024년에 완전히 동일한 문구로 반복 출제됩니다. 정답(바소프레신 증가 / 소마토스타틴 감소)을 반드시 암기하십시오. '
            '② 산염기/ABG 해석은 4년 연속 출제됩니다. pH·PCO2·HCO3- 삼각형과 음이온 차이(정상 12) 공식을 숙지하십시오. '
            '③ 2024·2025년에는 PAG 통증억제·시상하부 체온조절·글루코코르티코이드·Frank-Starling이 집중 출제되었습니다. '
            '④ CO2 운반(적혈구 HCO3-)·SGLT2·MG·글루카곤 당신생은 2년 연속 동일 주제로 반복됩니다.',
            s['note']
        )
    ]]
    tip_t = Table(tip_data, colWidths=[28*mm, 136*mm])
    tip_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff8e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#f9a825')),
    ]))
    story.append(tip_t)

    doc.build(story)
    print(f'PDF 생성 완료: {output_path}')

if __name__ == '__main__':
    build_pdf('/home/user/Gjp/기종평_3교시_빈출유형_분석.pdf')
