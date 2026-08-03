#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""핵심 개념 도해(schematic) 생성기 — 오프라인·자작(저작권 free).

관련 지식 보조용 개념 도해를 matplotlib 로 직접 그려 diagrams/ 에 저장한다.
연도·교시 무관하게 재사용되는 개념 도해이므로 파일명은 개념 키로 관리한다.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, FancyArrow, Ellipse, Polygon, FancyArrowPatch

FONT = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
FONTB = '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'
fm.fontManager.addfont(FONT)
fm.fontManager.addfont(FONTB)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

OUT = 'diagrams'
os.makedirs(OUT, exist_ok=True)
NAVY = '#0f3460'


def _new(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    ax.axis('off')
    return fig, ax


def _save(fig, key):
    p = os.path.join(OUT, f'{key}.png')
    fig.savefig(p, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return p


def spinal_tracts():
    fig, ax = _new(5.2, 3.2)
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.add_patch(Ellipse((5, 3), 8, 5, fc='#f2f4f8', ec='#888', lw=1.2))
    # 나비모양 회색질 (H)
    gray = Polygon([(3.3,4.3),(4.6,3.6),(4.6,2.4),(3.3,1.7),(3.3,2.6),(4.0,3),(3.3,3.4)],
                   closed=True, fc='#b7c4d6', ec='none')
    gray2 = Polygon([(6.7,4.3),(5.4,3.6),(5.4,2.4),(6.7,1.7),(6.7,2.6),(6.0,3),(6.7,3.4)],
                    closed=True, fc='#b7c4d6', ec='none')
    ax.add_patch(gray); ax.add_patch(gray2)
    ax.plot([4.6,5.4],[3,3], color='#b7c4d6', lw=6)
    # 신경로 영역
    ax.add_patch(Ellipse((5, 5.0), 2.0, 0.9, fc='#2e7d32', alpha=.75, ec='none'))   # 뒤섬유단
    ax.add_patch(Ellipse((8.0, 3.0), 0.9, 1.6, fc='#c0392b', alpha=.8, ec='none'))  # 가쪽척수시상로
    ax.add_patch(Ellipse((5.6, 1.1), 1.4, 0.7, fc='#e08a00', alpha=.85, ec='none')) # 앞척수시상로
    ax.annotate('뒤섬유단–안쪽섬유띠\n(미세촉각·진동·고유감각, 동측)', (5,5.0), (0.2,5.7),
                fontsize=8, ha='left', color='#2e7d32',
                arrowprops=dict(arrowstyle='-', color='#2e7d32'))
    ax.annotate('가쪽척수시상로\n(통각·온도각, 교차)', (8.0,3.0), (8.6,4.4),
                fontsize=8, ha='left', color='#c0392b',
                arrowprops=dict(arrowstyle='-', color='#c0392b'))
    ax.annotate('앞척수시상로\n(거친촉각·압각)', (5.6,1.1), (6.6,0.3),
                fontsize=8, ha='left', color='#b5680a',
                arrowprops=dict(arrowstyle='-', color='#b5680a'))
    ax.set_title('척수 단면 — 주요 상행신경로', fontsize=11, color=NAVY, weight='bold')
    return _save(fig, 'spinal_tracts')


def adrenal_zones():
    fig, ax = _new(5.0, 3.4)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    rows = [
        ('피막 (capsule)', '#cfd8dc', ''),
        ('토리층 (zona glomerulosa)', '#a5d6a7', '알도스테론 — 염분(salt)'),
        ('다발층 (zona fasciculata)', '#fff59d', '코티솔 — 당(sugar)'),
        ('그물층 (zona reticularis)', '#ffcc80', '안드로젠 — 성호르몬(sex)'),
        ('속질 (medulla)', '#ef9a9a', '카테콜아민(에피네프린)'),
    ]
    heights = [1.1, 1.9, 2.6, 1.9, 2.5]
    y = 10
    for (name, col, func), h in zip(rows, heights):
        y0 = y - h
        ax.add_patch(Rectangle((0.3, y0), 6.3, h, fc=col, ec='white', lw=1.5))
        ax.text(3.45, y0 + h/2, name, ha='center', va='center', fontsize=8.5, weight='bold')
        if func:
            ax.text(6.9, y0 + h/2, func, ha='left', va='center', fontsize=8.2, color='#333')
        y = y0
    ax.set_title('부신겉질 3층 + 속질  (GFR: salt·sugar·sex)', fontsize=10.5, color=NAVY, weight='bold')
    ax.set_xlim(0, 12); ax.set_ylim(0, 10.6)
    return _save(fig, 'adrenal_zones')


def sarcomere():
    fig, ax = _new(5.4, 2.4)
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.4);
    ax.add_patch(Rectangle((3, 1), 4, 2, fc='#b7c4d6', ec='none'))        # A띠
    ax.add_patch(Rectangle((4.5, 1), 1.0, 2, fc='#e3eaf2', ec='none'))    # H띠
    for x in [1, 9]:
        ax.plot([x, x], [0.6, 3.4], 'k-', lw=2.2)
    ax.plot([5, 5], [1, 3], color='#555', ls='--', lw=1.2)               # M선
    ax.annotate('A띠 (굵은필라멘트·불변)', (5, 3.5), ha='center', fontsize=9, color=NAVY, weight='bold')
    ax.annotate('I띠', (2, 3.5), ha='center', fontsize=9, weight='bold')
    ax.annotate('I띠', (8, 3.5), ha='center', fontsize=9, weight='bold')
    ax.annotate('H띠', (5, 0.55), ha='center', fontsize=8.5)
    ax.annotate('Z선', (1, 0.3), ha='center', fontsize=8)
    ax.annotate('M선', (5.75, 0.55), ha='center', fontsize=8)
    ax.text(5, 4.05, '수축 시 I띠·H띠 짧아짐 · A띠 불변 (활주설)', ha='center', fontsize=8, color='#c0392b')
    ax.set_title('뼈대근육 근절(sarcomere) 구조', fontsize=11, color=NAVY, weight='bold')
    return _save(fig, 'sarcomere')


def filtration_barrier():
    fig, ax = _new(5.2, 3.0)
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.text(5, 5.6, '혈액(모세혈관) 쪽', ha='center', fontsize=8.5, color='#c0392b')
    ax.text(5, 0.25, '소변(보먼공간) 쪽', ha='center', fontsize=8.5, color='#0f3460')
    layers = [
        (4.3, '① 창내피 (fenestrated endothelium)', '#ef9a9a', True),
        (3.0, '② 토리바닥막 (GBM · 음전하 · Ⅳ형 콜라겐)', '#c5e1a5', False),
        (1.7, '③ 발세포 여과틈새막 (nephrin)', '#90caf9', True),
    ]
    for y, label, col, pores in layers:
        ax.add_patch(Rectangle((1.2, y), 7.6, 0.9, fc=col, ec='#666', lw=1))
        ax.text(5, y + 0.45, label, ha='center', va='center', fontsize=8.3, weight='bold')
        if pores:
            for x in [2.2, 3.4, 4.6, 5.8, 7.0, 7.8]:
                ax.plot([x, x], [y, y + 0.9], color='white', lw=2)
    ax.annotate('', (5, 1.5), (5, 4.6), arrowprops=dict(arrowstyle='->', color='#333', lw=1.4))
    ax.set_title('콩팥 토리 여과장벽 3층', fontsize=11, color=NAVY, weight='bold')
    return _save(fig, 'filtration_barrier')


def liver_zones():
    fig, ax = _new(5.4, 2.8)
    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    for i, (col, z) in enumerate([('#a5d6a7', '1구역\n(문맥주위)'),
                                   ('#fff59d', '2구역'),
                                   ('#ef9a9a', '3구역\n(중심정맥주위)')]):
        ax.add_patch(Rectangle((1 + i*3, 1.5), 3, 3, fc=col, ec='white', lw=1.5))
        ax.text(2.5 + i*3, 3, z, ha='center', va='center', fontsize=8.5, weight='bold')
    ax.text(1, 5.0, '문맥굴(산소↑)', fontsize=8.5, color='#2e7d32')
    ax.text(9.2, 5.0, '중심정맥(산소↓)', fontsize=8.5, color='#c0392b')
    ax.annotate('혈류 →', (10, 4.7), (1.2, 4.7), fontsize=8.5, color='#333',
                arrowprops=dict(arrowstyle='->', color='#333'))
    ax.annotate('← 담즙', (1.2, 1.05), (10, 1.05), fontsize=8.5, color='#b5680a',
                arrowprops=dict(arrowstyle='->', color='#b5680a'))
    ax.text(6, 0.35, '허혈·독성(아세트아미노펜)=3구역 먼저 · 담즙울혈=1구역 먼저',
            ha='center', fontsize=7.8, color='#555')
    ax.set_title('간샘꽈리(acinus) 3구역', fontsize=11, color=NAVY, weight='bold')
    return _save(fig, 'liver_zones')


def cerebellar_layers():
    fig, ax = _new(5.0, 2.8)
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.add_patch(Rectangle((0.5, 4), 9, 1.6, fc='#e3eaf2', ec='white'))
    ax.add_patch(Rectangle((0.5, 3.1), 9, 0.9, fc='#ffe0b2', ec='white'))
    ax.add_patch(Rectangle((0.5, 0.6), 9, 2.5, fc='#c5cae9', ec='white'))
    ax.text(9.3, 4.8, '분자층 (별·바구니세포)', ha='right', fontsize=8.3)
    ax.text(9.3, 3.55, '조롱박세포층', ha='right', fontsize=8.3, weight='bold', color='#c0392b')
    ax.text(9.3, 1.7, '과립층 (과립세포 다수)', ha='right', fontsize=8.3)
    for x in [2, 4, 6]:
        ax.add_patch(Ellipse((x, 3.55), 0.5, 0.55, fc='#c0392b', ec='none'))
        ax.plot([x, x-0.3, x, x+0.3], [3.8, 4.8, 5.0, 4.7], color='#c0392b', lw=1)
    ax.text(1.0, 5.75, '조롱박세포=유일한 출력세포(억제성)', fontsize=7.8, color='#c0392b')
    ax.set_title('소뇌겉질 3층', fontsize=11, color=NAVY, weight='bold')
    return _save(fig, 'cerebellar_layers')


def respiratory_tree():
    fig, ax = _new(5.6, 2.8)
    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    stages = ['기관지', '세기관지', '종말\n세기관지', '호흡\n세기관지', '꽈리관·꽈리']
    xs = [1, 3.2, 5.4, 7.6, 10]
    for i, (x, s) in enumerate(zip(xs, stages)):
        col = '#c5cae9' if i < 3 else '#a5d6a7'
        ax.add_patch(Rectangle((x-0.9, 2.6), 1.8, 1.4, fc=col, ec='#666', lw=1))
        ax.text(x, 3.3, s, ha='center', va='center', fontsize=8)
        if i < 4:
            ax.annotate('', (xs[i+1]-0.95, 3.3), (x+0.95, 3.3),
                        arrowprops=dict(arrowstyle='->', color='#333'))
    ax.text(1, 4.5, '← 전도부 (가스교환 X)', fontsize=8, color='#3949ab')
    ax.text(11.8, 4.5, '호흡부 →', fontsize=8, color='#2e7d32', ha='right')
    ax.text(4.3, 1.7, '연골·샘 소실', ha='center', fontsize=7.6, color='#555')
    ax.text(5.4, 1.2, '술잔세포 소실(클라라세포)', ha='center', fontsize=7.6, color='#555')
    ax.text(8.8, 1.7, '벽에 꽈리 출현', ha='center', fontsize=7.6, color='#2e7d32')
    ax.set_title('호흡계 전도부 → 호흡부 이행', fontsize=11, color=NAVY, weight='bold')
    return _save(fig, 'respiratory_tree')


def atrial_septum():
    fig, ax = _new(5.0, 3.0)
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.add_patch(Ellipse((3, 3), 4, 4.4, fc='#e3f2fd', ec='#666'))
    ax.add_patch(Ellipse((7, 3), 4, 4.4, fc='#ffebee', ec='#666'))
    ax.add_patch(Rectangle((4.9, 1), 0.2, 4, fc='#90a4ae', ec='none'))  # 사이막
    ax.add_patch(Ellipse((5, 3), 0.7, 1.1, fc='#fff59d', ec='#b5680a', lw=1.3))  # 타원오목
    ax.text(2.6, 5.2, '오른심방', ha='center', fontsize=9, color='#c0392b')
    ax.text(7.4, 5.2, '왼심방', ha='center', fontsize=9, color='#1565c0')
    ax.annotate('타원오목 (fossa ovalis)\n= 태아 타원구멍 닫힌 흔적', (5, 3), (6.0, 0.4),
                fontsize=8, ha='left', color='#b5680a',
                arrowprops=dict(arrowstyle='->', color='#b5680a'))
    ax.text(0.2, 0.3, '미폐쇄=난원공개존(PFO) · 결손=심방사이막결손(ASD)', fontsize=7.6, color='#555')
    ax.set_title('심방사이막 — 타원오목', fontsize=11, color=NAVY, weight='bold')
    return _save(fig, 'atrial_septum')


def tca_cycle():
    import numpy as np
    fig, ax = _new(5.2, 4.2)
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.5, 1.5); ax.set_aspect('equal')
    nodes = ['시트르산\n(citrate)', '이소시트르산', 'α-케토글루타르산\n→ 글루탐산',
             '숙시닐-CoA', '숙신산', '푸마르산', '말산', '옥살아세트산\n→ 아스파르트산']
    n = len(nodes)
    ang = [np.pi/2 - 2*np.pi*i/n for i in range(n)]
    xs = [0.95*np.cos(a) for a in ang]; ys = [0.95*np.sin(a) for a in ang]
    for i in range(n):
        j = (i+1) % n
        ax.annotate('', (xs[j], ys[j]), (xs[i], ys[i]),
                    arrowprops=dict(arrowstyle='->', color='#0f3460', lw=1.1,
                                    connectionstyle='arc3,rad=0.12'))
    for i, (x, y, t) in enumerate(zip(xs, ys, nodes)):
        hi = ('글루탐산' in t) or ('아스파르트산' in t)
        ax.text(x, y, t, ha='center', va='center', fontsize=7.2,
                weight='bold' if hi else 'normal',
                color='#c0392b' if hi else '#222',
                bbox=dict(boxstyle='round,pad=0.2',
                          fc='#fff3cd' if hi else '#eef2f7', ec='#bbb'))
    ax.text(0, 0, 'TCA\n회로', ha='center', va='center', fontsize=10, weight='bold', color='#0f3460')
    ax.axis('off')
    ax.set_title('TCA 회로 — 아미노산·지방산 대사 연결', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'tca_cycle')


