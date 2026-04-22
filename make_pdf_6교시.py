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
    return {
        'title': ParagraphStyle(
            'Title', fontName='NanumGothicBold', fontSize=16,
            textColor=colors.HexColor('#1a1a2e'), spaceAfter=6, spaceBefore=4,
            leading=22, alignment=1
        ),
        'subtitle': ParagraphStyle(
            'Subtitle', fontName='NanumGothic', fontSize=10,
            textColor=colors.HexColor('#555555'), spaceAfter=12,
            leading=14, alignment=1
        ),
        'h1': ParagraphStyle(
            'H1', fontName='NanumGothicBold', fontSize=13,
            textColor=colors.HexColor('#16213e'), spaceAfter=6, spaceBefore=14,
            leading=18
        ),
        'h2': ParagraphStyle(
            'H2', fontName='NanumGothicBold', fontSize=11,
            textColor=colors.HexColor('#0f3460'), spaceAfter=4, spaceBefore=10,
            leading=16
        ),
        'body': ParagraphStyle(
            'Body', fontName='NanumGothic', fontSize=9,
            textColor=colors.HexColor('#333333'), spaceAfter=3, spaceBefore=2,
            leading=14
        ),
        'bullet': ParagraphStyle(
            'Bullet', fontName='NanumGothic', fontSize=9,
            textColor=colors.HexColor('#333333'), spaceAfter=2, spaceBefore=1,
            leading=13, leftIndent=12
        ),
        'small': ParagraphStyle(
            'Small', fontName='NanumGothic', fontSize=8,
            textColor=colors.HexColor('#666666'), spaceAfter=2, leading=12
        ),
        'note': ParagraphStyle(
            'Note', fontName='NanumGothic', fontSize=8.5,
            textColor=colors.HexColor('#555555'), spaceAfter=4, spaceBefore=4,
            leading=13, leftIndent=8
        ),
    }


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=18*mm, leftMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm
    )
    s = make_styles()
    story = []

    # ── 표지 ──────────────────────────────────────────────
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph('기초의학종합평가 (KAMC)', s['subtitle']))
    story.append(Paragraph('6교시 빈출 유형 분석', s['title']))
    story.append(Paragraph('2021 · 2023 · 2024 · 2025년도', s['subtitle']))
    story.append(Paragraph('약리학', s['subtitle']))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#0f3460')))
    story.append(Spacer(1, 6*mm))

    # ── 섹션 1: ★★★ 최빈출 — 임상시험 단계 + 약동학 기초 ─────
    story.append(Paragraph('★★★ 최빈출 유형 — 임상시험 단계 · 약동학 기초 (4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_pk = [
        ('1', '임상시험 단계 구분',
         '2021·2023·2024·2025 (4년)',
         '전임상: 동물실험 — 독성·약동학 확인\n'
         '1상: 건강한 자원자 소수 — 안전성·약동학 (반복투여 포함)\n'
         '2상: 소수 환자 대상 — 유효성 확인, 적정 용량 결정\n'
         '3상: 다수 환자 — 효능 확증, 이중맹검 무작위 대조시험\n'
         '4상: 시판 후 조사 — 장기 안전성·희귀 부작용 확인\n'
         '※ "건강인 2주 반복 + 안전성" = 1상 / "소수 환자 + 유효 용량 결정" = 2상'),

        ('2', 'PK 기초 — 분포용적·반감기·부하용량·항정상태',
         '2021·2023·2024·2025 (4년)',
         '분포용적(Vd): IV bolus 후 y절편(C₀) → Vd = Dose / C₀\n'
         '반감기(t½): 1차 약동학 → t½ = 0.693/k (농도 절반 시간)\n'
         '부하용량(LD): LD = Vd × Css (빠른 효과 원할 때)\n'
         '항정상태 농도(Css): Css = (F × 용량) / (CL × 투여간격)\n'
         '→ 용량 2배 → Css 2배, 반감기는 불변 (1차 약동학)\n'
         '0차 약동학: 알코올 — 일정 속도로 대사, 농도-시간 그래프 직선\n'
         '경피패치: 일정한 혈중 농도 plateau curve\n'
         '※ 분포용적 계산 = y절편 사용 (x절편·기울기 아님)'),

        ('3', '약물 이온화 — Henderson-Hasselbalch',
         '2023·2024·2025 (3년)',
         '약산성 약물: 위장(산성, pH 1~2) → 비이온화↑ → 흡수 유리\n'
         '약염기성 약물: 소장(염기성, pH 7~8) → 비이온화↑ → 흡수\n'
         'pKa = pH일 때 → 이온화:비이온화 = 50:50\n'
         '약산 기준: [이온화]/[비이온화] = 10^(pH − pKa)\n'
         '→ pKa 3.4 약산, 혈장 pH 7.4: 10^(7.4−3.4) = 10,000:1 (이온화:비이온화)\n'
         '흡수 형태 = 항상 비이온화형 (지용성↑ → 막 통과)\n'
         '※ pKa가 낮을수록 강산, 흡수되는 형태는 언제나 비이온화형'),
    ]

    for no, title, years, desc in top_pk:
        row = [[
            Paragraph(f'<b>{no}.</b>', s['body']),
            Paragraph(f'<b>{title}</b>', s['h2']),
            Paragraph(years, s['small'])
        ]]
        t = Table(row, colWidths=[8*mm, 110*mm, 46*mm])
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
            story.append(Paragraph(
                '• ' + line if not line.startswith('※') else line,
                s['bullet']
            ))
        story.append(Spacer(1, 2*mm))

    # ── 섹션 2: ★★★ 최빈출 — 용량-반응 곡선 / 길항제 ──────────
    story.append(PageBreak())
    story.append(Paragraph('★★★ 최빈출 유형 — 용량-반응 곡선 · 길항제 · 치료지수 (4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_pd = [
        ('4', '경쟁적 vs 비경쟁적 길항제',
         '2021·2023·2024·2025 (4년)',
         '경쟁적 길항제: EC50 우측 이동(증가), Emax 불변 → 고농도 작용제로 극복 가능\n'
         '비경쟁적 길항제: Emax 감소, EC50 불변 (또는 약간 우측 이동) → 극복 불가\n'
         '부분작용제: Emax 낮음 — 단독 투여 시 일부 효과, 완전작용제와 경쟁 시 길항\n'
         '역작용제(inverse agonist): 기저 활성도 감소 (항히스타민제 일부)\n'
         '※ 경쟁적 = Emax 그대로 (가장 자주 혼동), 비경쟁적 = Emax 감소'),

        ('5', '효력(potency) vs 효능(efficacy) · 치료지수',
         '2021·2023·2024·2025 (4년)',
         '효력(potency): EC50 낮을수록 높음 (Ki 낮을수록 = 수용체 친화도↑)\n'
         '효능(efficacy): Emax 클수록 높음 — 최대 가능 효과\n'
         '치료지수(TI): TI = TD50 / ED50 → 높을수록 안전한 약물\n'
         'Hill\'s coefficient: 농도-반응 S자 가파를수록 큼 (EC10–EC90 간격 좁을수록)\n'
         'pA2: 경쟁적 길항제 효력 지표 — 2배 작용제 농도가 필요할 때의 길항제 농도(-log)\n'
         '※ 효력 ≠ 효능 — EC50 낮아도 Emax 낮으면 좋은 약 아님'),

        ('6', 'BZD vs 바르비투르산염 — GABAA 수용체 조절',
         '2025 (1년, 신유형)',
         'GABAA 수용체: Cl⁻ 통로 — GABA 결합 시 과분극 → 신경 억제\n'
         'Benzodiazepine(midazolam): GABA의 EC50 감소 → 곡선 좌측 이동, Emax 불변\n'
         '→ GABA 빈도(frequency) 증가 조절자 (양성 allosteric 조절)\n'
         'Barbiturate(pentobarbital): Emax 증가 → 곡선 위로 이동, EC50 불변\n'
         '→ GABA 지속시간(duration) 증가 조절자\n'
         '※ BZD = EC50 감소(친화도↑), Barbiturate = Emax 증가 — 혼동 주의'),
    ]

    for no, title, years, desc in top_pd:
        row = [[
            Paragraph(f'<b>{no}.</b>', s['body']),
            Paragraph(f'<b>{title}</b>', s['h2']),
            Paragraph(years, s['small'])
        ]]
        t = Table(row, colWidths=[8*mm, 110*mm, 46*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fff3e0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#ffcc80')),
        ]))
        story.append(t)
        for line in desc.split('\n'):
            story.append(Paragraph(
                '• ' + line if not line.startswith('※') else line,
                s['bullet']
            ))
        story.append(Spacer(1, 2*mm))

    doc.build(story)
    print(f'PDF 생성 완료: {output_path}')


if __name__ == '__main__':
    build_pdf('/home/user/Gjp/기종평_6교시_빈출유형_분석.pdf')
