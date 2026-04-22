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

    # ── 섹션 3: ★★★ 최빈출 — 자율신경계 약물 ──────────────────
    story.append(PageBreak())
    story.append(Paragraph('★★★ 최빈출 유형 — 자율신경계 약물 (4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_ans = [
        ('7', '콜린작동성 약물 — 무스카린·니코틴 수용체',
         '2021·2023·2024·2025 (4년)',
         'Pilocarpine: 무스카린 작용제 → 동공수축·방수 배출↑ (녹내장)\n'
         '→ 부작용: 배뇨 횟수 증가 (방광 평활근 수축)\n'
         'Neostigmine: AChE 억제 → ACh↑ → 무스카린+니코틴 효과 (중증근무력증)\n'
         'Atropine: 무스카린 수용체 차단 → 동공산대, 심박수↑, 분비↓\n'
         'Scopolamine: 무스카린 차단 → 멀미 예방 (경피패치)\n'
         'Metoclopramide: D2 차단 → 구토↓, 위장운동↑, EPS 부작용\n'
         '※ 무스카린 수용체 = GPCR / 니코틴 수용체 = 이온통로 (혼동 주의)'),

        ('8', '아드레날린계 약물 — α·β 수용체 선택성',
         '2021·2023·2024·2025 (4년)',
         'α1 작용제(phenylephrine): 혈관수축 → 비충혈 제거, 혈압↑\n'
         'α1 차단제(prazosin, tamsulosin): 혈압↓, BPH 배뇨 개선\n'
         '→ prazosin 첫 복용: 기립성 저혈압 (first-dose effect)\n'
         'β1 차단제(metoprolol): 심박수↓, 심박출량↓ → 심방세동·고혈압\n'
         'β2 작용제(ritodrine, salbutamol): 자궁이완(조산↓), 기관지 이완(천식)\n'
         '비선택적 β차단제(propranolol): 기관지수축 부작용 → 천식 금기\n'
         'Epinephrine(아나필락시스): α1(혈관수축) + β1(심장↑) + β2(기관지 이완)\n'
         '※ α1 vs β2 혼동 금지 — ritodrine은 β2(자궁이완), α1(혈관수축)과 반대'),

        ('9', '골격근 이완제 · 국소마취제 · Varenicline',
         '2021·2023·2024·2025 (4년)',
         '[골격근 이완제] 경쟁적 NMJ 차단(pancuronium) → ACh와 경쟁, 신경근 차단\n'
         '→ 충분한 AChE 억제제(neostigmine)로 역전 가능\n'
         '[국소마취] Lidocaine + epinephrine: epinephrine이 혈관수축 → 흡수 지연, 효과 연장\n'
         '→ 감염조직: pH↓ → 비이온화형↓ → lidocaine 효과 감소\n'
         '[Varenicline] α4β2 니코틴 수용체 부분작용제 → 도파민↑(금단↓) + 니코틴 차단(쾌감↓)\n'
         '→ 2021: β2 수용체 혼동 선택지 출제 / 2025: 기전 직접 물음\n'
         '※ varenicline = 니코틴 수용체 (β2 아드레날린 수용체가 아님)'),
    ]

    for no, title, years, desc in top_ans:
        row = [[
            Paragraph(f'<b>{no}.</b>', s['body']),
            Paragraph(f'<b>{title}</b>', s['h2']),
            Paragraph(years, s['small'])
        ]]
        t = Table(row, colWidths=[8*mm, 110*mm, 46*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3e5f5')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#ce93d8')),
        ]))
        story.append(t)
        for line in desc.split('\n'):
            story.append(Paragraph(
                '• ' + line if not line.startswith('※') and not line.startswith('[') else line,
                s['bullet']
            ))
        story.append(Spacer(1, 2*mm))

    # ── 섹션 4: ★★★ 최빈출 — 고혈압·항균제·항정신병·항암제 ────
    story.append(PageBreak())
    story.append(Paragraph('★★★ 최빈출 유형 — 고혈압·항균제·항정신병·항암제 (4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_misc = [
        ('10', '고혈압 약물 — 이뇨제·ACEI·ARB·CCB·β차단제',
         '2021·2023·2024·2025 (4년)',
         'Thiazide: 원위세뇨관 → 저칼륨혈증, 저나트륨혈증\n'
         'Loop(furosemide): Henle 굵은 오름가지 → 강력 이뇨, 저칼륨\n'
         'Spironolactone: 알도스테론 차단 → K+ 보존, thiazide 병합 시 저칼륨 방지\n'
         'ACEI(enalapril): 마른기침 부작용 (브라디키닌 축적)\n'
         'ARB(losartan): 기침 없음, 당뇨+CKD 신보호 1차 선택\n'
         'CCB(amlodipine): 협심증+고혈압 병합에 유리\n'
         'β1 차단제(metoprolol): 심방세동·심부전, 천식 환자에 β1 선택적 사용\n'
         '※ 저칼륨 발생 시 spironolactone 추가, ACEI 기침 → ARB로 교체'),

        ('11', '항균제 — 기전별·선택·내성',
         '2021·2023·2024·2025 (4년)',
         'β-lactam(ampicillin, ceftriaxone): 세포벽 합성 억제 (PBP 결합)\n'
         'MRSA: vancomycin 선택 — 내성 기전 = 세포벽 표적(D-Ala-D-Ala→D-Lac) 구조 변화\n'
         'Fluoroquinolone(ciprofloxacin): DNA gyrase·topoisomerase IV 억제 → E.coli UTI\n'
         'Isoniazid: 미콜산 합성 억제 (결핵 1차) → 말초신경병증 → Vitamin B6 보충\n'
         'Rifampin: RNA polymerase 억제, 강력 CYP 유도 → 와파린·경구피임약 효과↓\n'
         'Fluconazole: 에르고스테롤 합성 억제 (항진균, 크립토콕쿠스·칸디다)\n'
         'Acyclovir: 바이러스 TK → 삼인산화 → DNA polymerase 억제 (헤르페스)\n'
         '※ vancomycin 내성 = 표적 변화 (β-lactamase 생산 아님)'),

        ('12', '항정신병 약물 — EPS·Clozapine 무과립구증',
         '2021·2023·2024·2025 (4년)',
         'EPS 원인: D2 수용체 차단 → 선조체 도파민 차단 → 추체외로증후군\n'
         '→ 증상: 불수의운동(tardive dyskinesia), 정좌불능(akathisia), 근긴장이상\n'
         'Haloperidol: D2 강력 차단 → EPS 높음, 대사부작용 적음\n'
         'Clozapine: D2 약한 차단 + 5-HT2A 차단 → EPS 없음\n'
         '→ 부작용: 무과립구증(agranulocytosis) — 특이체질성 반응 (독성반응 아님)\n'
         '→ 혈액검사 정기 모니터링 필수\n'
         'Olanzapine: D2+5-HT2 차단 → 대사증후군(비만·당뇨) 부작용\n'
         '※ clozapine 무과립구증 = 특이체질성, EPS 없음 = 세로토닌 수용체 차단'),

        ('13', '항암제·NSAIDs·혈당강하제',
         '2021·2023·2024·2025 (4년)',
         '[항암제] Cisplatin: DNA 가교(cross-link) → 심한 N/V → ondansetron(5-HT3 차단)\n'
         '5-FU: 티미딜산 합성↓ → S기 작용 / MDR1(P-gp): ATP 의존 배출 → 다약제 내성\n'
         '[NSAIDs] Aspirin: COX 비가역 공유결합 → 혈소판 7~10일 효과 지속\n'
         'Celecoxib: COX-2 선택적 → 위장관 독성 최소\n'
         'Acetaminophen: COX 억제 없음, 항염증 없음, 진통·해열만\n'
         '[혈당강하제] 속효성 인슐린(lispro): 식사 직전 → 식후 혈당 조절\n'
         'Sulfonylurea(glibenclamide): K+ 채널 차단 → 인슐린 분비↑\n'
         'Metformin: AMPK 활성화 → 간 포도당 생성↓\n'
         '※ MDR = 약물 배출 증가 (DNA 복구↑ 아님), Aspirin = 공유결합(비가역)'),
    ]

    for no, title, years, desc in top_misc:
        row = [[
            Paragraph(f'<b>{no}.</b>', s['body']),
            Paragraph(f'<b>{title}</b>', s['h2']),
            Paragraph(years, s['small'])
        ]]
        t = Table(row, colWidths=[8*mm, 110*mm, 46*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f5e9')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#a5d6a7')),
        ]))
        story.append(t)
        for line in desc.split('\n'):
            story.append(Paragraph(
                '• ' + line if not line.startswith('※') and not line.startswith('[') else line,
                s['bullet']
            ))
        story.append(Spacer(1, 2*mm))

    doc.build(story)
    print(f'PDF 생성 완료: {output_path}')


if __name__ == '__main__':
    build_pdf('/home/user/Gjp/기종평_6교시_빈출유형_분석.pdf')