def electron_transport():
    fig, ax = _new(5.8, 2.9)
    ax.set_xlim(0, 14); ax.set_ylim(0, 6)
    comps = [('복합체 I\n(NADH-Q)', '#c5cae9'), ('복합체 II\n(FADH₂)', '#c5cae9'),
             ('CoQ', '#b2dfdb'), ('복합체 III', '#c5cae9'),
             ('cyt c', '#b2dfdb'), ('복합체 IV\n(cyt c 산화효소)', '#ffcdd2')]
    xs = [1.2, 3.0, 4.7, 6.4, 8.4, 10.4]
    ws = [1.4, 1.4, 1.0, 1.4, 1.0, 1.8]
    for (name, col), x, w in zip(comps, xs, ws):
        ax.add_patch(Rectangle((x-w/2, 2.4), w, 1.6, fc=col, ec='#666'))
        ax.text(x, 3.2, name, ha='center', va='center', fontsize=7.2)
    for i in range(len(xs)-1):
        ax.annotate('', (xs[i+1]-ws[i+1]/2, 3.2), (xs[i]+ws[i]/2, 3.2),
                    arrowprops=dict(arrowstyle='->', color='#333'))
    ax.annotate('O₂ → H₂O', (12.4, 3.2), (11.3, 3.2),
                arrowprops=dict(arrowstyle='->', color='#2e7d32'), fontsize=8, color='#2e7d32', va='center')
    ax.plot([10.4, 10.4], [4.2, 5.2], color='#c0392b', lw=2)
    ax.plot([10.0, 10.8], [5.0, 5.0], color='#c0392b', lw=2)
    ax.text(10.4, 5.5, '청산가리(CN⁻) 차단', ha='center', fontsize=8, color='#c0392b', weight='bold')
    ax.text(7, 1.4, '복합체 IV 차단 → 전자가 cyt c까지 전달되고 정체(상류 환원형 축적)',
            ha='center', fontsize=7.6, color='#555')
    ax.axis('off')
    ax.set_title('전자전달계(ETC)와 청산가리 작용점', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'electron_transport')


