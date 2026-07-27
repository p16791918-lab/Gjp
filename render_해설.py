#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""기종평 문항별 해설 PDF 공용 렌더러.

연도·교시별 데이터 모듈(META dict + QUESTIONS list[dict])을 받아
  (1) 상세 해설 PDF
  (2) 빈출 집계용 JSON 데이터
를 함께 생성한다.

QUESTIONS 각 항목(dict) 스키마:
  num      : int   문항 번호
  ans      : int   정답 번호(1~5)
  subject  : str   과목 (예: '조직학', '해부학', '발생학')
  topic    : str   대주제 (빈출 집계 단위, 예: '내분비샘 조직')
  keywords : list  키워드(빈출 집계·검색용)
  q        : str   문제 요약
  exp      : str   정답 근거(기전·구조)
  bg       : str   관련 배경지식(개념 틀·분류·암기 포인트)   # optional
  note     : str   감별/오답 정리                            # optional
섹션 구분 헤더는 {'section': '...'} 한 줄로 넣는다.
"""
import json, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether,
    Image, Table, TableStyle
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

CONTENT_W = (210 - 32) * mm  # A4 폭 - 좌우 여백(16*2)

pdfmetrics.registerFont(TTFont('NanumGothic', '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'))
pdfmetrics.registerFont(TTFont('NanumGothicBold', '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'))

CIRCLED = {1: '①', 2: '②', 3: '③', 4: '④', 5: '⑤'}


def _styles():
    return {
        'title': ParagraphStyle('Title', fontName='NanumGothicBold', fontSize=18,
            textColor=colors.HexColor('#1a1a2e'), spaceAfter=6, leading=24, alignment=1),
        'subtitle': ParagraphStyle('Subtitle', fontName='NanumGothic', fontSize=11,
            textColor=colors.HexColor('#555555'), spaceAfter=10, leading=15, alignment=1),
        'section': ParagraphStyle('Section', fontName='NanumGothicBold', fontSize=13,
            textColor=colors.white, spaceAfter=6, spaceBefore=10, leading=18,
            backColor=colors.HexColor('#0f3460'), borderPad=6, leftIndent=4),
        'tag': ParagraphStyle('Tag', fontName='NanumGothic', fontSize=7.5,
            textColor=colors.HexColor('#0f3460'), spaceAfter=1, spaceBefore=8, leading=10),
        'qnum': ParagraphStyle('Qnum', fontName='NanumGothicBold', fontSize=10.5,
            textColor=colors.HexColor('#16213e'), spaceAfter=2, spaceBefore=1, leading=15),
        'ans': ParagraphStyle('Ans', fontName='NanumGothicBold', fontSize=10,
            textColor=colors.HexColor('#c0392b'), spaceAfter=3, leading=14),
        'exp': ParagraphStyle('Exp', fontName='NanumGothic', fontSize=9,
            textColor=colors.HexColor('#2c2c2c'), spaceAfter=3, leading=14, leftIndent=4),
        'bg': ParagraphStyle('Bg', fontName='NanumGothic', fontSize=8.5,
            textColor=colors.HexColor('#234e52'), spaceAfter=3, leading=13, leftIndent=10,
            backColor=colors.HexColor('#eaf4f4'), borderPad=4),
        'note': ParagraphStyle('Note', fontName='NanumGothic', fontSize=8.5,
            textColor=colors.HexColor('#5a5a5a'), spaceAfter=3, leading=13, leftIndent=10,
            backColor=colors.HexColor('#f4f6f9'), borderPad=4),
    }


def _figure_row(fig_paths, target_h=34*mm, gap=4*mm, max_h=40*mm):
    """사진 경로 리스트를 한 줄 이미지 Table 플로어블로 만든다(폭 초과 시 축소)."""
    paths = [p for p in fig_paths if p and os.path.exists(p)]
    if not paths:
        return None
    imgs, widths = [], []
    for p in paths:
        iw, ih = ImageReader(p).getSize()
        w = target_h * iw / ih
        imgs.append((p, w, target_h)); widths.append(w)
    total = sum(widths) + gap * (len(imgs) - 1)
    scale = min(1.0, CONTENT_W / total)
    cells = [Image(p, width=w*scale, height=h*scale) for (p, w, h) in imgs]
    col_w = [w*scale + (gap if i < len(cells)-1 else 0) for i, (_, w, _) in enumerate(imgs)]
    t = Table([cells], colWidths=col_w, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    return t


def build_pdf(meta, questions, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
        rightMargin=16*mm, leftMargin=16*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = _styles()
    story = [Spacer(1, 4*mm),
             Paragraph('기초의학종합평가 (KAMC)', s['subtitle']),
             Paragraph(meta['title'], s['title']),
             Paragraph(meta['subtitle'], s['subtitle']),
             HRFlowable(width='100%', thickness=2, color=colors.HexColor('#0f3460')),
             Spacer(1, 3*mm),
             Paragraph(
                 '※ 각 문항은 <b>정답 근거</b> → <b>관련 지식(배경)</b> → <b>감별/오답</b> 순으로 구성했습니다. '
                 '문항 위 [과목 · 대주제]는 연도별 빈출 집계용 태그입니다. '
                 '사진·그림 문항은 KAMC 공식 정답지를 기준으로 판단 요지를 정리했습니다.', s['exp']),
             Spacer(1, 3*mm)]

    for item in questions:
        if 'section' in item:
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph(item['section'], s['section']))
            continue
        block = []
        tag = f"[{item.get('subject','')} · {item.get('topic','')}]"
        block.append(Paragraph(tag, s['tag']))
        block.append(Paragraph(f"{item['num']}. {item['q']}", s['qnum']))
        fig = _figure_row(item.get('figs', []))
        if fig is not None:
            block.append(fig)
        block.append(Paragraph(f"정답 {CIRCLED[item['ans']]}", s['ans']))
        block.append(Paragraph(item['exp'], s['exp']))
        if item.get('bg'):
            block.append(Paragraph('■ 관련 지식: ' + item['bg'], s['bg']))
        if item.get('diag') and os.path.exists(item['diag']):
            iw, ih = ImageReader(item['diag']).getSize()
            w = min(102*mm, CONTENT_W)
            block.append(Image(item['diag'], width=w, height=w*ih/iw, hAlign='LEFT'))
        if item.get('note'):
            block.append(Paragraph('▸ 감별/오답: ' + item['note'], s['note']))
        block.append(HRFlowable(width='100%', thickness=0.4, color=colors.HexColor('#dddddd'),
                                spaceBefore=3, spaceAfter=1))
        story.append(KeepTogether(block))

    doc.build(story)
    print(f'PDF 생성 완료: {output_path}')


def save_json(meta, questions, output_path):
    """빈출 집계용 구조화 데이터 저장."""
    rows = []
    for item in questions:
        if 'section' in item:
            continue
        rows.append({
            'year': meta['year'], 'period': meta['period'],
            'num': item['num'], 'ans': item['ans'],
            'subject': item.get('subject', ''), 'topic': item.get('topic', ''),
            'keywords': item.get('keywords', []), 'q': item['q'],
        })
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({'meta': meta, 'questions': rows}, f, ensure_ascii=False, indent=2)
    print(f'JSON 데이터 저장: {output_path} ({len(rows)}문항)')


def render_all(meta, questions, pdf_path, json_path):
    build_pdf(meta, questions, pdf_path)
    save_json(meta, questions, json_path)
