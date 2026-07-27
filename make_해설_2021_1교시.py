#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2021년도 기초의학종합평가 1교시(해부학/조직학/발생학) 문항별 해설 PDF 생성"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('NanumGothic', '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'))
pdfmetrics.registerFont(TTFont('NanumGothicBold', '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'))

CIRCLED = {1: '①', 2: '②', 3: '③', 4: '④', 5: '⑤'}


def make_styles():
    return {
        'title': ParagraphStyle('Title', fontName='NanumGothicBold', fontSize=18,
            textColor=colors.HexColor('#1a1a2e'), spaceAfter=6, leading=24, alignment=1),
        'subtitle': ParagraphStyle('Subtitle', fontName='NanumGothic', fontSize=11,
            textColor=colors.HexColor('#555555'), spaceAfter=10, leading=15, alignment=1),
        'subject': ParagraphStyle('Subject', fontName='NanumGothicBold', fontSize=13,
            textColor=colors.white, spaceAfter=6, spaceBefore=10, leading=18,
            backColor=colors.HexColor('#0f3460'), borderPad=6, leftIndent=4),
        'qnum': ParagraphStyle('Qnum', fontName='NanumGothicBold', fontSize=10.5,
            textColor=colors.HexColor('#16213e'), spaceAfter=2, spaceBefore=8, leading=15),
        'ans': ParagraphStyle('Ans', fontName='NanumGothicBold', fontSize=10,
            textColor=colors.HexColor('#c0392b'), spaceAfter=2, leading=14),
        'exp': ParagraphStyle('Exp', fontName='NanumGothic', fontSize=9,
            textColor=colors.HexColor('#333333'), spaceAfter=3, leading=13.5, leftIndent=4),
    }