def urea_cycle():
    import numpy as np
    fig, ax = _new(5.2, 3.8)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.6); ax.set_aspect('equal')
    nodes = ['카바모일인산\n(CPS-I)', '시트룰린\n(OTC)', '아르지니노숙신산\n(ASS)',
             '아르지닌\n(ASL)', '오르니틴\n(아르지네이스)']
    n = len(nodes)
    ang = [np.pi/2 - 2*np.pi*i/n for i in range(n)]
    xs = [0.95*np.cos(a) for a in ang]; ys = [0.95*np.sin(a) for a in ang]
    for i in range(n):
        j = (i+1) % n
        ax.annotate('', (xs[j], ys[j]), (xs[i], ys[i]),
                    arrowprops=dict(arrowstyle='->', color='#0f3460', lw=1.1,
                                    connectionstyle='arc3,rad=0.12'))
    for x, y, t in zip(xs, ys, nodes):
        ax.text(x, y, t, ha='center', va='center', fontsize=7.2,
                bbox=dict(boxstyle='round,pad=0.2', fc='#eef2f7', ec='#bbb'))
    ax.text(0, 0, '요소회로\nNH₃→요소', ha='center', va='center', fontsize=8.5, weight='bold', color='#0f3460')
    ax.text(0, -1.42, 'CPT-I(지방산 산화)은 요소회로와 무관 → 암모니아↑ 원인 아님',
            ha='center', fontsize=7.4, color='#c0392b')
    ax.axis('off')
    ax.set_title('요소회로 효소 (암모니아 처리)', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'urea_cycle')


def o2_dissociation():
    import numpy as np
    fig, ax = _new(5.2, 3.2)
    x = np.linspace(0, 100, 200)
    def hb(p50):
        n = 2.8
        return 100 * x**n / (p50**n + x**n)
    ax.plot(x, hb(20), color='#1565c0', lw=2, ls='--', label='좌측이동 (친화도↑)')
    ax.plot(x, hb(26), color='#333', lw=2, label='정상 (P50≈26)')
    ax.plot(x, hb(38), color='#c0392b', lw=2, label='우측이동 (친화도↓)')
    ax.axhline(50, color='#aaa', ls=':', lw=0.8)
    ax.text(2, 50, 'P50', fontsize=7, color='#888', va='bottom')
    ax.annotate('우측이동 = 친화도↓ (조직에 O2 방출↑)\nH+↑(pH↓)·CO2↑·온도↑·2,3-BPG↑',
                (52, 60), (30, 20), fontsize=7.2, color='#c0392b',
                arrowprops=dict(arrowstyle='->', color='#c0392b'))
    ax.text(30, 92, '좌측이동 = 친화도↑\npH↑·CO2↓·온도↓·CO·태아Hb·미오글로빈',
            fontsize=7.2, color='#1565c0')
    ax.set_xlabel('산소분압 pO2 (mmHg)', fontsize=8.5)
    ax.set_ylabel('산소포화도 (%)', fontsize=8.5)
    ax.legend(fontsize=7.5, loc='lower right')
    ax.tick_params(labelsize=7.5)
    ax.set_title('산소-헤모글로빈 해리곡선 (보어 효과)', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'o2_dissociation')


def glucose_alanine():
    fig, ax = _new(5.4, 2.8)
    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    ax.add_patch(Rectangle((0.5, 1), 3.2, 4, fc='#e3f2fd', ec='#1565c0'))
    ax.add_patch(Rectangle((8.3, 1), 3.2, 4, fc='#ffebee', ec='#c0392b'))
    ax.text(2.1, 4.6, '근육', ha='center', fontsize=9.5, weight='bold', color='#1565c0')
    ax.text(9.9, 4.6, '간', ha='center', fontsize=9.5, weight='bold', color='#c0392b')
    ax.text(2.1, 3.4, '포도당→피루브산', ha='center', fontsize=7.6)
    ax.text(2.1, 2.6, '피루브산+아미노기\n→(ALT)→알라닌', ha='center', fontsize=7.4, color='#0f3460')
    ax.text(9.9, 3.4, '알라닌→피루브산', ha='center', fontsize=7.6)
    ax.text(9.9, 2.6, '→ 당신생 → 포도당', ha='center', fontsize=7.4, color='#0f3460')
    ax.annotate('알라닌 →', (8.2, 3.8), (3.8, 3.8), fontsize=8, color='#333', va='center',
                arrowprops=dict(arrowstyle='->', color='#333'))
    ax.annotate('← 포도당', (3.8, 2.0), (8.2, 2.0), fontsize=8, color='#2e7d32', va='center',
                arrowprops=dict(arrowstyle='->', color='#2e7d32'))
    ax.text(6, 0.4, '근육은 G6P가수분해효소가 없어 알라닌으로 간접 기여', ha='center', fontsize=7.6, color='#555')
    ax.axis('off')
    ax.set_title('포도당–알라닌 회로', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'glucose_alanine')


def fasting_fuel():
    import numpy as np
    fig, ax = _new(5.2, 3.0)
    t = np.linspace(0, 7, 100)
    ax.plot(t, 100*np.exp(-t/2.2)+40, color='#1565c0', lw=2, label='포도당(B)')
    ax.plot(t, 60*(1-np.exp(-t/0.8)), color='#e08a00', lw=2, label='지방산(C)')
    ax.plot(t, 90*(1-np.exp(-t/3.5)), color='#c0392b', lw=2, label='케톤체(A)')
    ax.set_xlabel('금식 기간 (일)', fontsize=8.5)
    ax.set_ylabel('상대 농도', fontsize=8.5)
    ax.legend(fontsize=8, loc='center right')
    ax.tick_params(labelsize=7.5)
    ax.text(0.2, 12, '초기: 글리코겐→포도당 · 지방분해로 지방산↑ · 수일 후 케톤체↑',
            fontsize=7.2, color='#555')
    ax.set_title('금식 시 혈중 연료 변화', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'fasting_fuel')


def flow_volume_loop():
    import numpy as np
    fig, ax = _new(5.0, 3.2)
    v = np.linspace(0, 5, 100)
    # 정상(A)
    fn = np.where(v < 0.8, v/0.8*10, 10*(1-(v-0.8)/4.2))
    ax.plot(5 - v, fn, color='#1565c0', lw=2, label='A: 정상')
    # 폐쇄(B) — 오목한 하강(scooping), 낮은 유량
    fb = np.where(v < 0.8, v/0.8*6, 6*(1-((v-0.8)/4.2))**1.8)
    ax.plot(5 - v, fb, color='#c0392b', lw=2, label='B: 폐쇄(COPD)')
    ax.annotate('오목한 하강\n(scooping)', (2.6, 1.6), (0.4, 4.0), fontsize=8, color='#c0392b',
                arrowprops=dict(arrowstyle='->', color='#c0392b'))
    ax.set_xlabel('폐용량 (큰 폐용량 →)', fontsize=8.5)
    ax.set_ylabel('유량 (flow)', fontsize=8.5)
    ax.legend(fontsize=8, loc='upper right')
    ax.tick_params(labelsize=7.5)
    ax.set_title('유량-용량곡선: 정상 vs 폐쇄폐질환', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'flow_volume_loop')


