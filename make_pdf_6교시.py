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

    # ── 섹션 5: ★★★ 3년 출제 — SSRI·결핵·오피오이드·와파린·흡입마취제·알코올 ──
    story.append(PageBreak())
    story.append(Paragraph('★★★ 최빈출 유형 — SSRI·결핵·오피오이드·와파린·흡입마취제·알코올 (3년 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top3_items = [
        ('14', 'SSRI / 우울증 · 세로토닌 증후군',
         '2023·2024·2025 (3년)',
         'SSRI(fluoxetine, paroxetine): 세로토닌 재흡수 억제 → 시냅스 세로토닌↑\n'
         '→ 시냅스 전 재흡수 펌프(transporter) 차단 — 수용체 차단 아님\n'
         'GI 부작용: 장 세로토닌 수용체(5-HT3) 직접 자극 → 구역·설사\n'
         '세로토닌 증후군: SSRI + 트립탄(sumatriptan) 병용 → 불안·근긴장·고체온\n'
         '→ MDMA(엑스터시): 세로토닌 과다 방출 → 고체온 + 저나트륨혈증\n'
         '항우울 효과 발현: 복용 후 2주 이상 지연\n'
         '※ GI 부작용 = 세로토닌 수용체 자극 (도파민·히스타민 아님)'),

        ('15', '결핵 약물 — Isoniazid·Rifampin 부작용·상호작용',
         '2021·2024·2025 (3년)',
         'Isoniazid: 미콜산 합성 억제, 1차 항결핵제\n'
         '→ 말초신경병증(손발 저림) → Vitamin B6(pyridoxine) 보충\n'
         'Rifampin: RNA polymerase 억제, 강력 CYP 유도제\n'
         '→ 와파린 병용: CYP 유도 → 와파린 대사↑ → 항응고 효과↓ → PT/INR↓\n'
         '→ 경구피임약, cyclosporine, 항레트로바이러스제 효과도 감소\n'
         '4제 요법: Isoniazid + Rifampin + Pyrazinamide + Ethambutol\n'
         '※ Rifampin = CYP 유도(효과 감소), Isoniazid = B6 부족(신경독성)'),

        ('16', '오피오이드 — 수용체·금단·말초 길항제',
         '2021·2023·2024 (3년)',
         'μ 수용체: 진통, 호흡억제, 변비, 도취감 — 호흡억제 주원인\n'
         '급성 중독: 동공축소(miosis) + 호흡억제 + 의식저하 → μ수용체\n'
         '→ 길항제: naloxone(정맥) → 즉각 역전\n'
         'Methylnaltrexone: 말초 μ 수용체만 차단 → 변비 해소 (중추 진통 유지)\n'
         '신체의존·금단: 갑작스런 중단 → 자율신경 항진(설사·빈맥·발한·불안)\n'
         '내성: 수용체 탈감작, 하향조절\n'
         '※ 호흡억제 = μ수용체 (κ=불쾌감, δ=기분조절)'),

        ('17', '와파린·항응고제·약물 상호작용',
         '2023·2024·2025 (3년)',
         'Warfarin: Vitamin K 의존성 응고인자 II·VII·IX·X 합성 억제\n'
         'Heparin: 항트롬빈 III 활성화 → 트롬빈·Xa 억제, 정맥 투여\n'
         '→ 과다출혈 발생 시: protamine sulfate로 역전\n'
         'Clopidogrel: ADP 수용체(P2Y12) 비가역 차단 → 혈소판 응집↓\n'
         'Rifampin + warfarin: CYP 유도 → 와파린 혈중 농도↓ → 효과↓\n'
         '→ 모니터링: PT/INR 증가 목표 (INR 2~3)\n'
         '※ Rifampin = 와파린 효과 감소 (증가 아님)'),

        ('18', '흡입마취제 — MAC·Partition coefficient',
         '2021·2023·2024 (3년)',
         'MAC: Minimum Alveolar Concentration — 50% 환자 마취 유지 최소 농도\n'
         'Oil/gas 계수↑ → 지용성↑ → 뇌 친화도↑ → MAC 낮음 (낮은 농도로 마취)\n'
         'Blood/gas 계수↓ → 폐에서 혈중 이행 느림 → 마취 유도·회복 빠름\n'
         '→ Desflurane: blood/gas 가장 낮음 → 마취유도·회복 가장 빠름\n'
         '→ Diethyl ether: blood/gas 높음 → 마취 유도 느림\n'
         '※ blood/gas 낮을수록 빠름 (직관과 반대 — 혼동 주의)'),

        ('19', '알코올 대사 · 알데하이드탈수소효소 결핍',
         '2023·2024·2025 (3년)',
         '대사경로: 에탄올 →(ADH)→ 아세트알데하이드 →(ALDH)→ 아세트산\n'
         'ALDH 결핍(동아시아인 유전적): 아세트알데하이드 축적 → 홍조·빈맥·두통\n'
         '→ 소량 음주에도 증상, 가족력 양성\n'
         'Disulfiram: ALDH 억제 → 알코올 혐오요법 (알코올 의존 치료)\n'
         '알코올 약동학: 0차 약동학 → 농도-시간 직선 (일정 속도 대사)\n'
         '→ 고농도 시 효소 포화 → 일차에서 0차로 전환\n'
         '※ ALDH 결핍 = 아세트알데하이드 축적 (ADH 결핍 아님)'),
    ]

    for no, title, years, desc in top3_items:
        row = [[
            Paragraph(f'<b>{no}.</b>', s['body']),
            Paragraph(f'<b>{title}</b>', s['h2']),
            Paragraph(years, s['small'])
        ]]
        t = Table(row, colWidths=[8*mm, 110*mm, 46*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fce4ec')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#f48fb1')),
        ]))
        story.append(t)
        for line in desc.split('\n'):
            story.append(Paragraph(
                '• ' + line if not line.startswith('※') else line,
                s['bullet']
            ))
        story.append(Spacer(1, 2*mm))

    # ── 섹션 6: ★★ 준빈출 표 ────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('★★ 준빈출 유형 요약표 (2년 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 3*mm))

    semi_data = [
        ['주제', '핵심 약물 / 기전', '오답 패턴', '출제 연도'],
        ['알츠하이머\ndonepezil',
         'AChE 억제 → ACh↑\nNMDA 차단(memantine)과 구별',
         'GABA·도파민 수용체 작용\n→ 오답',
         '2021·2025'],
        ['파킨슨병\nlevodopa/carbidopa',
         'Levodopa: 도파민 전구체\nCarbidopa: AADC 억제 → 말초 전환↓',
         'carbidopa = COMT 억제제\n→ 오답 (entacapone)',
         '2023·2024'],
        ['헤르페스\nacyclovir',
         '바이러스 TK → 삼인산화\n→ DNA polymerase 억제',
         '바이러스 부착·방출 억제\n→ 오답',
         '2023·2024'],
        ['Statin\n근육통',
         'HMG-CoA reductase 억제\n→ 간 콜레스테롤 합성↓',
         '근육통 = 횡문근융해증 위험\n→ CPK 모니터링',
         '2023·2025'],
        ['Varenicline\n금연',
         'α4β2 니코틴 수용체 부분작용제\n도파민↑(금단↓) + 니코틴 차단',
         'β2 아드레날린 수용체\n→ 오답',
         '2023·2025'],
        ['통풍\nallopurinol',
         '잔틴 산화효소 억제 → 요산 생성↓\nProbenecid: 요산 배설↑',
         'colchicine = 발작 급성 치료\nallopurinol = 장기 예방',
         '2021·2025'],
        ['녹내장\n안압 하강',
         'Pilocarpine: 무스카린 작용 → 방수 배출↑\nTimolol: β차단 → 방수 생성↓',
         '피로카르핀 = 동공산대\n→ 오답 (실제 동공수축)',
         '2021·2025'],
        ['자궁수축억제제\nRitodrine',
         'β2 수용체 작용제 → 자궁 평활근 이완\n→ 조산 방지',
         'α1 수용체 작용\n→ 오답',
         '2024·2025'],
        ['갑상선 약물\nPTU/MMI',
         'Peroxidase 억제 → 갑상선호르몬 합성↓\nPTU: T4→T3 전환도 억제',
         'PTU 임신 1분기 금기(×)\n→ 오히려 임신 1분기에 PTU 사용',
         '2021·2023'],
        ['Digoxin\n심부전',
         'Na+/K+ ATPase 억제 → 세포내 Na+↑\n→ Na+/Ca2+ 교환체 역방향 → Ca2+↑ → 수축력↑',
         'Ca2+ 통로 직접 차단\n→ 오답',
         '2023·2024'],
    ]

    col_w = [30*mm, 55*mm, 48*mm, 25*mm]
    tbl = Table(semi_data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'NanumGothicBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'NanumGothic'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white]),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cccccc')),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#0f3460')),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 6*mm))

    # ── 주제별 핵심 정리 ───────────────────────────────────────
    story.append(Paragraph('주제별 핵심 암기 포인트', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    keypoints = [
        ('약동학 공식 정리',
         [
             'Vd = Dose / C₀ (IV bolus y절편)',
             't½ = 0.693 / k (1차 약동학)',
             'LD = Vd × Css (부하용량)',
             'Css = (F × 용량) / (CL × τ)',
             '알코올 = 0차 약동학 (농도-시간 직선)',
         ]),
        ('임상시험 단계 암기',
         [
             '전임상 → 1상(건강인·PK) → 2상(소수 환자·용량) → 3상(다수 환자·확증) → 4상(시판후)',
             '1상: "반복투여 + 안전성 + 건강인" 키워드',
             '2상: "소수 환자 + 유효 용량 결정" 키워드',
             '3상: "이중맹검 + 무작위 + 효능 확증" 키워드',
         ]),
        ('수용체-약물 연결고리',
         [
             'D2 차단 → EPS (haloperidol, metoclopramide)',
             'D2+5HT2 차단 → EPS 없음 (clozapine, olanzapine)',
             'α4β2 니코틴 부분작용 → varenicline (금연)',
             'β2 작용 → ritodrine(조산↓), albuterol(천식)',
             'μ 수용체 → 호흡억제·진통·변비',
         ]),
        ('CYP450 약물 상호작용 핵심',
         [
             'Rifampin = 강력 CYP 유도 → 와파린·피임약 효과↓',
             'Fluoxetine/paroxetine = CYP 억제 → 병용 약물 독성↑',
             '알코올(만성) = CYP2E1 유도 → acetaminophen 독성↑',
             '자몽주스 = CYP3A4 억제 → statin·CCB 혈중 농도↑',
         ]),
        ('부작용 연결 암기',
         [
             'ACEI → 마른기침 (브라디키닌) / ARB → 기침 없음',
             'Clozapine → 무과립구증 (특이체질성)',
             'Isoniazid → 말초신경병증 (Vit B6 보충)',
             'Cisplatin → 신독성·구역구토 (ondansetron)',
             'Thiazide → 저칼륨·저나트륨 / Loop → 저칼륨',
             'Statin → 근육통·횡문근융해증 (CPK↑)',
         ]),
    ]

    for heading, points in keypoints:
        story.append(Paragraph(f'▶ {heading}', s['h2']))
        for pt in points:
            story.append(Paragraph(f'• {pt}', s['bullet']))
        story.append(Spacer(1, 2*mm))

    # ── 섹션 7: 연도별 출제 현황 표 ───────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('연도별 출제 현황 (6교시 약리학)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 3*mm))

    trend_header = ['주제', '2021', '2023', '2024', '2025', '합계']
    trend_rows = [
        ['임상시험 단계 구분', '●', '●', '●', '●', '4'],
        ['용량-반응 곡선 / 길항제', '●', '●', '●', '●', '4'],
        ['약동학 기초 (PK)', '●', '●', '●', '●', '4'],
        ['자율신경계 약물', '●', '●', '●', '●', '4'],
        ['고혈압 약물', '●', '●', '●', '●', '4'],
        ['항균제 (기전·선택·내성)', '●', '●', '●', '●', '4'],
        ['혈당강하제 / 인슐린', '●', '●', '●', '●', '4'],
        ['NSAIDs / COX 억제', '●', '○', '●', '●', '3'],
        ['항정신병 약물 (EPS·clozapine)', '●', '●', '●', '●', '4'],
        ['항암제 / MDR / P-gp', '●', '●', '●', '●', '4'],
        ['나이트로글리세린 / 협심증', '●', '○', '●', '●', '3'],
        ['약물 이온화 / pH', '○', '●', '●', '●', '3'],
        ['SSRI / 우울증', '○', '●', '●', '●', '3'],
        ['결핵 약물 (INH·Rifampin)', '●', '○', '●', '●', '3'],
        ['이뇨제 (thiazide·loop·spiro)', '●', '●', '●', '●', '4'],
        ['흡입마취제 (MAC)', '●', '●', '●', '○', '3'],
        ['알코올 대사 (ALDH)', '○', '●', '●', '●', '3'],
        ['오피오이드 / 마약성 진통제', '●', '●', '●', '○', '3'],
        ['와파린 / 항응고제', '○', '●', '●', '●', '3'],
        ['파킨슨병 (levodopa)', '○', '●', '●', '○', '2'],
        ['알츠하이머 (donepezil)', '●', '○', '○', '●', '2'],
        ['헤르페스 (acyclovir)', '○', '●', '●', '○', '2'],
        ['Statin 근육 부작용', '○', '●', '○', '●', '2'],
        ['통풍 (allopurinol)', '●', '○', '○', '●', '2'],
        ['Varenicline 금연', '○', '●', '○', '●', '2'],
    ]

    trend_data = [trend_header] + trend_rows
    col_w2 = [68*mm, 18*mm, 18*mm, 18*mm, 18*mm, 14*mm]
    tbl2 = Table(trend_data, colWidths=col_w2, repeatRows=1)

    ts2 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'NanumGothicBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'NanumGothic'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cccccc')),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#16213e')),
    ])
    # 4년 출제 행 강조
    for i, row in enumerate(trend_rows, start=1):
        if row[-1] == '4':
            ts2.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#e3f2fd'))
        elif row[-1] == '3':
            ts2.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f9fbe7'))
    tbl2.setStyle(ts2)
    story.append(tbl2)
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph('● 출제  ○ 미출제   파란 배경 = 4년 연속 ★★★  연두 배경 = 3년 ★★★', s['small']))

    # ── 섹션 8: 시험 전략 TIP ─────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('시험 전략 TIP', s['h1']))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#e53935')))
    story.append(Spacer(1, 3*mm))

    tips = [
        ('1', '약동학 계산 문제는 반드시 1문항 출제',
         '공식 3개만 암기: LD=Vd×Css / Css=F×D/(CL×τ) / t½=0.693/k\n'
         '알코올 = 0차 약동학(직선), 나머지 = 1차(지수 감소)'),
        ('2', '임상시험 단계 = 매년 1~2문항',
         '"건강인+안전성" = 1상 / "소수 환자+유효 용량" = 2상\n'
         '"다수 환자+효능 확증+이중맹검" = 3상'),
        ('3', '용량-반응 곡선 그래프 문제 = 매년 출제',
         '경쟁적 길항제: EC50↑, Emax 불변 / 비경쟁적: Emax↓, EC50 불변\n'
         'BZD vs Barbiturate: BZD=EC50↓(좌이동), Barbiturate=Emax↑'),
        ('4', '수용체 이름과 약물 연결 반드시 암기',
         'D2 차단=EPS / α4β2 니코틴=varenicline / β2=ritodrine(자궁), albuterol(천식)\n'
         'μ 수용체=호흡억제 / GABAA=BZD·바르비투르'),
        ('5', 'CYP 유도 vs 억제 단골 출제',
         'Rifampin = 강력 유도 → 와파린 효과↓ (매년 변형 출제)\n'
         'SSRI = CYP 억제 → 트립탄 병용 시 세로토닌 증후군'),
        ('6', '부작용 연결 오답 선택지 패턴',
         'ACEI 마른기침 → 직접 독성 아님, 브라디키닌 축적\n'
         'Clozapine 무과립구증 → 독성반응(×) → 특이체질성\n'
         'Isoniazid 신경병증 → Vit B6, Rifampin 와파린↓ → CYP 유도'),
    ]

    for no, heading, detail in tips:
        tip_data = [[
            Paragraph(f'<b>TIP {no}</b>', s['body']),
            Paragraph(f'<b>{heading}</b>', s['h2']),
        ]]
        tip_t = Table(tip_data, colWidths=[16*mm, 148*mm])
        tip_t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ffebee')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#ef9a9a')),
            ('BOX', (0, 0), (-1, 0), 1, colors.HexColor('#e53935')),
        ]))
        story.append(tip_t)
        for line in detail.split('\n'):
            story.append(Paragraph(f'  → {line}', s['note']))
        story.append(Spacer(1, 2*mm))

    doc.build(story)
    print(f'PDF 생성 완료: {output_path}')


if __name__ == '__main__':
    build_pdf('/home/user/Gjp/기종평_6교시_빈출유형_분석.pdf')
