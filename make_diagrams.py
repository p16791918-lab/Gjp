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
    ax.plot(x, hb(26), color='#1565c0', lw=2, label='해수면 (정상)')
    ax.plot(x, hb(38), color='#c0392b', lw=2, label='고산 (2,3-BPG↑)')
    ax.axhline(50, color='#aaa', ls=':', lw=0.8)
    ax.annotate('오른쪽 이동\n= 산소친화도 감소', (55, 62), (60, 30), fontsize=8, color='#c0392b',
                arrowprops=dict(arrowstyle='->', color='#c0392b'))
    ax.set_xlabel('산소분압 pO₂ (mmHg)', fontsize=8.5)
    ax.set_ylabel('산소포화도 (%)', fontsize=8.5)
    ax.legend(fontsize=8, loc='lower right')
    ax.tick_params(labelsize=7.5)
    ax.set_title('산소-헤모글로빈 해리곡선 (2,3-BPG 효과)', fontsize=10.5, color=NAVY, weight='bold')
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


ALL = [spinal_tracts, adrenal_zones, sarcomere, filtration_barrier,
       liver_zones, cerebellar_layers, respiratory_tree, atrial_septum,
       tca_cycle, electron_transport, urea_cycle, o2_dissociation,
       glucose_alanine, fasting_fuel,
       flow_volume_loop, cerebral_autoregulation]

if __name__ == '__main__':
    for fn in ALL:
        print('생성:', fn())