def cerebral_autoregulation():
    import numpy as np
    fig, ax = _new(5.0, 3.0)
    p = np.linspace(20, 200, 200)
    flow = np.clip((p - 20) * 3, 0, None)
    flow = np.where(p < 60, (p-20)/40*50, np.where(p > 150, 50 + (p-150)/50*40, 50))
    ax.plot(p, flow, color='#0f3460', lw=2.2)
    ax.axvspan(60, 150, color='#c5e1a5', alpha=.35)
    ax.text(105, 70, '자동조절 구간\n(혈류 일정)', ha='center', fontsize=8, color='#2e7d32')
    ax.annotate('B: 혈압↑ →\n뇌혈관 저항 증가로\n혈류 일정 유지', (110, 50), (120, 15),
                fontsize=7.8, color='#c0392b', ha='left',
                arrowprops=dict(arrowstyle='->', color='#c0392b'))
    ax.text(35, 12, 'A: 조절 하한\n이하', fontsize=7.6, color='#555')
    ax.set_xlabel('평균 동맥압 (mmHg)', fontsize=8.5)
    ax.set_ylabel('뇌혈류량', fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    ax.set_title('뇌혈류 자동조절 (myogenic)', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'cerebral_autoregulation')


def antagonist_curves():
    import numpy as np
    fig, ax = _new(5.2, 3.0)
    x = np.linspace(-2, 3, 200)
    def curve(shift=0, emax=100):
        return emax / (1 + 10**(-(x - shift)))
    ax.plot(x, curve(0), color='#1565c0', lw=2, label='A: 작용제 단독')
    ax.plot(x, curve(1.0), color='#e08a00', lw=2, label='B: 경쟁적 길항제(우측이동)')
    ax.plot(x, curve(0, 60), color='#c0392b', lw=2, label='C: 비경쟁적 길항제(최대↓)')
    ax.axhline(50, color='#aaa', ls=':', lw=0.8)
    ax.set_xlabel('로그 용량', fontsize=8.5)
    ax.set_ylabel('반응 (%)', fontsize=8.5)
    ax.legend(fontsize=7.6, loc='upper left')
    ax.tick_params(labelsize=7.5)
    ax.text(0.2, 8, 'ED50: A=C < B (경쟁적=우측이동, 비경쟁적=ED50 불변·Emax↓)',
            fontsize=7.3, color='#555')
    ax.set_title('작용제 용량-반응: 경쟁적 vs 비경쟁적 길항제', fontsize=10, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'antagonist_curves')


def therapeutic_index():
    import numpy as np
    fig, ax = _new(5.2, 3.0)
    x = np.linspace(-1, 4, 200)
    eff = 100 / (1 + 10**(-(x - 0.5)))
    tox = 100 / (1 + 10**(-(x - 2.5)))
    ax.plot(x, eff, color='#1565c0', lw=2, label='효능(치료효과)')
    ax.plot(x, tox, color='#c0392b', lw=2, label='독성')
    ax.axhline(50, color='#aaa', ls=':', lw=0.8)
    ax.annotate('ED50', (0.5, 50), (0.5, 20), fontsize=8, color='#1565c0', ha='center',
                arrowprops=dict(arrowstyle='->', color='#1565c0'))
    ax.annotate('TD50', (2.5, 50), (2.5, 20), fontsize=8, color='#c0392b', ha='center',
                arrowprops=dict(arrowstyle='->', color='#c0392b'))
    ax.set_xlabel('로그 용량', fontsize=8.5)
    ax.set_ylabel('반응 개체 비율 (%)', fontsize=8.5)
    ax.legend(fontsize=8, loc='center right')
    ax.tick_params(labelsize=7.5)
    ax.text(-0.9, 90, '치료지수(TI) = TD50 / ED50 (클수록 안전)', fontsize=7.8, color='#555')
    ax.set_title('치료지수(therapeutic index)', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'therapeutic_index')


def glycolysis():
    """해당작용 수직 흐름 모식도 — 3개 조절효소 강조 + 젖산/아세틸CoA 분기."""
    fig, ax = _new(5.4, 6.2)
    ax.set_xlim(0, 10); ax.set_ylim(0, 15)
    main = [
        (13.6, '포도당', False),
        (11.9, '포도당-6-인산 (G6P)', False),
        (10.2, '과당-6-인산 (F6P)', False),
        (8.5, '과당-1,6-2인산 (F1,6BP)', False),
        (6.8, '글리세르알데하이드-3-인산 ×2', False),
        (5.1, '포스포엔올피루브산 (PEP) ×2', False),
        (3.4, '피루브산 ×2', False),
    ]
    for y, t, _ in main:
        ax.text(4.0, y, t, ha='center', va='center', fontsize=8,
                bbox=dict(boxstyle='round,pad=0.3', fc='#eef2f7', ec='#8aa0b8'))
    # 세로 화살표
    for i in range(len(main) - 1):
        ax.annotate('', (4.0, main[i+1][0] + 0.5), (4.0, main[i][0] - 0.5),
                    arrowprops=dict(arrowstyle='-|>', color='#0f3460', lw=1.3))
    # 효소·조효소 주석 (오른쪽)
    def enz(y, text, hot):
        ax.text(6.5, y, text, ha='left', va='center', fontsize=7.4,
                color='#c0392b' if hot else '#555', weight='bold' if hot else 'normal')
    enz(12.75, '헥소키나스 ★  (ATP 1 소모)', True)
    enz(9.35, 'PFK-1 ★ 속도조절  (ATP 1 소모)', True)
    enz(5.95, 'NAD+ 환원(NADH ×2) · ATP ×2 생성', False)
    enz(4.25, '피루브산키나스 ★  (ATP ×2 생성)', True)
    # 순생성 요약
    ax.text(0.3, 14.4, '순생성(세포질): ATP 2 · NADH 2', ha='left', va='center',
            fontsize=8.2, color='#0f3460', weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#fff3cd', ec='#d0a840'))
    # 분기: 무산소(젖산) / 유산소(아세틸CoA)
    ax.annotate('', (1.7, 1.9), (3.4, 2.9),
                arrowprops=dict(arrowstyle='-|>', color='#7a7a7a', lw=1.2))
    ax.annotate('', (6.4, 1.9), (4.6, 2.9),
                arrowprops=dict(arrowstyle='-|>', color='#2e7d32', lw=1.2))
    ax.text(1.5, 1.4, '젖산\n(무산소·LDH)\nNAD+ 재생', ha='center', va='center', fontsize=7.2,
            color='#7a5100', bbox=dict(boxstyle='round,pad=0.3', fc='#fdf0d5', ec='#c9a24a'))
    ax.text(6.6, 1.4, '아세틸CoA · TCA 진입\n(유산소·미토콘드리아)', ha='center', va='center', fontsize=7.2,
            color='#1b5e20', bbox=dict(boxstyle='round,pad=0.3', fc='#dcedc8', ec='#7cb342'))
    ax.axis('off')
    ax.set_title('해당작용 — 3개 조절효소(★)와 피루브산 분기', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'glycolysis')


def visual_field_defects():
    """시각경로 병변 위치별 시야결손(반맹) — 좌·우 눈 시야 도식."""
    import numpy as np
    from matplotlib.patches import Wedge, Circle
    fig, ax = _new(5.8, 5.2)
    ax.set_xlim(0, 12); ax.set_ylim(0, 12); ax.axis('off')

    def eye(cx, cy, r, spec):
        ax.add_patch(Circle((cx, cy), r, fc='white', ec='#333', lw=1.1))
        g = '#333'
        if spec == 'full':
            ax.add_patch(Circle((cx, cy), r, fc=g, ec='#333', lw=1.1))
        elif spec == 'left':
            ax.add_patch(Wedge((cx, cy), r, 90, 270, fc=g))
        elif spec == 'right':
            ax.add_patch(Wedge((cx, cy), r, -90, 90, fc=g))
        elif spec == 'UL':   # 위-왼쪽 사분면
            ax.add_patch(Wedge((cx, cy), r, 90, 180, fc=g))
        elif spec == 'left_ms':  # 좌반맹 + 황반보존
            ax.add_patch(Wedge((cx, cy), r, 90, 270, fc=g))
            ax.add_patch(Circle((cx, cy), r*0.32, fc='white', ec='none'))
        # 십자 안내선
        ax.plot([cx-r, cx+r], [cy, cy], color='#bbb', lw=0.5)
        ax.plot([cx, cx], [cy-r, cy+r], color='#bbb', lw=0.5)

    rows = [
        ('① 오른 시신경',        'full', 'norm', '오른눈 완전 실명'),
        ('② 시각교차(정중)',     'left', 'right', '양측 이측반맹(양비측)'),
        ('③ 오른 시각로',        'left', 'left', '왼쪽 동측반맹'),
        ('④ 오른 관자엽(마이어)', 'UL', 'UL', '왼쪽 위 사분맹'),
        ('⑤ 오른 뒤통수엽',      'left_ms', 'left_ms', '왼쪽 동측반맹(황반보존)'),
    ]
    y = 10.6
    ax.text(1.9, 11.4, '병변 위치', fontsize=8, ha='center', weight='bold', color='#0f3460')
    ax.text(5.2, 11.4, '왼눈', fontsize=8, ha='center', weight='bold', color='#0f3460')
    ax.text(6.9, 11.4, '오른눈', fontsize=8, ha='center', weight='bold', color='#0f3460')
    ax.text(9.6, 11.4, '결손', fontsize=8, ha='center', weight='bold', color='#0f3460')
    for label, lspec, rspec, desc in rows:
        ax.text(0.2, y, label, fontsize=7.6, va='center', ha='left', color='#222')
        eye(5.2, y, 0.62, lspec)
        eye(6.9, y, 0.62, 'norm' if rspec == 'norm' else rspec)
        if rspec == 'norm':
            ax.add_patch(Circle((6.9, y), 0.62, fc='white', ec='#333', lw=1.1))
            ax.plot([6.9-0.62, 6.9+0.62], [y, y], color='#bbb', lw=0.5)
            ax.plot([6.9, 6.9], [y-0.62, y+0.62], color='#bbb', lw=0.5)
        ax.text(9.6, y, desc, fontsize=7.0, va='center', ha='center', color='#c0392b')
        y -= 2.05
    ax.text(6, 0.2, '검은 부분 = 안 보이는 시야  ·  교차 전=같은눈 / 교차=양비측 / 교차 후=반대쪽 동측',
            fontsize=6.9, ha='center', color='#555')
    ax.set_title('시각경로 병변과 시야결손(반맹)', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'visual_field_defects')


def energy_overview():
    """포도당 완전산화 전체 흐름 — 해당→피루브산산화→TCA→전자전달계, ATP 총계."""
    fig, ax = _new(6.0, 3.6)
    ax.set_xlim(0, 13); ax.set_ylim(0, 10); ax.axis('off')

    def box(x, y, w, h, t, fc, tc='#20303d', fs=7.2):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec='#888', lw=1.0))
        ax.text(x + w/2, y + h/2, t, fontsize=fs, ha='center', va='center', color=tc)

    steps = [
        (0.3, '포도당\n(세포질)', '#eef2f7'),
        (3.0, '피루브산 ×2\n해당', '#dbe7f2'),
        (6.0, '아세틸CoA ×2\n(미토콘드리아)', '#dbe7d5'),
        (9.0, 'TCA 회로 ×2', '#fdecc8'),
    ]
    for x, t, c in steps:
        box(x, 6.5, 2.4, 1.8, t, c)
    for x in [2.7, 5.7, 8.7]:
        ax.annotate('', (x + 0.3, 7.4), (x, 7.4), arrowprops=dict(arrowstyle='->', color='#333'))
    # 산출물(각 단계 아래)
    ax.text(1.5, 5.9, 'ATP 2 · NADH 2', fontsize=6.8, ha='center', color='#1565c0')
    ax.text(7.2, 5.9, 'NADH 2 · CO2 2\n(피루브산 탈수소효소)', fontsize=6.6, ha='center', color='#2e7d32')
    ax.text(10.2, 5.9, 'NADH 6 · FADH2 2\nGTP 2 · CO2 4', fontsize=6.6, ha='center', color='#b5680a')
    # 전자전달계 수집 박스
    box(2.6, 2.6, 7.8, 1.6, '전자전달계 · 산화적 인산화 (미토콘드리아 속막)\nNADH ≈ 2.5 ATP · FADH2 ≈ 1.5 ATP · 최종 전자수용체 = 산소',
        '#c5cae9', fs=7.0)
    for x in [2.0, 8.2, 10.2]:
        ax.annotate('', (x, 4.2), (x, 5.6), arrowprops=dict(arrowstyle='->', color='#5c6bc0', lw=1.2))
    ax.text(11.6, 3.4, 'H2O', fontsize=7.5, color='#2e7d32', weight='bold')
    ax.annotate('', (11.4, 3.4), (10.4, 3.4), arrowprops=dict(arrowstyle='->', color='#2e7d32'))
    # 총계
    ax.add_patch(Rectangle((3.2, 0.4), 6.6, 1.2, fc='#fff3cd', ec='#d0a840', lw=1.2))
    ax.text(6.5, 1.0, '포도당 1개 완전산화 ≈ 30~32 ATP  (무산소면 해당의 2 ATP뿐)',
            fontsize=7.8, ha='center', color='#0f3460', weight='bold')
    ax.set_title('에너지 대사 전체 흐름 — 해당 · TCA · 전자전달계',
                 fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'energy_overview')


