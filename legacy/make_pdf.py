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

# 스타일 정의
def make_styles():
    title_style = ParagraphStyle(
        'Title', fontName='NanumGothicBold', fontSize=16,
        textColor=colors.HexColor('#1a1a2e'), spaceAfter=6, spaceBefore=4,
        leading=22, alignment=1  # center
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
    story.append(Paragraph('1교시 빈출 유형 분석', s['title']))
    story.append(Paragraph('2021 · 2023 · 2024 · 2025년도', s['subtitle']))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#0f3460')))
    story.append(Spacer(1, 6*mm))

    # ── 섹션 1: 최빈출 유형 ────────────────────────────────
    story.append(Paragraph('★★★ 최빈출 유형 (3~4년 연속 출제)', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    top_items = [
        ('1', '쿠싱증후군 — 코티솔 분비 부위',
         '2021·2023·2024·2025 (4년 전부)',
         '얼굴/목/가슴 지방 축적 + 자주색 복부 줄무늬 + 근위축\n'
         '→ 덱사메타손 억제검사 코티솔 초과\n'
         '→ 부신겉질 다발층(zona fasciculata)에서 코티솔 분비\n'
         '※ 매년 문구 거의 동일, 조직사진 A~E 중 선택'),

        ('2', '보행 시 골반 유지 근육',
         '2021·2023·2025',
         '걸을 때 한쪽 다리를 들어올릴 때 골반이 기울어지지 않도록 지지\n'
         '→ 중간볼기근(gluteus medius)\n'
         '※ sartorius, piriformis, gluteus maximus, quadriceps를 오답으로 제시'),

        ('3', '왼심방·왼심실 뒤벽 심근경색 — 관련 동맥',
         '2021·2024',
         '→ 휘돌이가지(circumflex branch) 막힘'),

        ('4', '이자머리 절제 후 이자몸통/꼬리 혈액공급 동맥',
         '2021·2024',
         '→ 지라동맥(splenic artery)'),

        ('5', '자궁절제술 후 소변량 감소 — 손상 구조물',
         '2023·2024',
         '자궁동맥 결찰 과정에서 손상\n→ 요관(ureter)'),

        ('6', '자궁동맥의 직접 기원 동맥',
         '2021·2024',
         '→ 속엉덩동맥(internal iliac artery)'),

        ('7', '발목 안쪽번짐(inversion) 손상',
         '2021·2024',
         '→ 앞목말종아리인대(anterior talofibular ligament)'),

        ('8', '귀밑샘 종양 절제 — 손상되기 쉬운 신경',
         '2021·2025',
         '→ 얼굴신경(facial nerve)'),

        ('9', '신경능선(neural crest) 유래 구조물',
         '2024·2025',
         '→ 부신속질(adrenal medulla)\n'
         '※ 망막·표피·심장막·속귀 막미로는 오답'),

        ('10', '배꼽탈장 선천기형 — 발생 기전',
         '2021·2023',
         '창자가 양막에 싸인 채 탯줄 쪽으로 탈출\n'
         '→ 생리적배꼽탈장(physiological umbilical hernia)이 복귀되지 않음'),

        ('11', '중간대뇌동맥 동맥류 — 출혈이 모이는 공간',
         '2021·2023',
         '극심한 두통, 갑자기 쓰러짐\n→ 거미막밑공간(subarachnoid space)'),

        ('12', '혈액뇌장벽(BBB) — 세포 A 식별',
         '2021·2024·2025',
         '혈관 주위를 감싸는 세포\n→ 별아교세포(astrocyte)'),

        ('13', '지라 현미경 — 적혈구 파괴 장소',
         '2021·2023',
         '→ 적색수질(red pulp)'),

        ('14', '출산 통증 신경차단마취 — 마취 신경',
         '2021·2023',
         '궁둥뼈가시 촉지 후 엉치가시인대 주위 주사\n→ 음부신경(pudendal nerve)'),

        ('15', '대상포진 얼굴 병변 — 분포 신경',
         '2021·2024',
         '이마·눈 주위 대상포진\n→ 눈신경(ophthalmic nerve, 삼차신경 1분지)'),
    ]

    for no, title, years, desc in top_items:
        # 번호+제목 행
        row_data = [[
            Paragraph(f'<b>{no}.</b>', s['body']),
            Paragraph(f'<b>{title}</b>', s['h2']),
            Paragraph(years, s['small'])
        ]]
        t = Table(row_data, colWidths=[8*mm, 110*mm, 46*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8f0fe')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#c0c8e0')),
            ('ROUNDEDCORNERS', [3]),
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
        ['정세관 — 테스토스테론 합성 세포', 'Leydig cell (간질세포)', '2021, 2025'],
        ['혈액고환장벽 형성 세포', 'Sertoli cell (버팀세포)', '2023, 2024'],
        ['표면활성물질 분비 세포', '2형 폐포세포 (Type II pneumocyte)', '2023, 2024'],
        ['ADH 합성 부위', '시상하부(hypothalamus)', '2023, 2024'],
        ['갑상샘 절제 후 저칼슘 증상', '부갑상샘 으뜸세포(chief cell) 제거', '2021, 2024'],
        ['소화관 조직 식별', 'Brunner샘→샘창자 / Peyer판→돌창자', '2021, 2023'],
        ['콩팥 사구체옆장치 기능', '레닌 분비(사구체옆세포) / NaCl 감지(치밀반점)', '2021·2023·2024'],
        ['식도 좁아짐 — 커진 심장 부위', '왼심방(left atrium)', '2021, 2024'],
        ['팔꿉 골절 — 갈고리손 변형', '자신경(ulnar nerve) 손상', '2021, 2024'],
        ['손목굴증후군 — 관련 신경', '정중신경(median nerve) + 엄지두덩 위축', '2023, 2024'],
        ['뇌혈관조영술 — 혈전 위치', '임상 증상과 혈관 매칭', '2021, 2024'],
        ['조직 내 단백/mRNA 위치 확인 실험기법', 'IHC = 단백질 / In situ hybridization = mRNA', '2021, 2024'],
    ]

    col_w = [65*mm, 72*mm, 30*mm]
    t2 = Table(table_data, colWidths=col_w, repeatRows=1)
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f3460')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'NanumGothicBold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTNAME', (0,1), (-1,-1), 'NanumGothic'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f4f6fb')]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#c0c8e0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t2)

    # ── 섹션 3: 주제별 핵심 정리 ───────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('주제별 핵심 포인트 요약', s['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 2*mm))

    sections = [
        ('해부학', [
            '심장: 청진 위치 암기, 경색-동맥 매칭, 식도 압박 = 왼심방',
            '복부: 이자 혈공급=지라동맥, 자궁동맥=속엉덩동맥, 자궁절제=요관 손상 주의',
            '하지: 중간볼기근(보행), 앞목말종아리인대(내번), 앞/뒤십자인대 감별',
            '상지: 자신경(갈고리손), 정중신경(손목굴), 겨드랑신경(외과목 골절)',
        ]),
        ('신경해부학', [
            '출혈 공간: 동맥류=거미막밑, 경막동맥=경막바깥, 교정맥=경막밑',
            '대뇌겉질: 청각=위관자이랑, 언어산출=이마엽(브로카), 무시=뒤마루엽',
            '뇌신경: 귀밑샘=얼굴신경, 대상포진=눈신경, 음부신경=출산마취',
            '속섬유막 뒷다리 경색 → 반대쪽 얼굴+사지 운동 장애',
        ]),
        ('조직학', [
            '세포 식별: Purkinje cell(소뇌), Leydig cell(테스토스테론), Sertoli cell(장벽), Type II(surfactant)',
            '노화 산물: 지질갈색소(lipofuscin)',
            '랑게르한스세포: Birbeck granule → 항원제시 기능',
            '지라 적색수질 = 적혈구 파괴 / 백색수질 = 면역반응',
        ]),
        ('발생학', [
            '배꼽탈장(omphalocele): 생리적탈장 복귀 실패, 양막에 싸임',
            '신경능선: 부신속질, 척수신경절, 뇌신경 감각절 유래',
            '착상 시기: 수정 후 6일경 (blastocyst)',
            '기관형성 민감기: 발생 4~8주차 (선천기형 발생 위험 최대)',
        ]),
        ('내분비', [
            '쿠싱증후군: 부신겉질 다발층 → 코티솔 과분비',
            'ADH(항이뇨호르몬): 시상하부 합성 → 뇌하수체 뒤엽 분비',
            '갑상샘 절제 합병증: 부갑상샘 으뜸세포 제거 → 저칼슘혈증, 근육 경련',
            '알도스테론: 부신겉질 사구층 분비 (레닌-안지오텐신계)',
        ]),
    ]

    for sec_title, bullets in sections:
        story.append(Paragraph(sec_title, s['h2']))
        for b in bullets:
            story.append(Paragraph('• ' + b, s['bullet']))
        story.append(Spacer(1, 2*mm))

    # ── 섹션 4: 시험 전략 ──────────────────────────────────
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#0f3460')))
    tip_data = [[
        Paragraph('<b>시험 전략 TIP</b>', s['h2']),
        Paragraph(
            '쿠싱증후군/코티솔 · 중간볼기근 · 이자-지라동맥 · 자궁동맥-속엉덩동맥 · '
            '발목 앞목말종아리인대 · 음부신경 마취는 매년 거의 동일한 문구로 출제됩니다. '
            '조직 사진 문제는 A~E 중 선택하는 형태가 많으며, '
            '임상 증상과 연결하는 연습이 핵심입니다.',
            s['note']
        )
    ]]
    tip_t = Table(tip_data, colWidths=[28*mm, 136*mm])
    tip_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff8e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f9a825')),
    ]))
    story.append(tip_t)

    doc.build(story)
    print(f'PDF 생성 완료: {output_path}')

if __name__ == '__main__':
    build_pdf('/home/user/Gjp/기종평_1교시_빈출유형_분석.pdf')
