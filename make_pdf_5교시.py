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
    story.append(Paragraph('5교시 빈출 유형 분석', s['title']))
    story.append(Paragraph('2021 · 2023 · 2024 · 2025년도', s['subtitle']))
    story.append(Paragraph('미생물학 + 면역학', s['subtitle']))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#0f3460')))
    story.append(Spacer(1, 6*mm))

    # ── 섹션 1: ★★★ 최빈출 — 바이러스학 ─────────────────
    story.append(Paragraph('★★★ 최빈출 유형 — 바이러스학 (3~4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_virus = [
        ('1', '바이러스 감염형태 — 잠복·불현·지속·재활성',
         '2021·2023·2024·2025 (4년)',
         '잠복감염(latent): 바이러스 DNA가 신경절 세포에 존재, 증식 없음\n'
         '→ HSV: 삼차신경절 / VZV: 후근신경절 — 재활성 시 수포 재발\n'
         '불현감염(abortive): 반증식허용세포에서 거대분자 생산 제한, 복제 불완전\n'
         '지속감염(persistent/chronic): 바이러스 지속 검출 (HIV, HCV)\n'
         '재활성감염(reactivated): 면역저하 시 잠복→활성화 (VZV→대상포진)\n'
         '※ 잠복감염 ≠ 비리온 존재 / ≠ 외피 존재 → DNA만 신경세포에 존재'),

        ('2', '한탄바이러스 / 유행성출혈열 (신증후출혈열)',
         '2021·2023·2024·2025 (4년)',
         '병원체: Hantaan virus — 분절 안 된 음성가닥 ssRNA, 외피 보유\n'
         '감염경로: 들쥐(등줄쥐) 배설물 건조 → 흡입 (진드기 물림 아님!)\n'
         '역학: 가을 추수철, 농부·군인·야외활동, 진드기 물린 상처 없음\n'
         '임상 5단계: 발열기 → 저혈압기 → 핍뇨기 → 이뇨기 → 회복기\n'
         '주요 소견: 혈소판감소, 단백뇨(3+), BUN/Cr 상승, 결막출혈·점출혈\n'
         '※ 쯔쯔가무시와 감별: 진드기 물린 딱지(eschar) 없음 + 쥐 배설물 흡입'),

        ('3', '인플루엔자바이러스 — 항원변이·뉴라민분해효소 억제제',
         '2021·2023·2025 (3년)',
         '유전체: 분절된 음성가닥 RNA 8개 → 항원대변이(reassortment) 가능\n'
         '항원 소변이(antigenic drift): HA/NA 점돌연변이 누적 → 연간 유행\n'
         '항원 대변이(antigenic shift): 두 바이러스 동시감염 → 유전체 재편성 → 범유행\n'
         '간섭(interference): 한 바이러스가 다른 바이러스 감염 억제 (2025 신유형)\n'
         '치료제: 오셀타미비르(oseltamivir) — 뉴라민분해효소(NA) 억제 → 방출 차단\n'
         '※ 항원 소변이=점돌연변이, 항원 대변이=유전체 재편성 (혼동 주의)'),

        ('4', '노로바이러스 — 해산물 식중독',
         '2021·2023·2024 (3년)',
         '유전체: 양성 단일가닥 RNA (ssRNA+), 외피 없음 → 소독제 저항성\n'
         '감염경로: 오염된 해산물(조개·굴) 섭취, 대변-구강, 직접 접촉\n'
         '임상: 메스꺼움·구토·설사 — 12~48시간 이내 자연회복\n'
         '배양검사: 대변세균배양 음성 + RNA 바이러스 확인 → 노로바이러스 시사\n'
         '로타바이러스와 비교: 로타=dsRNA, 주로 영아, 겨울철 설사\n'
         '※ "해산물 섭취 + 대변 세균배양 음성 + ssRNA(+)" → 노로바이러스'),

        ('5', 'SARS-CoV-2 — Spike 단백·부착·백신',
         '2023·2024·2025 (3년)',
         '유전체: 양성 단일가닥 RNA (ssRNA+), 외피 보유 → 알코올·비누에 감수성\n'
         'Spike 단백: ACE2 수용체에 결합 → 부착(attachment) 단계\n'
         '단클론항체: Evusheld → Spike 단백 표적 → 부착 단계 차단\n'
         'mRNA 백신/DNA 백신: Spike 단백 유전자 사용 (사진에서 Spike 부위 선택)\n'
         'HPV와 비교: HPV=외피 없음→소독제 저항, SARS-CoV-2=외피 있음→소독제 감수성\n'
         '※ 부착(attachment)·투과(penetration)·탈외피(uncoating) 순서 암기'),
    ]

    for no, title, years, desc in top_virus:
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
    build_pdf('/home/user/Gjp/기종평_5교시_빈출유형_분석.pdf')