def tca_energy():
    """TCA 회로 한 바퀴 에너지·CO2 산출 모식도."""
    import numpy as np
    fig, ax = _new(5.4, 4.6)
    ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7); ax.set_aspect('equal')
    nodes = ['시트르산', '이소시트르산', 'α-케토\n글루타르산', '숙시닐-CoA',
             '숙신산', '푸마르산', '말산', '옥살아세트산']
    # 각 전이 화살표(i→i+1)에 붙는 산출물
    edge_out = ['', 'NADH · CO2', 'NADH · CO2', 'GTP', 'FADH2', '', 'NADH', '(아세틸CoA 합류)']
    n = len(nodes)
    ang = [np.pi/2 - 2*np.pi*i/n for i in range(n)]
    xs = [1.05*np.cos(a) for a in ang]; ys = [1.05*np.sin(a) for a in ang]
    for i in range(n):
        j = (i+1) % n
        ax.annotate('', (xs[j], ys[j]), (xs[i], ys[i]),
                    arrowprops=dict(arrowstyle='->', color='#0f3460', lw=1.1,
                                    connectionstyle='arc3,rad=0.12'))
        out = edge_out[i]
        if out:
            mx, my = (xs[i]+xs[j])/2, (ys[i]+ys[j])/2
            r = (mx**2 + my**2) ** 0.5
            hot = ('GTP' in out) or ('FADH' in out) or ('NADH' in out)
            ax.text(mx*1.55, my*1.55, out, ha='center', va='center', fontsize=6.8,
                    color='#c0392b' if hot else '#555', weight='bold' if hot else 'normal')
    for x, y, t in zip(xs, ys, nodes):
        ax.text(x, y, t, ha='center', va='center', fontsize=7.0,
                bbox=dict(boxstyle='round,pad=0.2', fc='#eef2f7', ec='#bbb'))
    ax.text(0, 0, '한 바퀴\nNADH 3\nFADH2 1\nGTP 1 · CO2 2', ha='center', va='center',
            fontsize=8, weight='bold', color='#0f3460')
    ax.axis('off')
    ax.set_title('TCA 회로 — 한 바퀴 에너지·CO2 산출', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'tca_energy')


def pv_loop():
    """좌심실 압력-용적곡선(PV loop) — 4상 + S1/S2 판막 사건."""
    fig, ax = _new(5.2, 3.8)
    # 꼭짓점 (용적 mL, 압력 mmHg)
    A = (120, 8)    # 승모판 닫힘(S1) = 이완기말
    B = (120, 80)   # 대동맥판 열림
    C = (50, 100)   # 대동맥판 닫힘(S2) = 수축기말
    D = (50, 8)     # 승모판 열림
    import numpy as np
    # 박출기 곡선(B→C): 살짝 위로 볼록
    bx = np.linspace(120, 50, 40); by = 80 + 20*np.sin(np.linspace(0, np.pi, 40))*0.9
    # 충만기 곡선(D→A): 완만한 상승
    dx = np.linspace(50, 120, 40); dy = 8 + 0.0009*(dx-50)**2
    ax.plot([A[0], B[0]], [A[1], B[1]], color='#0f3460', lw=2)      # 등용성 수축
    ax.plot(bx, by, color='#0f3460', lw=2)                          # 박출
    ax.plot([C[0], D[0]], [C[1], D[1]], color='#0f3460', lw=2)      # 등용성 이완
    ax.plot(dx, dy, color='#0f3460', lw=2)                          # 충만
    for (x, y), t, dxy in [(A, 'S1 승모판닫힘', (6, -10)), (B, '대동맥판 열림', (4, 4)),
                           (C, 'S2 대동맥판닫힘', (-2, 8)), (D, '승모판 열림', (-30, -6))]:
        ax.plot(x, y, 'o', color='#c0392b', ms=5)
        ax.annotate(t, (x, y), (x+dxy[0], y+dxy[1]), fontsize=7.3, color='#c0392b')
    ax.text(85, 45, '박출량(SV)', fontsize=8, color='#1565c0', ha='center')
    ax.annotate('', (50, 32), (120, 32), arrowprops=dict(arrowstyle='<->', color='#1565c0'))
    ax.text(85, 26, 'SV = EDV - ESV', fontsize=7, color='#1565c0', ha='center')
    ax.set_xlabel('좌심실 용적 (mL)', fontsize=8.5)
    ax.set_ylabel('좌심실 압력 (mmHg)', fontsize=8.5)
    ax.set_xlim(30, 150); ax.set_ylim(0, 120); ax.tick_params(labelsize=7.5)
    ax.set_title('좌심실 압력-용적곡선(PV loop)', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'pv_loop')