# (문항번호, 과목, 정답번호, 문제요약, 해설)
DATA = [
    ("해부학·조직학·발생학 (조직·내분비)", None, None, None, None),
    (1, None, 1, "저·고배율 조직사진, 분비 호르몬은?",
     "사진은 <b>이자섬(랑게르한스섬)</b> 조직으로, 세포끈이 모세혈관 사이에 배열된 내분비섬 구조가 특징이다. "
     "이자섬의 β세포가 <b>인슐린</b>을 분비하므로 정답은 ①. 갑상샘(티록신)은 소포(follicle)에 콜로이드가 채워진 형태로 감별된다."),
    (2, None, 3, "오른다리 통증·온도감각 소실, 척수 눌림 신경로는?",
     "바늘·뜨거운 물(통각·온도각)의 소실은 <b>가쪽척수시상로(lateral spinothalamic tract)</b> 장애다. "
     "이 경로는 반대쪽으로 교차하여 상행하므로, 척수 눌림 부위 반대편 팔다리의 통·온각이 떨어진다. 정답 ③."),
    (3, None, 2, "날개목·작은키·손발 림프부종 → 진단은?",
     "날개모양 목(webbed neck)·저신장·림프부종은 <b>터너증후군(45,X)</b>의 전형적 소견이다. 정답 ②. "
     "클라인펠터(47,XXY)는 큰 키·불임 남성, 다운(21삼염색체)은 지적장애·특징적 얼굴로 감별된다."),
    (4, None, 1, "뇌 관상면 별표 회색질 부위는?",
     "속섬유막 가쪽에 위치한 렌즈핵의 바깥 부분 회색질은 <b>조가비핵(putamen)</b>이다. 정답 ①. "
     "꼬리핵은 가쪽뇌실을 따라 굽은 형태, 속섬유막은 흰색질(신경섬유)로 구분된다."),
    (5, None, 5, "소뇌겉질에서 화살표가 가리키는 세포는?",
     "소뇌겉질 조롱박세포층(Purkinje layer)에 한 줄로 배열된 크고 플라스크 모양의 세포가 <b>조롱박세포(Purkinje cell)</b>다. 정답 ⑤. "
     "분자층의 별세포·바구니세포, 과립층의 과립세포와 위치로 감별한다."),
    (6, None, 2, "심장막마찰음·왼어깨·목 방사통 관련 신경은?",
     "섬유심장막·벽쪽장막심장막은 <b>가로막신경(phrenic nerve, C3~5)</b>이 분포한다. 같은 분절의 목·어깨 피부로 연관통이 나타난다. 정답 ②."),
    (7, None, 2, "정세관 조직, 테스토스테론 합성 세포는?",
     "테스토스테론은 정세관 <b>사이(간질)의 leydig세포(사이질세포)</b>가 합성한다. 사진에서 정세관 바깥 사이질에 위치한 세포(B)가 정답 ②. "
     "정세관 안쪽 sertoli세포는 지지·영양 기능을 한다."),
    (8, None, 1, "허혈성 괴사·쓸개즙 울혈이 먼저 나타나는 구역은?",
     "간샘꽈리에서 <b>허혈·저산소에 가장 취약한 곳은 중심정맥 주위(3구역)</b>이라 여기서 괴사가 먼저 시작된다. "
     "반면 쓸개즙 울혈은 <b>문맥 주위(1구역)</b>에서 먼저 나타난다. 사진 표지에 맞춰 정답 ① (A–B)."),
    (9, None, 2, "얼굴신경 손상으로 소리전달 영향받은 구조물은?",
     "얼굴신경은 <b>등자근(stapedius)</b>을 지배한다. 마비 시 등자근이 등자뼈를 고정하지 못해 소리가 과도하게 크게 들리는 청각과민(hyperacusis)이 생긴다. "
     "따라서 소리전달에 영향받은 구조물은 <b>등자뼈(stapes)</b>. 정답 ②."),
    (10, None, 1, "이자 몸통·꼬리에 혈액 공급하는 동맥은?",
     "이자머리는 위·아래이자샘창자동맥이, <b>이자 몸통·꼬리는 지라동맥(splenic artery)</b>의 이자가지가 공급한다. "
     "머리 절제 후 남긴 몸통·꼬리의 혈류는 지라동맥이 담당하므로 정답 ①."),
    (11, None, 5, "노화세포에 축적된 산화 물질은?",
     "지질·인지질이 산화되어 축적된 갈색 색소는 <b>지질갈색소(lipofuscin)</b>로, '소모색소'라 불리며 노화·위축 세포에서 흔하다. 정답 ⑤. "
     "혈철소는 철(Fe) 함유 색소로 감별된다."),
    (12, None, 1, "왼심방·왼심실 뒤벽 심근경색, 막힌 동맥은?",
     "왼심장동맥의 <b>휘돌이가지(circumflex branch)</b>가 왼심방·왼심실의 뒤·가쪽벽을 공급한다. 정답 ①. "
     "앞심실사이가지는 앞벽·심실사이막을, 오른심장동맥은 아래벽을 담당한다."),
    (13, None, 3, "연골·샘·술잔세포 없고 민무늬근 관찰되는 전도부는?",
     "연골·샘·술잔세포가 사라지고 단층 입방/원주상피와 민무늬근만 뚜렷한 부위는 <b>종말세기관지(terminal bronchiole)</b>다. 사진의 C가 정답 ③."),
    (14, None, 5, "난소동맥을 포함하는 구조물은?",
     "난소동맥은 <b>난소걸이인대(suspensory ligament of ovary, 깔때기골반인대)</b> 안을 지나 난소로 간다. 사진의 E가 정답 ⑤. "
     "난소 고유인대에는 난소동맥가지가 지나지만 본줄기는 걸이인대에 있다."),
    (15, None, 2, "척수-근육 연관 그림, 별표 부위 용어는?",
     "하나의 운동신경세포와 그것이 지배하는 모든 근섬유를 합쳐 <b>운동단위(motor unit)</b>라 한다. 정답 ②. "
     "운동종말판은 신경-근육 접합부 그 자체만을 가리킨다."),
    (16, None, 3, "두덩뼈가지 아래 붙어 발기에 관여하는 구조물은?",
     "음경해면체의 뒤쪽 갈라진 부분이 두덩활 아래에 붙는데 이를 <b>음경다리(crus of penis)</b>라 하며 궁둥해면체근이 덮는다. 정답 ③. "
     "음경망울은 요도해면체의 팽대부다."),
    (17, None, 1, "허파 조직에서 꽈리큰포식세포는?",
     "꽈리큰포식세포(먼지세포)는 꽈리안 표면에 자유롭게 놓인 크고 세포질이 풍부한 세포로 관찰된다. 사진의 A가 정답 ①."),
    (18, None, 3, "긴엄지폄근힘줄 가쪽 맥박 약화, 폐쇄 의심 동맥은?",
     "발등에서 긴엄지폄근힘줄 가쪽으로 만지는 맥박은 <b>발등동맥</b>으로, 이는 <b>앞정강동맥(anterior tibial artery)</b>의 연속이다. 정답 ③. "
     "당뇨·고혈압에 의한 말초동맥질환을 시사한다."),
    (19, None, 2, "소변량·나트륨 감지하여 혈류 조절하는 콩팥 부위는?",
     "먼쪽곱슬세관이 자기 토리로 접하는 곳의 <b>치밀반점(macula densa)</b>이 세관 내 Na⁺ 농도를 감지해 토리곁장치를 통해 혈류를 조절한다. 사진의 B가 정답 ②."),
    (20, None, 2, "혈액뇌장벽 그림에서 A로 표시된 세포는?",
     "모세혈관을 발돌기로 감싸며 혈액뇌장벽 형성에 관여하는 세포는 <b>별아교세포(astrocyte)</b>다. 정답 ②. "
     "실제 장벽은 내피세포의 치밀이음부지만, 별아교세포 발돌기가 이를 유도·유지한다."),

    ("해부학 (팔다리·발생·머리)", None, None, None, None),
    (21, None, 1, "팔꿉 골절 후 갈퀴손·손 안쪽 감각소실, 손상 신경은?",
     "손 안쪽(새끼손가락쪽) 감각소실과 갈퀴손(claw hand)은 <b>자신경(ulnar nerve)</b> 손상의 특징이다. 정답 ①. "
     "팔꿉 안쪽(위관절융기 뒤)에서 표면을 지나 손상되기 쉽다."),
    (22, None, 3, "수정 과정 그림, 화살표가 가리키는 것은?",
     "난자 바깥을 방사상으로 둘러싼 난포세포층이 <b>부챗살세포(corona radiata)</b>다. 정답 ③. "
     "투명층은 난자와 부챗살세포 사이의 무세포성 당단백질층이다."),
    (23, None, 4, "복부 CT에서 별표 장기는?",
     "가로막 아래 좌우 뒤쪽 복막뒤공간에 위치한 콩모양 장기는 <b>콩팥(kidney)</b>이다. 상대적 위치·모양으로 정답 ④."),
    (24, None, 3, "중간대뇌동맥 동맥류 파열, 혈액이 모이는 공간은?",
     "뇌바닥 동맥류 파열 시 혈액은 거미막과 연질막 사이 <b>거미막밑공간(subarachnoid space)</b>에 고인다(거미막밑출혈). 정답 ③. "
     "'벼락두통'이 전형적 증상이다."),
    (25, None, 4, "걸을 때 골반을 기울여 반대쪽 다리를 드는 근육은?",
     "디딤다리 쪽 <b>중간볼기근(gluteus medius)</b>이 골반을 수평으로 잡아 반대쪽 다리를 들 수 있게 한다. 마비 시 Trendelenburg 징후가 나타난다. 정답 ④."),
    (26, None, 5, "발목 안쪽들림(inversion) 손상 시 다치는 구조물은?",
     "안쪽들림 손상에서 가장 잘 다치는 것은 가쪽 인대 중 <b>앞목말종아리인대(anterior talofibular ligament)</b>다. 정답 ⑤. "
     "세모인대는 반대로 가쪽들림에서 손상된다."),
    (27, None, 1, "귀밑샘 종양 절제 시 가장 손상되기 쉬운 신경은?",
     "<b>얼굴신경(facial nerve)</b>이 귀밑샘 실질을 가로질러 얕은엽·깊은엽으로 나누므로 절제 중 가장 손상되기 쉽다. 정답 ①."),
    (28, None, 1, "희소돌기아교세포 MBP 염색과 같은 패턴 보이는 구조는?",
     "MBP(말이집바탕단백)는 말이집 성분이고, 중추에서 희소돌기아교세포가 <b>축삭(axon)</b>을 말이집으로 감싼다. 따라서 축삭을 따라 염색된다. 정답 ①."),
    (29, None, 4, "가슴 방사선에서 화살표 구조물은?",
     "기관지나무 위치·주행을 고려할 때 화살표는 <b>아래엽기관지(inferior lobar bronchus)</b>에 해당한다. 정답 ④."),
    (30, None, 4, "오른쪽 얼굴·팔 마비, 혈전 예상 위치는?",
     "오른얼굴·팔의 마비·감각소실은 왼쪽 중간대뇌동맥 영역 병변을 시사한다. 뇌혈관조영에서 해당 동맥의 혈전 위치(D)가 정답 ④."),
    (31, None, 3, "쿠싱징후(자주색 줄무늬·근위축)+코티솔↑, 호르몬 분비 위치는?",
     "덱사메타손 억제에도 코티솔↑은 <b>쿠싱증후군</b>이다. 코티솔은 부신겉질 <b>다발층(zona fasciculata)</b>에서 분비되므로, 조직사진의 해당 부위(C)가 정답 ③."),
    (32, None, 2, "자궁관 속공간을 덮는 상피는?",
     "자궁관 점막은 섬모가 있는 <b>단층원주상피(simple columnar epithelium)</b>로 덮여 있어 난자를 이동시킨다. 정답 ②."),
    (33, None, 1, "간 내장면에서 위와 맞닿는 부분은?",
     "간 왼엽 내장면의 오목한 <b>위자국(gastric impression)</b>이 위와 맞닿는다. 사진의 A가 정답 ①."),
    (34, None, 5, "창자가 양막에 싸여 탯줄로 탈출한 기형의 기전은?",
     "양막에 싸인 창자가 탯줄바닥으로 탈출한 것은 <b>배꼽탈장(omphalocele)</b>이며, <b>생리적 배꼽탈장이 복강으로 복귀하지 못한</b> 것이 기전이다. 정답 ⑤. "
     "배벽갈림증(gastroschisis)은 막이 없다는 점에서 감별된다."),
    (35, None, 3, "소화계통 장기 조직사진, 이 장기는?",
     "점막에 큰 림프소절 무리(파이어판, Peyer's patch)가 특징적으로 보이면 <b>돌창자(ileum)</b>다. 정답 ③. "
     "샘창자는 브루너샘, 빈창자는 긴 돌림주름으로 감별한다."),
    (36, None, 3, "도르래신경 마비, 겹보임이 심해지는 동작은?",
     "도르래신경은 위빗근을 지배하며 위빗근은 모음 상태에서 눈을 <b>아래로</b> 내린다. 마비 시 <b>아래쪽을 볼 때</b> 복시가 심해져 계단을 내려갈 때 어려움을 겪는다. 정답 ③."),
    (37, None, 4, "허리통증, 별표 피부분절 부위의 척수는?",
     "그림의 별표 위치(대개 다리 가쪽·발등)에 해당하는 피부분절은 <b>L5</b>다. 정답 ④."),
    (38, None, 5, "권투 샌드백 타격 후 골절이 흔한 부위는?",
     "주먹으로 치다가 흔히 골절되는 곳은 <b>다섯째 손허리뼈 목(권투가골절, boxer's fracture)</b>이다. 사진의 E가 정답 ⑤."),
    (39, None, 2, "어깨관절이 구조적으로 가장 흔히 탈구되는 방향은?",
     "어깨관절은 아래쪽에 돌림근띠 보강이 없어 <b>구조적으로 아래(inferior)</b>가 가장 약하다. 정답 ②. "
     "(임상적으로 실제 탈구는 앞아래쪽으로 자주 일어나지만, 구조적 취약성을 묻는 문항이다.)"),
    (40, None, 3, "엄지 손목손허리관절의 관절 종류는?",
     "엄지의 손목손허리관절은 큰마름뼈–첫째손허리뼈 사이의 <b>안장관절(saddle joint)</b>로, 맞섬(opposition)을 포함한 자유로운 운동이 가능하다. 정답 ③."),

    ("해부학·조직학 (면역·콩팥·머리목·순환)", None, None, None, None),
    (41, None, 5, "백신 접종 후 T세포에 항원을 제시하는 세포는?",
     "가장 강력한 전문 항원제시세포는 <b>가지세포(dendritic cell)</b>다. 사진 28-5가 가지 돌기가 뻗은 형태로 정답 ⑤."),
    (42, None, 2, "대상포진(얼굴), 바이러스가 잠복했던 곳은?",
     "얼굴(특히 눈 주위) 대상포진은 삼차신경 신경절 중 <b>눈신경(ophthalmic nerve, V1)</b>에 잠복한 수두-대상포진 바이러스의 재활성이다. 정답 ②."),
    (43, None, 2, "단층입방상피·솔가장자리(brush border)가 뚜렷한 부위는?",
     "긴 미세융모로 솔가장자리를 이루어 재흡수에 특화된 콩팥 부위는 <b>토리쪽곱슬세관(proximal convoluted tubule)</b>이다. 사진의 B가 정답 ②."),
    (44, None, 1, "처음부터 복막 뒤에서 발달하는 일차복막뒤장기는?",
     "<b>콩팥</b>은 발생 초기부터 복막 뒤에 위치하는 일차복막뒤장기다. 정답 ①. "
     "이자·샘창자·오름·내림잘록창자는 나중에 붙는 이차복막뒤장기다."),
    (45, None, 1, "과체중아(거대아) 출산 확률이 높은 산모는?",
     "<b>당뇨병 산모</b>는 태아 고인슐린혈증으로 거대아(macrosomia) 위험이 높다. 정답 ①. "
     "흡연·음주·혈액순환장애는 오히려 저체중아와 연관된다."),
    (46, None, 2, "더부신경 손상 시 움직이기 어려운 근육은?",
     "더부신경(CN XI)은 <b>등세모근(trapezius)</b>과 목빗근을 지배한다. 손상 시 어깨 으쓱임·팔 올림이 어려워진다. 정답 ②."),
    (47, None, 3, "간문맥 찢김 시 그물막구멍 뒤에서 함께 손상될 구조물은?",
     "그물막구멍(Winslow공)의 <b>뒤경계는 아래대정맥(IVC)</b>이다(앞: 간문맥·앞: 간십이지장인대). 간문맥 손상 시 뒤쪽 아래대정맥이 함께 다칠 수 있다. 정답 ③."),
    (48, None, 3, "분비물 분류·농축·당단백 합성에 중요한 소기관은?",
     "분비단백을 분류·농축·수식(당화)하는 소기관은 <b>골지체(Golgi apparatus)</b>다. 사진의 C가 정답 ③."),
    (49, None, 2, "nephrin으로 구성되어 여과를 제한하는 콩팥 구조는?",
     "발세포 발돌기 사이의 <b>여과틈새막(slit diaphragm)</b>이 nephrin 단백질로 이루어져 큰 분자의 여과를 막는다. 사진의 B가 정답 ②."),
    (50, None, 2, "가골(bone callus) 형성에 중요한 뼈 구조물은?",
     "골절 치유 시 <b>뼈바깥막(periosteum)</b>의 뼈모세포·전구세포가 증식하여 가골을 만든다. 정답 ②."),
    (51, None, 4, "aquaporin-2 mRNA의 조직 내 발현 위치를 확인하는 기법은?",
     "특정 <b>mRNA의 조직 내 위치</b>를 보려면 <b>제자리부합법(in situ hybridization)</b>을 쓴다. 정답 ④. "
     "노던블롯은 정량, 면역조직화학·웨스턴블롯은 단백질을 본다."),
    (52, None, 2, "가로무늬근 TEM에서 A·B·C가 차례로 가리키는 띠는?",
     "어두운 <b>A띠(중앙)</b>, 밝은 <b>I띠(Z선 양쪽)</b>, A띠 가운데 밝은 <b>H띠</b>. 사진 순서에 맞춰 A띠–I띠–H띠, 정답 ②."),
    (53, None, 2, "코막힘·위쪽어금니 통증·중간콧길 부종, 삼출액 고이는 코곁굴은?",
     "<b>위턱굴(maxillary sinus)</b>은 중간콧길로 열리고 위쪽 어금니와 가까워, 염증 시 어금니 통증과 중간콧길 부종이 나타난다. 정답 ②."),
    (54, None, 4, "지라에서 적혈구가 파괴되는 장소는?",
     "수명이 다한 적혈구는 지라의 <b>붉은속질(red pulp)</b>에서 큰포식세포에 의해 파괴된다. 사진의 ④가 정답. "
     "흰속질(white pulp)은 림프구가 모여 면역반응을 담당한다."),
    (55, None, 5, "갑상샘 절제 후 근경련·테타니, 먼저 확인할 물질은?",
     "갑상샘 절제 중 부갑상샘이 함께 손상되면 저칼슘혈증으로 테타니가 생긴다. 먼저 <b>부갑상샘호르몬(PTH)</b>을 확인한다. 정답 ⑤."),
    (56, None, 5, "부착반점 없고 Birbeck과립을 가진 세포(A)의 기능은?",
     "Birbeck 과립을 갖고 각질세포와 부착반점을 이루지 않는 세포는 표피의 <b>랑게르한스세포</b>로, 기능은 <b>항원제시</b>다. 정답 ⑤."),
    (57, None, 3, "자궁동맥의 기원이 되는 동맥은?",
     "자궁동맥은 <b>속엉덩동맥(internal iliac artery)</b>의 앞가지에서 기시한다. 전체자궁절제 시 요관 위를 지나는 자궁동맥 결찰에 주의한다. 정답 ③."),
    (58, None, 1, "바륨삼킴에서 식도를 누른 커진 심장 부위는?",
     "식도는 <b>왼심방</b> 바로 뒤를 지나므로, 왼심방 확장 시 식도가 눌려 좁아진다. 정답 ①."),
    (59, None, 1, "심장 A·B 공간 사이 벽에서 관찰되는 구조는?",
     "A·B가 좌우 심방이면 그 사이 심방사이막에 태아 때 타원구멍의 흔적인 <b>타원오목(fossa ovalis)</b>이 보인다. 정답 ①."),
    (60, None, 1, "궁둥뼈가시 촉지 후 주사, 마취되는 신경은?",
     "궁둥뼈가시·엉치가시인대 주위로 주사하는 신경차단은 <b>음부신경(pudendal nerve)</b> 차단으로, 출산 시 회음부 통증을 완화한다. 정답 ①."),
]


