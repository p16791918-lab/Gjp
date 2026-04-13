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

# 한글 폰트 등록
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
    story.append(Paragraph('2교시 빈출 유형 분석', s['title']))
    story.append(Paragraph('2021 · 2023 · 2024 · 2025년도 | 과목: 생화학', s['subtitle']))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#0f3460')))
    story.append(Spacer(1, 6*mm))

    # ── 섹션 1: 최빈출 유형 ────────────────────────────────
    story.append(Paragraph('★★★ 최빈출 유형 (3~4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_items = [
        ('1', '전자전달사슬 복합체 IV 억제제',
         '2021·2023·2024·2025 (4년 전부)',
         '일산화탄소(CO) 또는 청산가리(cyanide) → 복합체 IV(cytochrome c oxidase) 억제\n'
         '→ Cytochrome c에 환원된(reduced) 형태가 축적됨\n'
         '※ 2021·2024: 청산가리(cyanide) / 2023·2025: 일산화탄소(CO)\n'
         '※ 복합체 I-II-III-CoQ-Cytochrome c-복합체 IV-O₂ 순서 암기 필수'),

        ('2', '금식(fasting) 시 혈중 대사체 변화 그래프',
         '2021·2023·2024',
         '그래프 A-B-C 식별: A(가장 높음)=케톤체, B=지방산, C(가장 낮음)=포도당\n'
         '→ 금식 초기: 포도당↓, 지방산↑(분해) → 수일 후 케톤체가 지방산 초과\n'
         '→ 2024에서는 "(A) 증가의 대사경로 = 케톤생성(ketogenesis)"로 변형 출제\n'
         '※ 매년 동일한 사진 그래프 형태로 반복 출제'),

        ('3', '팔미트산(C16) β-산화 ATP 계산',
         '2021·2023·2025',
         '팔미트산 → 7회 β-산화 → 7 FADH₂ + 7 NADH + 8 acetyl-CoA\n'
         '→ β-산화 단계만: 7×1.5 + 7×2.5 = 10.5 + 17.5 = 28 ATP\n'
         '→ 전체(TCA 포함): 7×1.5 + 7×2.5 + 8×10 - 2(활성화) = 106 ATP\n'
         '※ 2021: 7번 vs 3번 각각 계산 / 2023: β-산화 생성 ATP만 / 2025: 전체 106 ATP'),

        ('4', 'dsRNA 바이러스 — uracil 비율로 guanine 계산',
         '2021·2023·2025',
         '이중가닥(double-strand) RNA 바이러스에 Chargaff 법칙 적용\n'
         'U = A, G = C (dsRNA이므로 염기쌍 대칭)\n'
         '→ uracil = 10% → adenine = 10% → G+C = 80% → guanine = 40%\n'
         '※ 장염 5세 남아 대변에서 dsRNA 바이러스 검출 — 동일 문구로 3년 반복 출제'),

        ('5', '산화질소(NO, Nitric Oxide) 식별',
         '2021·2024·2025',
         'L-arginine → L-citrulline + NO (산화질소합성효소, NOS에 의해)\n'
         '→ 혈관 평활근 이완 (cGMP 경로)\n'
         '→ 나이트로글리세린(nitroglycerin)이 NO를 생성하여 협심증 치료\n'
         '※ 2021: 반응식 사진(L-arginine→L-citrulline+A), 역할 = 평활근 이완\n'
         '※ 2024·2025: 특성 설명(arginine 유래, 혈관이완, cGMP)으로 물질 식별'),

        ('6', '지속 운동 시 에너지원 — 유리지방산',
         '2023·2024·2025',
         '마라톤 등 지속적 유산소 운동 그래프 → 화살표 에너지원 = 유리지방산(free fatty acid)\n'
         '→ 크레아틴인산(수초) → 근육 글리코겐(수분) → 혈당 → 유리지방산(수시간)\n'
         '→ 2024: "마라톤 2시간 = 지방조직의 중성지방"\n'
         '※ 2023·2025: 동일 그래프(사진)에서 화살표 에너지원 선택'),

        ('7', '통풍(Gout) — 퓨린 분해 대사 / 요산(uric acid)',
         '2021·2023·2025',
         '퓨린 분해 최종 산물 = 요산(uric acid)\n'
         '→ 과도하게 축적 시 관절에 결정 형태로 침착 → 통풍\n'
         '→ 치료: allopurinol (xanthine oxidase 억제)\n'
         '※ 2021: allopurinol 처방, purine degradation 경로\n'
         '※ 2023: 엄지발가락 통증, 혈청 요산 증가 → 통풍\n'
         '※ 2025: 요산이 관절에 결정 침착 → 통풍'),

        ('8', 'mRNA 5\' Capping 기능',
         '2021·2023',
         'mRNA가 핵산말단분해효소(exonuclease)에 의해 분해되지 않도록 보호\n'
         '→ mRNA가 핵공을 통해 핵으로부터 세포질로 방출되는 과정 도움\n'
         '→ 단백질 번역 초기 mRNA와 리보솜 상호작용에 필요\n'
         '※ 동일한 세 가지 기능 설명으로 2년 연속 동일 문구 출제'),
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
            story.append(Paragraph('• ' + line if not line.startswith('※') else line, s['bullet']))
        story.append(Spacer(1, 2*mm))

    # ── 섹션 2: 준빈출 유형 ────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('★★ 준빈출 유형 (2년 이상 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    table_header = ['유형', '핵심 포인트', '출제연도']
    table_data = [table_header] + [
        ['PKU(페닐케톤뇨증) — 결핍 효소 산물',
         '페닐알라닌 수산화효소 결핍 → 타이로신(tyrosine) 감소\n밝은 피부·머리카락 아이 사진 제시',
         '2023, 2024'],
        ['G6PD 결핍 → NADPH 결핍 → 용혈',
         '항말라리아 약 후 용혈 / 산화적 스트레스 증가\nRBC의 NADPH 결핍으로 산화 손상',
         '2023, 2024'],
        ['철결핍성 빈혈 검사 소견',
         '총철결합능(TIBC) 증가, ferritin 감소\ntransferrin 증가, 소적혈구',
         '2024, 2025'],
        ['HMG-CoA 환원효소 억제제(스타틴)',
         'HMG-CoA → mevalonate 단계 경쟁적 억제\nKm 증가, Vmax 불변 (경쟁 억제)',
         '2023, 2025'],
        ['미토콘드리아 DNA polymerase γ',
         '세균 DNA pol 억제 항생제 → 미토콘드리아 손상\n미토콘드리아 DNA 복제 효소 = polymerase γ',
         '2023, 2024'],
        ['2,3-BPG → 헤모글로빈 산소 친화도 감소',
         '2,3-BPG 증가 → 산소-헤모글로빈 해리곡선 우측 이동\n→ 조직 산소 해리 증가 (고산지역·간부전 환자)',
         '2021, 2024'],
        ['Acetyl-CoA 세포질 이동 = citrate shuttle',
         '지방산 합성 위해 미토콘드리아 → 세포질 이동\ncitrate 형태로 이동 = 시트르산 수송계',
         '2021, 2025'],
        ['siRNA — RNA 간섭(RNAi)',
         'mRNA 분해로 특정 단백질 knock-down\nRISC 복합체 이용, 21~23 염기 구성',
         '2021, 2023'],
        ['L/S ratio — diacylglycerol + CDP',
         '태아 폐성숙 지표 (L/S ≥ 2 = 성숙)\ndiacylglycerol + CDP-choline → phosphatidylcholine',
         '2021, 2025'],
        ['신생아 고암모니아혈증 — 요소회로 장애',
         '요소회로 효소 결핍 → 암모니아 축적 → 글루타민 증가\n아르지닌 투여 → ornithine carbamoyl transferase 활성화',
         '2021, 2024, 2025'],
        ['당화혈색소(HbA1c)',
         '비효소적 당화반응으로 생성, 장기 혈당 지표(2~3개월)\n인슐린 처방 후 1개월 내 HbA1c 변화 없음 = 적혈구 반감기',
         '2021, 2023'],
        ['글루타치온(Glutathione) 항산화',
         'Cys + Glu + Gly 트리펩타이드, 강력 항산화\nNADPH에 의해 환원·재생, 과산화수소 제거',
         '2021, 2025'],
        ['미오글로빈 vs 헤모글로빈 산소 친화도',
         '미오글로빈: 단량체, 산소분압만 영향, 높은 친화도\n헤모글로빈: 사량체, 협동결합, 2,3-BPG·pH·CO₂ 영향',
         '2024, 2025'],
        ['Warburg effect / PET-FDG',
         '종양세포: 산소 충분해도 해당과정 항진(혐기성 해당)\n18F-FDG-PET에서 포도당 고섭취 → 종양 진단',
         '2023, 2024'],
    ]

    col_w = [55*mm, 85*mm, 26*mm]
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

    # ── 섹션 3: 주제별 핵심 정리 ───────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('주제별 핵심 포인트 요약', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    sections = [
        ('에너지 대사 (탄수화물·지방)', [
            '해당과정 → 피루브산 → acetyl-CoA (미토콘드리아 기질)',
            '팔미트산 β-산화: 7회 → 7FADH₂+7NADH+8acetyl-CoA, 전체 106 ATP',
            '금식: 포도당↓→지방산↑→케톤체↑↑ (장기 금식 시 케톤체>지방산)',
            '케톤체 합성: 간 미토콘드리아 HMG-CoA synthase / 케톤체 산화: 간 외 조직',
            'Acetyl-CoA 세포질 이동: citrate shuttle (지방산 합성)',
            '암세포: 산소 있어도 해당과정 항진 = Warburg effect',
        ]),
        ('호흡사슬 & 산화적 인산화', [
            '전자전달 순서: NADH → 복합체I → CoQ → 복합체III → Cytochrome c → 복합체IV → O₂',
            'Complex IV 억제: CO(일산화탄소), cyanide(청산가리) → cytochrome c 축적(산화됨)',
            'Uncoupler: proton gradient 해소 → ATP 생성↓, 열 발생↑',
            'ATP synthase 억제 → NADH 축적, 전자전달 감소',
        ]),
        ('뉴클레오티드 대사 & 분자생물학', [
            'dsRNA Chargaff: U=A, G=C → uracil 10% → guanine 40%',
            '퓨린 분해 최종 산물: 요산(uric acid) → 통풍 / allopurinol(xanthine oxidase 억제)로 치료',
            'Lesch-Nyhan 증후군: HGPRT 결핍 (퓨린 재활용 불가)',
            'mRNA 5\'capping: 분해 보호 + 핵공 통과 + 리보솜 결합',
            'siRNA: RISC 이용, 21~23nt, 표적 mRNA 분해 (knock-down)',
            'PKU: 페닐알라닌 수산화효소 결핍 → 타이로신 감소, 페닐케톤 축적',
        ]),
        ('지질 대사 & 콜레스테롤', [
            'L/S ratio: 태아 폐성숙 지표 → phosphatidylcholine (diacylglycerol + CDP-choline)',
            'HMG-CoA 환원효소: 콜레스테롤 합성 속도조절단계 → 스타틴으로 경쟁적 억제',
            'arachidonic acid → PG: cyclooxygenase(COX) / 류코트라이엔: lipoxygenase',
            'NO 합성: L-arginine → NO + L-citrulline / 혈관이완(cGMP) / 협심증 치료(니트로글리세린)',
            'Apoprotein: ApoC-II 결핍 → lipoprotein lipase 활성↓ → 고중성지방',
        ]),
        ('혈액 & 임상 생화학', [
            '헤모글로빈: 협동결합, 2,3-BPG·pH·CO₂ 영향 / 미오글로빈: 높은 친화도, 산소분압만 영향',
            '2,3-BPG 증가 → 산소 해리↑ → 조직 산소 공급↑ (고산지역, 말기 간부전)',
            'HbA1c: 비효소적 당화, 2~3개월 혈당 반영, 적혈구 반감기(~120일) 때문에 단기 변화 미반영',
            'G6PD 결핍: NADPH↓ → 글루타치온 재생 불가 → RBC 산화 손상 → 용혈성 빈혈',
            '철결핍성 빈혈: ferritin↓, TIBC↑, transferrin↑, 소적혈구, 저색소성',
            '비타민 B12 결핍: 위소매절제술/위절제술 후 → 대적혈구성 빈혈',
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
        ['Complex IV 억제 (CO/cyanide)', '○ (cyanide)', '○ (CO)', '○ (cyanide)', '○ (CO)'],
        ['금식 그래프 A-B-C', '○', '○', '○', '-'],
        ['팔미트산 β-산화 ATP', '○', '○', '-', '○'],
        ['dsRNA uracil→guanine 40%', '○', '○', '-', '○'],
        ['산화질소(NO) 식별', '○', '-', '○', '○'],
        ['지속 운동 = 유리지방산', '-', '○', '○', '○'],
        ['통풍 / 요산', '○', '○', '-', '○'],
        ['5\' capping', '○', '○', '-', '-'],
        ['PKU (타이로신 감소)', '-', '○', '○', '-'],
        ['G6PD 결핍 → 용혈', '-', '○', '○', '-'],
        ['철결핍성 빈혈', '-', '-', '○', '○'],
        ['HMG-CoA 억제제(스타틴)', '-', '○', '-', '○'],
        ['DNA polymerase γ', '-', '○', '○', '-'],
        ['2,3-BPG 헤모글로빈', '○', '-', '○', '-'],
        ['Acetyl-CoA citrate shuttle', '○', '-', '-', '○'],
        ['siRNA / RNAi', '○', '○', '-', '-'],
        ['요소회로 / 고암모니아혈증', '○', '-', '○', '○'],
        ['HbA1c 비효소적 당화', '○', '○', '-', '-'],
        ['글루타치온 항산화', '○', '-', '-', '○'],
        ['미오글로빈 vs 헤모글로빈', '-', '-', '○', '○'],
        ['Warburg effect / PET-FDG', '-', '○', '○', '-'],
        ['비타민 B1 결핍 (Wernicke)', '-', '-', '○', '-'],
        ['비타민 B12 결핍', '-', '-', '○', '-'],
    ]

    col_w2 = [75*mm, 22*mm, 22*mm, 22*mm, 22*mm]
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

    # 출제된 셀(○) 강조
    for row_idx in range(1, len(yearly_data)):
        for col_idx in range(1, 5):
            if yearly_data[row_idx][col_idx] != '-':
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
            '① Complex IV 억제제(CO/cyanide)는 4년 연속 반드시 출제됩니다. '
            '② dsRNA 바이러스 guanine 40%, 팔미트산 β-산화 ATP(106 또는 28), '
            '금식 그래프(케톤체>지방산>포도당)는 계산형 반복 유형입니다. '
            '③ NO 특성(arginine 유래, 혈관이완, cGMP)과 마라톤 에너지원(유리지방산)은 '
            '사진 제시형으로 거의 동일한 그래프가 반복됩니다. '
            '④ 통풍→요산, PKU→타이로신, G6PD→NADPH는 임상 증상과 연결 연습이 핵심입니다.',
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
    build_pdf('/home/user/Gjp/기종평_2교시_빈출유형_분석.pdf')