def cardiac_ap():
    """심실근 활동전위 5상 — 고원기(L형 Ca) 강조."""
    import numpy as np
    fig, ax = _new(5.2, 3.4)
    t0 = np.linspace(-0.5, 0, 20); v0 = np.full_like(t0, -90)          # 4상 안정막
    t1 = np.array([0, 0.02]); v1 = np.array([-90, 20])                 # 0상 상승(Na)
    t2 = np.array([0.02, 0.05]); v2 = np.array([20, 5])                # 1상 초기재분극
    t3 = np.linspace(0.05, 0.25, 30); v3 = np.full_like(t3, 5)         # 2상 고원기(Ca)
    t4 = np.linspace(0.25, 0.35, 20); v4 = np.linspace(5, -90, 20)     # 3상 재분극(K)
    t5 = np.linspace(0.35, 0.7, 20); v5 = np.full_like(t5, -90)        # 4상
    for t, v in [(t0, v0), (t1, v1), (t2, v2), (t3, v3), (t4, v4), (t5, v5)]:
        ax.plot(t, v, color='#0f3460', lw=2)
    ax.axhline(0, color='#ccc', ls=':', lw=0.7)
    ax.annotate('0상 (Na+ 유입)', (0.012, 15), (-0.45, 25), fontsize=7.4, color='#c0392b',
                weight='bold', arrowprops=dict(arrowstyle='->', color='#c0392b'))
    ax.annotate('1상', (0.035, 10), (0.04, 30), fontsize=7.4, color='#555', weight='bold',
                arrowprops=dict(arrowstyle='->', color='#555'))
    ax.text(0.15, 22, '2상 고원기\n(L형 Ca2+ 유입 vs K+ 유출)', fontsize=7.4, color='#1565c0',
            ha='center', weight='bold')
    ax.annotate('3상 (K+ 유출)', (0.30, -40), (0.33, -20), fontsize=7.4, color='#2e7d32',
                weight='bold', arrowprops=dict(arrowstyle='->', color='#2e7d32'))
    ax.text(0.55, -78, '4상 안정막 -90mV', fontsize=7.4, color='#555', ha='center', weight='bold')
    ax.set_xlabel('시간', fontsize=8.5); ax.set_ylabel('막전위 (mV)', fontsize=8.5)
    ax.set_ylim(-100, 40); ax.set_xticks([]); ax.tick_params(labelsize=7.5)
    ax.set_title('심실근 활동전위 — 고원기와 이온흐름', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'cardiac_ap')


def cardiac_venous_return():
    """심장기능곡선 × 정맥환류곡선 교차 = 작동점."""
    import numpy as np
    fig, ax = _new(5.2, 3.4)
    rap = np.linspace(-2, 8, 100)
    co = 5 * (1 - np.exp(-(rap + 2) / 2.2))           # 심장기능곡선(전부하↑→박출↑)
    vr = np.clip((7 - rap) * 0.75, 0, None)           # 정맥환류곡선(MSFP=7에서 0)
    ax.plot(rap, co, color='#c0392b', lw=2, label='심장기능곡선(Starling)')
    ax.plot(rap, vr, color='#1565c0', lw=2, label='정맥환류곡선')
    # 교차점 근사
    idx = int(np.argmin(np.abs(co - vr)))
    ax.plot(rap[idx], co[idx], 'ko', ms=6)
    ax.annotate('작동점\n(심박출량=정맥환류)', (rap[idx], co[idx]),
                (rap[idx]-3.2, co[idx]+0.6), fontsize=7.4, color='#333',
                arrowprops=dict(arrowstyle='->', color='#333'))
    ax.axvline(7, color='#1565c0', ls=':', lw=0.8)
    ax.text(7, 0.2, 'MSFP\n(평균체순환\n충만압)', fontsize=6.8, color='#1565c0', ha='center')
    ax.set_xlabel('우심방압 RAP (mmHg)', fontsize=8.5)
    ax.set_ylabel('혈류량 (L/분)', fontsize=8.5)
    ax.legend(fontsize=7.6, loc='upper right'); ax.tick_params(labelsize=7.5)
    ax.set_title('심장기능곡선 × 정맥환류곡선', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'cardiac_venous_return')


def menstrual_cycle():
    """월경주기 호르몬 곡선 — 여포기/황체기, 배란."""
    import numpy as np
    fig, ax = _new(5.4, 3.4)
    d = np.linspace(0, 28, 200)
    def bump(c, w, h): return h * np.exp(-((d - c) / w) ** 2)
    lh = bump(14, 0.7, 1.0) + 0.08
    fsh = bump(13.3, 1.0, 0.45) + bump(1, 3, 0.18) + 0.08
    est = bump(12.5, 2.2, 0.85) + bump(21, 3.5, 0.5) + 0.06
    prog = bump(21, 3.6, 1.0) + 0.03
    ax.plot(d, lh, color='#c0392b', lw=1.8, label='LH')
    ax.plot(d, fsh, color='#8e44ad', lw=1.5, label='FSH')
    ax.plot(d, est, color='#1565c0', lw=1.8, label='에스트로겐')
    ax.plot(d, prog, color='#2e7d32', lw=1.8, label='프로게스테론')
    ax.axvline(14, color='#888', ls='--', lw=1)
    ax.text(14, 1.15, '배란', fontsize=8, color='#333', ha='center', weight='bold')
    ax.text(7, -0.16, '여포기(증식기)', fontsize=7.6, color='#555', ha='center')
    ax.text(21, -0.16, '황체기(분비기)', fontsize=7.6, color='#555', ha='center')
    ax.set_xlabel('주기 일수 (day)', fontsize=8.5); ax.set_ylabel('상대 농도', fontsize=8.5)
    ax.set_ylim(-0.25, 1.3); ax.set_yticks([]); ax.tick_params(labelsize=7.5)
    ax.legend(fontsize=7.4, loc='upper left', ncol=2)
    ax.set_title('월경주기 호르몬 변화', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'menstrual_cycle')


def glucose_titration():
    """신장 포도당 처리 — 여과·재흡수·배설과 역치·Tm."""
    import numpy as np
    fig, ax = _new(5.2, 3.4)
    pg = np.linspace(0, 600, 300)
    filt = pg * 1.25                                   # 여과량(GFR 125)
    tm = 375.0                                         # 재흡수 최대
    # splay: Tm 부근을 부드럽게 포화시키는 재흡수 곡선
    reab = tm * np.tanh(filt / tm)
    exc = np.clip(filt - reab, 0, None)
    ax.plot(pg, filt, color='#333', lw=1.8, label='여과량(filtered)')
    ax.plot(pg, reab, color='#1565c0', lw=1.8, label='재흡수(reabsorbed)')
    ax.plot(pg, exc, color='#c0392b', lw=1.8, label='배설(excreted)')
    ax.axhline(tm, color='#1565c0', ls=':', lw=0.8)
    ax.text(20, tm + 15, 'Tm(재흡수 최대)', fontsize=7, color='#1565c0')
    ax.axvline(180, color='#c0392b', ls=':', lw=0.8)
    ax.text(188, 40, '역치≈180\n(포도당뇨 시작)', fontsize=7, color='#c0392b')
    ax.set_xlabel('혈장 포도당 (mg/dL)', fontsize=8.5)
    ax.set_ylabel('포도당량 (mg/분)', fontsize=8.5)
    ax.legend(fontsize=7.4, loc='upper left'); ax.tick_params(labelsize=7.5)
    ax.set_title('신장 포도당 처리 — 역치·Tm·삼출(splay)', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'glucose_titration')


