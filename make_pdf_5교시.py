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

    # ── 섹션 2: ★★★ 최빈출 — 세균학·진균학·면역학 ──────────
    story.append(PageBreak())
    story.append(Paragraph('★★★ 최빈출 유형 — 세균학·진균학·면역학 (3~4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_bact = [
        ('6', '결핵 (M. tuberculosis) — 항산성염색·잠복감염·과민반응',
         '2021·2023·2024·2025 (4년)',
         '항산성염색(Ziehl-Neelsen): 세포벽 미콜산(지방산) → 탈색 저항 → 붉은 막대균\n'
         '잠복결핵: 투베르쿨린 양성 + IGRA 양성 + X선 정상 + 무증상 → 항결핵제 처방\n'
         '폐 병변: 상엽(apex) 호발, 동공(cavity)·석회화·선상침윤 — 하엽이면 다른 진단\n'
         '조직 손상 기전: 세포매개성 과민반응 (제4형) — 내독소·외독소가 아님\n'
         '면역학적 검사: 투베르쿨린 피부반응검사(TST) / 인터페론감마 분비검사(IGRA)\n'
         '※ "항산성염색 + 상엽 동공 + 식은땀·객혈" → 결핵, 손상기전 = 세포매개성'),

        ('7', 'H. pylori — 위염·궤양·위암',
         '2021·2023·2025 (3년)',
         '형태: 그람음성 나선형 막대균, 편모 운동성 (매우 활발)\n'
         '핵심 효소: 카탈라제(+), 요소분해효소(+) — 요소→암모니아+CO₂ → 알칼리화\n'
         '독성인자: VacA(공포형성 세포독소), CagA, 단백·지질 분해효소\n'
         '배양: 미호기성(5% CO₂), 37°C, 5일 이상 → 작은 집락\n'
         '질환 진행: 위염 → 위십이지장궤양 → 저등급 MALT 림프종 → 위선암\n'
         '※ Campylobacter와 감별: 둘 다 나선형이지만 Campy=요소분해효소(-)+장염'),

        ('8', 'Legionella pneumophila — 냉각탑·에어로졸',
         '2023·2024·2025 (3년)',
         '환경: 냉각탑, 샤워기, 가습기, 월풀 스파 — 인공 수환경에 서식\n'
         '전파: 에어로졸(비말핵) 흡입 — 사람 간 직접 전파 없음\n'
         '역학: 고온다습 늦여름·초가을 집단발생, 면역저하자·중장년 남성\n'
         '배지: BCYE (Buffered Charcoal Yeast Extract) — 시스테인·철 공급 필수\n'
         '임상: 발열·오한·근육통 → 폐렴 ± 설사·혼돈(레지오넬라증)\n'
         '※ "냉각탑·가습기 노출 + 폐렴 + BCYE 배지" → Legionella'),

        ('9', 'S. pyogenes 합병증 — 사구체신염·심내막염·성홍열',
         '2021·2023·2024 (3년)',
         '급성 사구체신염: GAS 인후염 후 2-3주 → 면역복합체 침착 (제3형 과민반응)\n'
         '류마티스열: GAS 인후염 후 심장판막 침범 → 추후 심내막염 위험\n'
         '세균성 심내막염: 류마티스열 과거력 + 치과처치 → viridans group streptococci\n'
         '성홍열: 발열외독소(erythrogenic toxin) → 딸기혀 + 전신홍반 + 인두통\n'
         '배양: β용혈, 혈액우무배지 투명 용혈대, 그람양성사슬알균\n'
         '※ 사구체신염 기전 = 면역복합체 (내독소·외독소 직접 손상 아님)'),

        ('10', '피부사상균증 — KOH 도말·균사 확인',
         '2021·2024·2025 (3년)',
         '검사법: KOH 도말 → 각질 용해 → 균사(hyphae)/포자 직접 확인\n'
         '피부사상균 감별: Trichophyton (대·소분생자), Microsporum (큰 대분생자)\n'
         'lactophenol cotton blue 염색: 대분생자(검은 화살)+소분생자(빨간 화살)\n'
         '치료: 스테로이드+항균제 혼합연고 → 악화! (스테로이드가 진균 증식 촉진)\n'
         'KOH 양성 소견: 실모양 균사(thread-like hyphae)\n'
         '※ 자낭포자·접합포자·담자포자는 피부사상균의 번식체가 아님 (오답)'),

        ('11', 'Th1 분화 사이토카인 IL-12 / 과민반응 제1형',
         '2021·2023·2024 / 2021·2024·2025 (각 3년)',
         '[Th1 분화] 나이브 T세포 → IL-12(수지상세포·대식세포 분비) → Th1\n'
         '→ Th1 기능: IFN-γ 분비 → 대식세포 활성화 → 세포내 기생세균 제거\n'
         '→ 화살표 A = IL-12 (매년 동일 그림 패턴으로 출제)\n'
         '→ 오답: IL-2(증식), IL-4(Th2), IL-17(Th17), IL-23(Th17 유지)\n'
         '[제1형 과민반응] IgE → 비만세포/호염기구 탈과립 → 히스타민·류코트리엔\n'
         '→ 임상: 이전 노출 후 재노출 시 즉각 반응 — 두드러기·호흡곤란·저혈압\n'
         '→ 제2형(항체매개), 제3형(면역복합체), 제4형(지연형 T세포) 구분 필수\n'
         '※ 아나필락시스 = 제1형 / GAS 사구체신염 = 제3형 / 결핵 TST = 제4형'),
    ]

    for no, title, years, desc in top_bact:
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

    # ── 섹션 3: ★★ 준빈출 — 미생물학·면역학 ────────────────
    story.append(PageBreak())
    story.append(Paragraph('★★ 준빈출 유형 — 미생물학·면역학 (2년 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    hdr = ['유형', '핵심 포인트', '출제연도']
    micro_data = [hdr] + [
        ['협막 India ink\n(음성염색)',
         '포식세포 식작용 회피가 주기능 — 면역원이 아님\n'
         '→ India ink: 배경 검게, 협막 투명하게 보임 (음성염색)\n'
         '→ Cryptococcus: 뇌막염, 라텍스 응집검사, 면역억제 환자',
         '2021·2023'],
        ['외피 유무와\n소독제 감수성',
         '외피(+): 알코올·비누에 감염력 소실 (SARS-CoV-2, HSV, CMV)\n'
         '외피(-): 소독제 저항성 (노로, HPV, 아데노, 폴리오)\n'
         '→ "알코올 소독 효과 없는 바이러스" = 외피 없는 바이러스',
         '2021·2023'],
        ['형질도입\n(Transduction)',
         '박테리오파지가 한 세균의 유전자를 다른 세균으로 전달\n'
         '→ 항균제 내성 유전자·독소 유전자 수평 전파\n'
         '→ 접합(conjugation)=성선모, 형질전환(transformation)=유리DNA',
         '2021·2025'],
        ['C. difficile\n위막성대장염',
         '항균제(퀴놀론·클린다마이신 등) 복용 후 설사 → 항균제 중단 후 악화\n'
         '→ 내시경: 장점막 위 황갈색·회백색 플라크\n'
         '→ 치료: 메트로니다졸 또는 반코마이신 경구',
         '2021·2023'],
        ['수막알균\n(N. meningitidis)',
         '그람음성 쌍알균, 뇌척수액에서 검출 → 세균성 수막염\n'
         '→ 병원성 인자: 협막 다당류 = 백신의 주성분\n'
         '→ Por 단백(오답), 섬모(오답), 지질테이코산(오답) 주의',
         '2021·2024'],
        ['EHEC\n(장출혈성대장균)',
         'Shigella dysenteriae 독소와 유사한 Shiga-like toxin 분비\n'
         '→ 출혈성 장관염 + 용혈요독증후군(HUS)\n'
         '→ EIEC(세포침입), ETEC(장독소), EPEC(부착), EAEC(응집) 감별',
         '2023·2024'],
        ['Chlamydia\ntrachomatis',
         '절대세포내 기생세균, 세포내 봉입체(inclusion body) 형성\n'
         '→ 신생아: 산도 통과 시 감염 → 스타카토성 기침, 간질성 폐렴\n'
         '→ 배양: McCoy 세포, Giemsa·요오드 염색으로 봉입체 확인',
         '2023·2024'],
        ['Salmonella\n(계란·식중독)',
         '계란·닭고기 오염, 맥콩키우무배지에서 무색 집락 (젖당 비분해)\n'
         '→ 복통·설사·발열 24~72시간 후 발병\n'
         '→ Typhoid(장티푸스)와 구별: 비장증대·장미반·지속발열',
         '2024·2025'],
        ['HSV 잠복감염\n(삼차신경절)',
         '입술 수포, 과로·면역저하 시 재발, acyclovir로 호전\n'
         '→ 잠복: 바이러스 DNA가 삼차신경절 신경세포에 존재\n'
         '→ 비리온·외피·캡시드가 존재하는 게 아님 (오답 주의)',
         '2021·2025'],
        ['Candida albicans\n(가성균사)',
         '질 감염: 흰색 두부 같은 분비물 + 가려움 → KOH 도말\n'
         '→ 가성균사(pseudohyphae): 진짜 균사 아님, 세포 연결된 형태\n'
         '→ 피부 감염 시에도 KOH에서 가성균사 확인 가능',
         '2021·2023'],
        ['수족구병\n(coxsackievirus)',
         '소아 여름철, 손·발·입 수포성 병변 + 발열\n'
         '→ RNA 바이러스, 산안정성(acid-stable), 분변-경구 전파\n'
         '→ 헤르판지나: 구개·편도 수포 (손발 병변 없음)와 구별',
         '2021·2025'],
        ['HPV — 자궁경부암',
         'Koilocytosis(공포세포): HPV 감염의 조직학적 특징\n'
         '→ 상피기저막 파괴 + 게놈 숙주세포 통합 → 암유전자 발현\n'
         '→ 고위험군: 16·18형(자궁경부암) / 저위험군: 6·11형(사마귀)',
         '2021·2025'],
        ['NK세포',
         'CD16+CD56+CD3−, 큰 과립성 림프구, IFN-γ 분비\n'
         '→ MHC class I 감소된 세포(바이러스 감염·종양) 표적 공격\n'
         '→ ADCC(항체의존세포매개세포독성) 반응 가능',
         '2021·2025'],
        ['VZV 대상포진\n(50세+ 백신)',
         '후근신경절 잠복 → 면역저하·고령 시 재활성 → 신경 분절 수포\n'
         '→ 다핵세포, 핵내봉입체, 조직검사 소견\n'
         '→ 백신 접종 권고: 50세 이상 성인 (임산부·건강한 소아 아님)',
         '2023·2025'],
        ['A형·E형 간염\n(대변-구강)',
         'A형 간염: ssRNA(+), 대변-구강 경로, 급성 간염\n'
         'E형 간염: ssRNA(+), 대변-구강, 임신부 중증화 위험\n'
         '→ B·C·D형 간염: 혈액·성접촉·수직감염 (대변-구강 아님)',
         '2021·2025'],
        ['수지상세포',
         '전문항원제시세포(professional APC) — 넓은 표면적\n'
         '미성숙: 항원 탐식·인지 우수 / 성숙: MHC II 발현↑, 림프절 이동\n'
         '→ 랑게르한스세포: 피부 표피의 수지상세포',
         '2023·2024'],
    ]

    col_w = [36*mm, 104*mm, 24*mm]
    t3 = Table(micro_data, colWidths=col_w, repeatRows=1)
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'NanumGothicBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'NanumGothic'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f4f6fb')]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c0c8e0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t3)

    doc.build(story)
    print(f'PDF 생성 완료: {output_path}')


if __name__ == '__main__':
    build_pdf('/home/user/Gjp/기종평_5교시_빈출유형_분석.pdf')
