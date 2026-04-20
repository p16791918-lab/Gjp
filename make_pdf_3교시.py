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

    doc.build(story)
    print(f'PDF 생성 완료 (1단계): {output_path}')

if __name__ == '__main__':
    build_pdf('/home/user/Gjp/기종평_3교시_빈출유형_분석.pdf')