def knudson_2hit():
    """종양유전자(1-hit gain) vs 종양억제유전자(2-hit loss) 모식도."""
    fig, ax = _new(5.6, 3.6)
    ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis('off')

    def allele(x, y, on, label=None):
        # on=True: 활성/정상(파랑), False: 불활성/돌연변이(빨강 X)
        col = '#c0392b' if not on else '#2e7d32'
        ax.add_patch(Rectangle((x, y), 1.4, 0.7, fc='#eef2f7', ec=col, lw=1.6))
        if not on:
            ax.plot([x+0.2, x+1.2], [y+0.15, y+0.55], color=col, lw=1.6)
            ax.plot([x+0.2, x+1.2], [y+0.55, y+0.15], color=col, lw=1.6)

    # 종양유전자(위)
    ax.text(0.2, 9.3, '종양유전자(oncogene) — 우성, 1-hit "기능획득"', fontsize=8.5,
            color='#c0392b', weight='bold')
    allele(0.7, 8.0, True); allele(2.3, 8.0, True)
    ax.annotate('', (5.0, 8.35), (4.0, 8.35), arrowprops=dict(arrowstyle='->', color='#333'))
    ax.text(4.5, 8.75, '한쪽 활성화\n돌연변이', fontsize=6.8, ha='center', color='#333')
    ax.add_patch(Rectangle((5.2, 8.0), 1.4, 0.7, fc='#fdecea', ec='#c0392b', lw=1.6))
    ax.text(5.9, 8.35, '과활성', fontsize=6.8, ha='center', color='#c0392b')
    allele(6.9, 8.0, True)
    ax.annotate('', (10.0, 8.35), (8.6, 8.35), arrowprops=dict(arrowstyle='->', color='#c0392b'))
    ax.text(10.6, 8.35, '암', fontsize=10, color='#c0392b', weight='bold', va='center')

    # 종양억제유전자(아래)
    ax.text(0.2, 5.6, '종양억제유전자 — 열성, 2-hit "기능상실"(Knudson)', fontsize=8.5,
            color='#1565c0', weight='bold')
    allele(0.7, 4.2, True); allele(2.3, 4.2, True)
    ax.annotate('', (5.0, 4.55), (4.0, 4.55), arrowprops=dict(arrowstyle='->', color='#333'))
    ax.text(4.5, 4.95, '1st hit\n(한쪽 소실)', fontsize=6.8, ha='center', color='#333')
    allele(5.2, 4.2, True); allele(6.9, 4.2, False)
    ax.annotate('', (10.0, 4.55), (8.5, 4.55), arrowprops=dict(arrowstyle='->', color='#333'))
    ax.text(9.25, 4.95, '2nd hit\n(나머지 소실)', fontsize=6.8, ha='center', color='#333')
    ax.text(10.6, 4.55, '', fontsize=8)
    allele(10.0, 4.2, False)
    ax.annotate('', (10.7, 3.9), (10.7, 3.2), arrowprops=dict(arrowstyle='->', color='#c0392b'))
    ax.text(10.7, 2.9, '억제 소실 → 암', fontsize=7.6, color='#c0392b', ha='center', weight='bold')
    ax.text(6, 1.4, '유전성 암은 1st hit를 이미 물려받아(생식세포 돌연변이) 조기·다발 발생',
            fontsize=7.4, ha='center', color='#555')
    ax.set_title('발암 유전자 — 종양유전자(1-hit) vs 종양억제유전자(2-hit)',
                 fontsize=10, color=NAVY, weight='bold')
    return _save(fig, 'knudson_2hit')


def gn_immunofluorescence():
    """사구체신염 면역형광 3패턴 — 선형/과립상/무침착."""
    import numpy as np
    fig, ax = _new(5.8, 2.8)
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis('off')
    panels = [
        (2.0, '선형(linear)', '항GBM병\n(굿패스처)', 'line'),
        (6.0, '과립상(granular)', '면역복합체\n(연쇄구균후·루푸스·막신병증)', 'granular'),
        (10.0, '무침착/미약', 'ANCA 혈관염·\n미세변화(발돌기소실)', 'none'),
    ]
    for cx, title, sub, kind in panels:
        # GBM 곡선(고리 모양)
        t = np.linspace(0.2*np.pi, 1.8*np.pi, 100)
        gx = cx + 1.3*np.cos(t); gy = 3.4 + 1.0*np.sin(t)
        if kind == 'line':
            ax.plot(gx, gy, color='#2e7d32', lw=3)
        else:
            ax.plot(gx, gy, color='#9aa', lw=1.2)
        if kind == 'granular':
            for tt in np.linspace(0.25*np.pi, 1.75*np.pi, 12):
                ax.plot(cx + 1.3*np.cos(tt), 3.4 + 1.0*np.sin(tt), 'o',
                        color='#2e7d32', ms=4)
        ax.text(cx, 1.5, title, fontsize=8.2, ha='center', weight='bold', color='#0f3460')
        ax.text(cx, 0.7, sub, fontsize=6.9, ha='center', color='#555')
    ax.set_title('사구체신염 면역형광 패턴', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'gn_immunofluorescence')


def gram_wall():
    """세균 세포벽 3형 — 그람양성 / 그람음성 / 항산균."""
    fig, ax = _new(5.8, 3.4)
    ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis('off')

    def layer(x, y, w, h, col, ec='#888'):
        ax.add_patch(Rectangle((x, y), w, h, fc=col, ec=ec, lw=0.8))

    W = 3.0
    # 그람양성 (x=0.4): 두꺼운 펩티도글리칸
    cx = 0.6
    ax.text(cx + W/2, 9.3, '그람양성', fontsize=9, ha='center', weight='bold', color='#6a1b9a')
    layer(cx, 2.0, W, 0.7, '#d1c4e9')                       # 세포막
    layer(cx, 2.7, W, 3.0, '#9575cd')                       # 두꺼운 펩티도글리칸
    ax.text(cx + W/2, 4.2, '두꺼운\n펩티도글리칸\n(+테이코산)', fontsize=6.8, ha='center',
            va='center', color='white')
    ax.text(cx + W/2, 2.35, '세포막', fontsize=6.5, ha='center', va='center')
    ax.text(cx + W/2, 1.2, '보라색 유지\n(크리스탈바이올렛)', fontsize=6.6, ha='center', color='#6a1b9a')

    # 그람음성 (중앙): 얇은 펩티도글리칸 + 외막(LPS)
    cx = 4.5
    ax.text(cx + W/2, 9.3, '그람음성', fontsize=9, ha='center', weight='bold', color='#c0392b')
    layer(cx, 2.0, W, 0.7, '#ffcdd2')                       # 세포막
    layer(cx, 2.7, W, 0.8, '#e57373')                       # 얇은 펩티도글리칸
    layer(cx, 3.5, W, 0.9, '#ef9a9a')                       # 주변공간
    layer(cx, 4.4, W, 0.9, '#c62828')                       # 외막 (LPS)
    ax.text(cx + W/2, 4.85, '외막(LPS=내독소)', fontsize=6.6, ha='center', va='center', color='white')
    ax.text(cx + W/2, 3.1, '얇은 펩티도글리칸', fontsize=6.4, ha='center', va='center')
    ax.text(cx + W/2, 2.35, '세포막', fontsize=6.5, ha='center', va='center')
    ax.text(cx + W/2, 1.2, '분홍색\n(사프라닌 대조염색)', fontsize=6.6, ha='center', color='#c0392b')

    # 항산균 (오른쪽): 미콜산
    cx = 8.4
    ax.text(cx + W/2, 9.3, '항산균(결핵·한센)', fontsize=9, ha='center', weight='bold', color='#1565c0')
    layer(cx, 2.0, W, 0.7, '#bbdefb')                       # 세포막
    layer(cx, 2.7, W, 1.2, '#64b5f6')                       # 펩티도글리칸+아라비노갈락탄
    layer(cx, 3.9, W, 1.4, '#1565c0')                       # 미콜산(밀랍)
    ax.text(cx + W/2, 4.6, '미콜산\n(밀랍층)', fontsize=6.8, ha='center', va='center', color='white')
    ax.text(cx + W/2, 3.3, '펩티도글리칸', fontsize=6.4, ha='center', va='center', color='white')
    ax.text(cx + W/2, 2.35, '세포막', fontsize=6.5, ha='center', va='center')
    ax.text(cx + W/2, 1.2, '항산성 염색\n(잘 안 벗겨짐)', fontsize=6.6, ha='center', color='#1565c0')

    ax.set_title('세균 세포벽 3형 — 그람 염색성의 근거', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'gram_wall')


