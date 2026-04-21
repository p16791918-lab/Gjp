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

pdfmetrics.registerFont(TTFont('NanumGothic', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
pdfmetrics.registerFont(TTFont('NanumGothicBold', '/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'))

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
    story.append(Paragraph('4교시 빈출 유형 분석', s['title']))
    story.append(Paragraph('2021 · 2023 · 2024 · 2025년도', s['subtitle']))
    story.append(Paragraph('병리학 + 기생충학', s['subtitle']))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#0f3460')))
    story.append(Spacer(1, 6*mm))

    # ── 섹션 1: 최빈출 병리학 ─────────────────────────────
    story.append(Paragraph('★★★ 최빈출 유형 — 병리학 (3~4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_path = [
        ('1', 'HPV 16형 → 자궁경부 고등급 병터',
         '2021·2023·2024·2025 (4년)',
         '자궁경부 고등급편평상피내병터(HSIL)에서 HPV 16·18형 검출\n'
         '→ 6·11형은 저위험군(오답 선택지로 자주 등장)\n'
         '→ E6/E7 단백질이 p53·pRB 불활성화 → 세포주기조절이상\n'
         '※ Koilocyte(공포세포)가 HPV 감염의 조직학적 특징'),

        ('2', 'APC 유전자 → 가족성 선종성 용종증 (FAP)',
         '2021·2023·2024 (3년)',
         '대장에 수백 개의 용종 → 대장전절제술\n'
         '→ APC 유전자 돌연변이 (BRCA1·TP53·KRAS·RB1은 오답)\n'
         '※ 망막색소상피 비대증(CHRPE) 동반 시 FAP 강력 시사\n'
         '※ hMLH1·hPMS2 변이 → HNPCC (미스매치복구 결핍, 별도 주제)'),

        ('3', 'GIST → 카할세포(Cajal) + KIT mutation',
         '2021·2024·2025 (3년)',
         '위장관 점막하 방추형 세포 종양\n'
         '→ CD117(c-KIT)·DOG1·CD34 양성 / S100 음성\n'
         '→ 기원: 카할세포 (신경내분비세포 아님 — 오답 주의)\n'
         '→ KIT mutation이 가장 흔한 유전자 변화 (APC·KRAS 아님)'),

        ('4', '자궁내막증 → 초콜릿 낭종',
         '2023·2024·2025 (3년)',
         '월경 주기와 연관된 골반 통증 + 난임\n'
         '→ 낭종 내부: 진한 갈색(초콜릿색) 혈성 끈끈한 액체\n'
         '→ 조직 소견: 자궁내막 유사 선조직 + 헤모시데린 침착 대식세포\n'
         '※ 기형종·점액낭샘종·자궁내막암과 감별 (오답 선택지)'),

        ('5', 'CMV 감염 → 심장/신장이식 후 십이지장 미란',
         '2023·2024·2025 (3년)',
         '면역억제제 복용 중 반복 객혈·장출혈·미란성 병변\n'
         '→ 감염체: 바이러스(CMV) / 염증 패턴: 세포변성세포증식 염증\n'
         '→ 조직: 핵내봉입체(owl eye inclusion body) 특징\n'
         '※ 박테리아-화농성, 곰팡이-육아종성과 구별 (오답 패턴)'),

        ('6', '급성췌장염 → 지방괴사 병리소견',
         '2021·2024·2025 (3년)',
         '음주 후 갑작스러운 상복부→등 방사통, 혈청 아밀라제 상승\n'
         '→ 특징적 병리: 급성염증 + 지방괴사(fat necrosis)\n'
         '→ 복막의 하얗고 부스러지는 결절 = 비누화(saponification)\n'
         '※ 췌관확장·섬유화·실질위축은 만성췌장염 소견 (오답)'),

        ('7', 'BRCA1 → 유방암·난소암 가족력',
         '2023·2024·2025 (3년)',
         '어머니·이모·언니 유방암 또는 난소암 가족력\n'
         '→ 권유 검사: BRCA1 (BRCA2도 포함되나 선택지는 BRCA1)\n'
         '※ ATM·CDH1·NF1·WT1은 오답 선택지로 등장\n'
         '※ MSH2·MLH1은 HNPCC(대장암 가족력) 관련'),
    ]

    for no, title, years, desc in top_path:
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

    doc.build(story)
    print(f'PDF 생성 완료: {output_path}')


if __name__ == '__main__':
    build_pdf('/home/user/Gjp/기종평_4교시_빈출유형_분석.pdf')