def build_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
        rightMargin=16*mm, leftMargin=16*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = make_styles()
    story = []

    # 표지
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('기초의학종합평가 (KAMC)', s['subtitle']))
    story.append(Paragraph('2021년도 1교시 문항별 해설', s['title']))
    story.append(Paragraph('해부학 · 조직학 · 발생학 (전 60문항)', s['subtitle']))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#0f3460')))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        '※ 사진·그림을 근거로 한 문항은 KAMC 공식 정답지를 기준으로 판단 요지를 정리하였습니다. '
        '각 해설은 정답의 근거와 감별 포인트 중심으로 구성했습니다.', s['exp']))
    story.append(Spacer(1, 3*mm))

    for row in DATA:
        if row[1] is None and row[2] is None:  # 과목 구분 헤더
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph(row[0], s['subject']))
            continue
        num, _subj, ans, q, exp = row
        block = [
            Paragraph(f'{num}. {q}', s['qnum']),
            Paragraph(f'정답 {CIRCLED[ans]}', s['ans']),
            Paragraph(exp, s['exp']),
            HRFlowable(width='100%', thickness=0.4, color=colors.HexColor('#dddddd'), spaceBefore=3, spaceAfter=1),
        ]
        story.append(KeepTogether(block))

    doc.build(story)
    print(f'생성 완료: {output_path}')


if __name__ == '__main__':
    build_pdf('기종평_2021_1교시_해설.pdf')