def antigen_presentation():
    """항원제시 경로 — MHC I(내인성·CD8) vs MHC II(외인성·CD4)."""
    fig, ax = _new(5.8, 4.2)
    ax.set_xlim(0, 12); ax.set_ylim(0, 12); ax.axis('off')

    def box(x, y, w, h, t, fc, tc='#20303d', fs=7.0):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec='#888', lw=1.0))
        ax.text(x + w/2, y + h/2, t, fontsize=fs, ha='center', va='center', color=tc)

    # MHC I (왼쪽)
    ax.text(3.0, 11.2, 'MHC I 경로', fontsize=9.5, ha='center', weight='bold', color='#1565c0')
    ax.text(3.0, 10.5, '모든 유핵세포', fontsize=7, ha='center', color='#555')
    steps1 = ['내인성 항원\n(바이러스·세포질 단백)', '프로테아좀에서 분해',
              'TAP로 소포체 이동', 'MHC I에 적재', 'CD8+ 세포독성 T세포']
    ys = [9.2, 7.7, 6.2, 4.7, 3.0]
    for t, y in zip(steps1, ys):
        box(0.7, y, 4.6, 1.0, t, '#e3f2fd')
    for i in range(len(ys)-1):
        ax.annotate('', (3.0, ys[i+1]+1.0), (3.0, ys[i]),
                    arrowprops=dict(arrowstyle='->', color='#1565c0'))

    # MHC II (오른쪽)
    ax.text(9.0, 11.2, 'MHC II 경로', fontsize=9.5, ha='center', weight='bold', color='#c0392b')
    ax.text(9.0, 10.5, '항원제시세포(수지상·대식·B)', fontsize=7, ha='center', color='#555')
    steps2 = ['외인성 항원\n(식균한 세균 단백)', '엔도솜·리소좀에서 분해',
              '(불변사슬 CLIP 교체)', 'MHC II에 적재', 'CD4+ 보조 T세포']
    for t, y in zip(steps2, ys):
        box(6.7, y, 4.6, 1.0, t, '#fdecea')
    for i in range(len(ys)-1):
        ax.annotate('', (9.0, ys[i+1]+1.0), (9.0, ys[i]),
                    arrowprops=dict(arrowstyle='->', color='#c0392b'))

    ax.text(6.0, 1.6, 'MHC I = CD8(세포독성) · MHC II = CD4(보조)  —  "8×1 = 2×4" 규칙',
            fontsize=7.4, ha='center', color='#555', weight='bold')
    ax.set_title('항원제시 — 내인성(MHC I) vs 외인성(MHC II)', fontsize=10.5, color=NAVY, weight='bold')
    return _save(fig, 'antigen_presentation')


def pk_curves():
    """혈중농도-시간곡선 — 정맥 vs 경구, 치료역(MEC~MTC)."""
    import numpy as np
    fig, ax = _new(5.4, 3.4)
    t = np.linspace(0, 12, 300)
    iv = 100 * np.exp(-0.35 * t)                       # 정맥: 즉시 최고 후 소실
    ka, ke = 1.1, 0.35
    oral = 60 * (ka / (ka - ke)) * (np.exp(-ke * t) - np.exp(-ka * t))  # 경구: 흡수+소실
    ax.plot(t, iv, color='#c0392b', lw=2, label='정맥주사(IV)')
    ax.plot(t, oral, color='#1565c0', lw=2, label='경구(초회통과·흡수)')
    ax.axhline(70, color='#e08a00', ls=':', lw=0.9)
    ax.axhline(20, color='#2e7d32', ls=':', lw=0.9)
    ax.text(9.5, 73, 'MTC(최소독성농도)', fontsize=6.8, color='#e08a00')
    ax.text(9.5, 22, 'MEC(최소유효농도)', fontsize=6.8, color='#2e7d32')
    ax.annotate('치료역', (6, 45), fontsize=8, color='#555', ha='center')
    # 경구 Tmax
    it = int(np.argmax(oral))
    ax.plot(t[it], oral[it], 'ko', ms=4)
    ax.annotate('Tmax', (t[it], oral[it]), (t[it]+0.6, oral[it]+8), fontsize=7, color='#1565c0')
    ax.set_xlabel('시간', fontsize=8.5); ax.set_ylabel('혈중 약물농도', fontsize=8.5)
    ax.set_ylim(0, 105); ax.legend(fontsize=7.6, loc='upper right'); ax.tick_params(labelsize=7.5)
    ax.set_title('혈중농도-시간곡선 — 정맥 vs 경구', fontsize=10.5, color=NAVY, weight='bold')
    fig.tight_layout()
    return _save(fig, 'pk_curves')


def autonomic_receptors():
    """자율신경 수용체 지도 — 교감(아드레날린) vs 부교감(콜린)."""
    fig, ax = _new(5.8, 4.2)
    ax.set_xlim(0, 12); ax.set_ylim(0, 12); ax.axis('off')

    def box(x, y, w, h, t, fc, tc='#20303d', fs=6.8):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec='#888', lw=0.9))
        ax.text(x + w/2, y + h/2, t, fontsize=fs, ha='center', va='center', color=tc)

    # 교감 (왼쪽)
    ax.text(3.0, 11.3, '교감신경 (아드레날린성)', fontsize=9, ha='center', weight='bold', color='#c0392b')
    ax.text(3.0, 10.6, '절후 노르에피네프린 · 부신속질 에피네프린', fontsize=6.6, ha='center', color='#555')
    symp = [
        ('α1', '혈관수축·산동·전립샘/방광목 수축 (차단=프라조신·탐수로신)', 9.3),
        ('α2', '시냅스전 음성되먹임 (NE 분비↓)', 7.9),
        ('β1', '심박·수축력↑·레닌분비 (차단=베타차단제)', 6.5),
        ('β2', '기관지·혈관 확장·자궁이완 (작용=살부타몰·리토드린)', 5.1),
    ]
    for r, eff, y in symp:
        box(0.5, y, 1.0, 1.0, r, '#fdecea', '#c0392b', 8)
        ax.text(1.7, y + 0.5, eff, fontsize=6.5, va='center', color='#333')

    # 부교감 (오른쪽/아래)
    ax.text(3.0, 3.9, '부교감신경 (콜린성) · 절후 아세틸콜린', fontsize=9, ha='center',
            weight='bold', color='#1565c0')
    para = [
        ('M2', '심박↓·전도↓ (심장)', 2.6),
        ('M3', '분비·평활근 수축·축동·조절수축 (작용=필로카르핀)', 1.4),
        ('Nn/Nm', '신경절·신경근접합부 (니코틴 수용체)', 0.2),
    ]
    for r, eff, y in para:
        box(0.5, y, 1.0, 1.0, r, '#e3f2fd', '#1565c0', 7.5)
        ax.text(1.7, y + 0.5, eff, fontsize=6.5, va='center', color='#333')

    ax.set_title('자율신경 수용체 지도 — 교감(α·β) vs 부교감(M·N)',
                 fontsize=10, color=NAVY, weight='bold')
    return _save(fig, 'autonomic_receptors')


ALL = [spinal_tracts, adrenal_zones, sarcomere, filtration_barrier,
       liver_zones, cerebellar_layers, respiratory_tree, atrial_septum,
       tca_cycle, electron_transport, urea_cycle, o2_dissociation,
       glucose_alanine, fasting_fuel,
       flow_volume_loop, cerebral_autoregulation,
       antagonist_curves, therapeutic_index,
       glycolysis, tca_energy, energy_overview, visual_field_defects,
       pv_loop, cardiac_ap, cardiac_venous_return, menstrual_cycle, glucose_titration,
       knudson_2hit, gn_immunofluorescence,
       gram_wall, antigen_presentation,
       pk_curves, autonomic_receptors]

if __name__ == '__main__':
    for fn in ALL:
        print('생성:', fn())
