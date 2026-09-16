#!/usr/bin/env python3
"""
Build ~/Desktop/e-yantra/LEARNING-ROADMAP.pdf from roadmap.md (same folder).

Understands only the Markdown subset roadmap.md uses: headings, paragraphs,
bullets, numbered lists, "- [ ]" checkboxes (-> clickable PDF checkboxes),
tables (empty-row tables -> fillable log tables), the map code block (-> drawn
diagram) and <details> answers (-> "Answers" section at the end).

Re-running overwrites the PDF, so ticks saved into it would be lost: the old
PDF is first copied to backups/ with its timestamp.
"""
import os
import re
import shutil
import time

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'roadmap.md')
OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'LEARNING-ROADMAP.pdf'))

# ---- Fonts & palette ---------------------------------------------------------
FD = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV', FD + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DV-B', FD + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DV-I', FD + 'DejaVuSans-Oblique.ttf'))
pdfmetrics.registerFont(TTFont('DV-BI', FD + 'DejaVuSans-BoldOblique.ttf'))
pdfmetrics.registerFont(TTFont('DVM', FD + 'DejaVuSansMono.ttf'))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-B', italic='DV-I', boldItalic='DV-BI')

NAVY = colors.HexColor('#122648')      # the e-Yantra turtlesim background
INK = colors.HexColor('#1f2430')
MUTED = colors.HexColor('#5b6475')
RULE = colors.HexColor('#d5dae3')
ZEBRA = colors.HexColor('#f4f6fa')
LINK = '#1a5fb4'
AMBER = colors.HexColor('#f59f00')
AMBER_DARK = colors.HexColor('#9a5b00')
AMBER_TINT = colors.HexColor('#fff4e0')
BOX_TINT = colors.HexColor('#eef2f8')

CHIP = {  # label -> (background tint, text colour)
    'WATCH': ('#dbe7ff', '#1c4ea3'), 'WATCH / READ': ('#dbe7ff', '#1c4ea3'),
    'TALK': ('#ece3ff', '#5b3cc4'), 'DO': ('#dcf5e4', '#1b7a3d'),
    'TEACH': ('#ffe8cc', '#a14b00'), 'CHECK': ('#e6eaef', '#394656'),
}

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

S = {
    'body': ParagraphStyle('body', fontName='DV', fontSize=9.6, leading=13.8, textColor=INK,
                           spaceAfter=5, alignment=TA_LEFT),
    'title': ParagraphStyle('title', fontName='DV-B', fontSize=19, leading=24, textColor=NAVY,
                            spaceAfter=4),
    'subtitle': ParagraphStyle('subtitle', fontName='DV', fontSize=10.5, leading=15,
                               textColor=MUTED, spaceAfter=10),
    'h1': ParagraphStyle('h1', fontName='DV-B', fontSize=15, leading=19, textColor=NAVY,
                         spaceBefore=12, spaceAfter=6),
    'h2': ParagraphStyle('h2', fontName='DV-B', fontSize=11.5, leading=15,
                         textColor=colors.HexColor('#2b3a55'), spaceBefore=8, spaceAfter=4),
    'cell': ParagraphStyle('cell', fontName='DV', fontSize=8.6, leading=11.6, textColor=INK),
    'cellhead': ParagraphStyle('cellhead', fontName='DV-B', fontSize=8.6, leading=11.6,
                               textColor=colors.white),
    'bullet': ParagraphStyle('bullet', fontName='DV', fontSize=9.6, leading=13.6, textColor=INK,
                             leftIndent=14, bulletIndent=3, spaceAfter=2),
    'item': ParagraphStyle('item', fontName='DV', fontSize=9.6, leading=13.2, textColor=INK),
    'toc': ParagraphStyle('toc', fontName='DV', fontSize=9.4, leading=14.5, textColor=INK),
    'small': ParagraphStyle('small', fontName='DV-I', fontSize=8, leading=11, textColor=MUTED),
}


# ---- Inline Markdown -> reportlab paragraph markup ---------------------------
def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline(text):
    keep = []

    def stash(markup):
        keep.append(markup)
        return f'\x00{len(keep) - 1}\x00'

    text = text.replace('\\*', stash('*'))
    text = re.sub(r'`([^`]+)`', lambda m: stash(
        f'<font name="DVM" size="8.8" color="#3d2a73">{esc(m.group(1))}</font>'), text)
    text = esc(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: stash(
        f'<link href="{m.group(2)}" color="{LINK}"><u>{inline_simple(m.group(1))}</u></link>'), text)
    text = inline_simple(text)
    while '\x00' in text:
        text = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], text)
    return text


def inline_simple(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<![\*\w])\*(?!\s)([^*]+?)(?<!\s)\*(?!\*)', r'<i>\1</i>', text)
    return text


def plain(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return re.sub(r'[*`\\]', '', text)


def slug(text, n=40):
    return re.sub(r'[^a-z0-9]+', '_', plain(text).lower())[:n].strip('_')


# ---- Custom flowables --------------------------------------------------------
class Bookmarked(Flowable):
    """Zero-size marker: registers a PDF bookmark + outline entry where it lands."""

    def __init__(self, key, title, level=0):
        super().__init__()
        self.key, self.title, self.level = key, title, level
        self.width = self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.title, self.key, level=self.level, closed=False)


class ModuleBand(Flowable):
    def __init__(self, code, title, meta, accent=False):
        super().__init__()
        self.code, self.title, self.meta, self.accent = code, title, meta, accent

    def wrap(self, aw, ah):
        self.width = aw
        self.height = 40
        return aw, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.width, self.height, 6, stroke=0, fill=1)
        if self.accent:
            c.setFillColor(AMBER)
            c.rect(0, 0, 5, self.height, stroke=0, fill=1)
        c.setFillColor(AMBER)
        c.setFont('DV-B', 19)
        c.drawString(14, 12.5, self.code)
        code_w = pdfmetrics.stringWidth(self.code, 'DV-B', 19)
        c.setFillColor(colors.white)
        c.setFont('DV-B', 13)
        c.drawString(26 + code_w, 14, self.title)
        if self.meta:
            c.setFillColor(colors.HexColor('#c9d3e6'))
            c.setFont('DV', 8.3)
            c.drawRightString(self.width - 12, 15, self.meta)


class Chip(Flowable):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.bg, self.fg = CHIP[label]
        self.width = pdfmetrics.stringWidth(label, 'DV-B', 7.6) + 14
        self.height = 14

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor(self.bg))
        c.roundRect(0, 0, self.width, self.height, 4, stroke=0, fill=1)
        c.setFillColor(colors.HexColor(self.fg))
        c.setFont('DV-B', 7.6)
        c.drawCentredString(self.width / 2, 4, self.label)


class CheckItem(Flowable):
    """A clickable PDF checkbox followed by a paragraph."""
    GUTTER = 17

    def __init__(self, para, name, tooltip):
        super().__init__()
        self.para, self.name, self.tooltip = para, name, tooltip

    def wrap(self, aw, ah):
        _, ph = self.para.wrap(aw - self.GUTTER, ah)
        self.width, self.height = aw, max(ph, 12)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.acroForm.checkboxRelative(
            name=self.name, tooltip=self.tooltip[:120], x=0.5, y=self.height - 11.5, size=10.5,
            buttonStyle='check', borderColor=NAVY, fillColor=colors.white, textColor=NAVY,
            borderWidth=0.9, forceBorder=True, checked=False)
        self.para.drawOn(c, self.GUTTER, 0)

    def getSpaceAfter(self):
        return 4


class FormTable(Flowable):
    """A table whose empty cells are fillable PDF text fields."""

    def __init__(self, headers, weights, rows, row_h, prefix):
        super().__init__()
        self.headers, self.weights, self.rows = headers, weights, rows
        self.row_h, self.prefix, self.head_h = row_h, prefix, 17

    HEAD_FONT, HEAD_SIZE, HEAD_LEAD = 'DV-B', 7.6, 9.2

    def _head_lines(self, text, width):
        lines, cur = [], ''
        for word in text.split():
            trial = f'{cur} {word}'.strip()
            if cur and pdfmetrics.stringWidth(trial, self.HEAD_FONT, self.HEAD_SIZE) > width:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        return lines + [cur]

    def wrap(self, aw, ah):
        total = sum(self.weights)
        self.widths = [aw * w / total for w in self.weights]
        self.head_lines = [self._head_lines(h, w - 8) for h, w in zip(self.headers, self.widths)]
        self.head_h = 8 + self.HEAD_LEAD * max(len(l) for l in self.head_lines)
        self.width, self.height = aw, self.head_h + self.rows * self.row_h
        return self.width, self.height

    def draw(self):
        c = self.canv
        top = self.height
        c.setFillColor(NAVY)
        c.rect(0, top - self.head_h, self.width, self.head_h, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont(self.HEAD_FONT, self.HEAD_SIZE)
        x = 0
        for lines, w in zip(self.head_lines, self.widths):
            for k, text in enumerate(lines):
                c.drawString(x + 4, top - 11 - k * self.HEAD_LEAD, text)
            x += w
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        for r in range(self.rows):
            y = top - self.head_h - (r + 1) * self.row_h
            x = 0
            for col, w in enumerate(self.widths):
                c.acroForm.textfieldRelative(
                    name=f'{self.prefix}_r{r + 1}_c{col + 1}', tooltip=self.headers[col],
                    x=x + 1.5, y=y + 1.5, width=w - 3, height=self.row_h - 3,
                    fontName='Helvetica', fontSize=8, borderWidth=0,
                    fillColor=colors.HexColor('#fbfcfe'), textColor=INK,
                    fieldFlags='multiline', forceBorder=False)
                x += w
            c.line(0, y, self.width, y)
        x = 0
        for w in self.widths[:-1]:
            x += w
            c.line(x, 0, x, top - self.head_h)
        c.rect(0, 0, self.width, top, stroke=1, fill=0)


def map_drawing(width):
    """Module map: KD track as a two-row snake, PacBot track, then after-Task-1 modules."""
    gap, bh = 16, 44
    bw = (width - 3 * gap) / 4
    rows = {'kd1': 262, 'kd2': 182, 'pb': 96, 'after': 12}
    h = 330
    d = Drawing(width, h)
    graded = {'M1', 'M6', 'M7', 'P2', 'P3'}

    def arrow(x1, y1, x2, y2, colour=NAVY):
        d.add(Line(x1, y1, x2, y2, strokeColor=colour, strokeWidth=1.2))
        if x2 != x1:
            sgn = 1 if x2 > x1 else -1
            d.add(Polygon([x2, y2, x2 - 5 * sgn, y2 + 3, x2 - 5 * sgn, y2 - 3], fillColor=colour, strokeColor=colour))
        else:
            sgn = 1 if y2 > y1 else -1
            d.add(Polygon([x2, y2, x2 - 3, y2 - 5 * sgn, x2 + 3, y2 - 5 * sgn], fillColor=colour, strokeColor=colour))

    def box(code, lines, col, y, style='kd'):
        x = col * (bw + gap)
        task = code in graded
        if style == 'after':
            fill, stroke, fg, codec = colors.white, MUTED, MUTED, MUTED
        elif style == 'pb':
            fill, stroke, fg, codec = (AMBER_DARK, AMBER_DARK, colors.white, AMBER_TINT) if task else (AMBER_TINT, AMBER_DARK, AMBER_DARK, AMBER_DARK)
        else:
            fill, stroke, fg, codec = (NAVY, NAVY, colors.white, AMBER) if task else (BOX_TINT, NAVY, NAVY, NAVY)
        r = Rect(x, y, bw, bh, rx=5, ry=5, fillColor=fill, strokeColor=AMBER if code == 'M3' else stroke,
                 strokeWidth=2 if code == 'M3' else 0.9)
        if style == 'after':
            r.strokeDashArray = [3, 2]
        d.add(r)
        d.add(String(x + bw / 2, y + bh - 14, code, fontName='DV-B', fontSize=10, fillColor=codec, textAnchor='middle'))
        for j, t in enumerate(lines):
            d.add(String(x + bw / 2, y + bh - 26 - j * 9.5, t, fontName='DV-B' if (task and j == 0) else 'DV',
                         fontSize=6.8, fillColor=fg, textAnchor='middle'))

    def label(y, text, colour):
        d.add(String(0, y + bh + 5, text, fontName='DV-B', fontSize=7.8, fillColor=colour))

    label(rows['kd1'], 'Khoj-o-Drone track', NAVY)
    for col, (code, lines) in enumerate([('M0', ['Big picture']), ('M1', ['KD 1A · 20 marks', 'computer vision']),
                                         ('M2', ['How a drone', 'flies']), ('M3', ['Feedback & PID', '★ core of 4 tasks'])]):
        box(code, lines, col, rows['kd1'])
    for col, (code, lines) in enumerate([('M4', ['ROS 2', '(just enough)']), ('M5', ['MuJoCo &', 'Swift Pico sim']),
                                         ('M6', ['KD 1B · 40 marks', 'tune altitude']), ('M7', ['KD 1C · 40 marks', 'tune x and y'])]):
        box(code, lines, col, rows['kd2'])
    for col in range(3):
        x = col * (bw + gap)
        arrow(x + bw + 2, rows['kd1'] + bh / 2, x + bw + gap - 2, rows['kd1'] + bh / 2)
        arrow(x + bw + 2, rows['kd2'] + bh / 2, x + bw + gap - 2, rows['kd2'] + bh / 2)
    m3_cx = 3 * (bw + gap) + bw / 2
    mid = (rows['kd1'] + rows['kd2'] + bh) / 2
    d.add(Line(m3_cx, rows['kd1'] - 2, m3_cx, mid, strokeColor=NAVY, strokeWidth=1.2))
    d.add(Line(m3_cx, mid, bw / 2, mid, strokeColor=NAVY, strokeWidth=1.2))
    arrow(bw / 2, mid, bw / 2, rows['kd2'] + bh + 2)

    label(rows['pb'], 'PacBot track (MQTT, planning, wall-following PID)', AMBER_DARK)
    for col, (code, lines) in enumerate([('P1', ['MQTT', 'broker & topics']), ('P2', ['PB 1A · 35 marks', 'maze path planning']),
                                         ('P3', ['PB 1B · 65 marks', 'wall-follow PID (uses M3)'])]):
        box(code, lines, col, rows['pb'], style='pb')
    for col in range(2):
        x = col * (bw + gap)
        arrow(x + bw + 2, rows['pb'] + bh / 2, x + bw + gap - 2, rows['pb'] + bh / 2, colour=AMBER_DARK)
    lx = 3 * (bw + gap) + 6
    d.add(Rect(lx, rows['pb'] + 30, 12, 9, fillColor=NAVY, strokeColor=NAVY, strokeWidth=0.6))
    d.add(String(lx + 17, rows['pb'] + 31.5, 'graded Task 1 part', fontName='DV', fontSize=7, fillColor=MUTED))
    d.add(Rect(lx, rows['pb'] + 13, 12, 9, fillColor=BOX_TINT, strokeColor=AMBER, strokeWidth=1.6))
    d.add(String(lx + 17, rows['pb'] + 14.5, 'core idea', fontName='DV', fontSize=7, fillColor=MUTED))

    label(rows['after'], 'After Task 1', MUTED)
    box('L1', ['Modelling, stability', '& LQR'], 0, rows['after'], style='after')
    box('T2', ['Task 2 preview', 'camera + search'], 1, rows['after'], style='after')
    return d


# ---- Tables ------------------------------------------------------------------
def col_weights(rows):
    head = [plain(c) for c in rows[0]]
    if head[:2] == ['Word', 'What it actually is']:
        return [0.18, 0.38, 0.27, 0.17]
    if head == ['Property', 'Value']:
        return [0.32, 0.68]
    if head == ['Week', 'Modules']:
        return [0.3, 0.7]
    n = len(head)
    weights = []
    for c in range(n):
        lens = [len(plain(r[c])) for r in rows]
        weights.append(max(8, 0.6 * min(max(lens), 60) + 0.4 * sum(lens) / len(lens)))
    return weights


def md_table(rows):
    weights = col_weights(rows)
    total = sum(weights)
    widths = [CONTENT_W * w / total for w in weights]
    data = [[Paragraph(inline(c), S['cellhead']) for c in rows[0]]]
    data += [[Paragraph(inline(c), S['cell']) for c in r] for r in rows[1:]]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, RULE),
        ('BOX', (0, 0), (-1, -1), 0.6, RULE),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(2, len(data), 2):
        style.append(('BACKGROUND', (0, i), (-1, i), ZEBRA))
    t.setStyle(TableStyle(style))
    return t


# ---- Markdown blocks -> story ------------------------------------------------
BAND_RE = re.compile(r'^([MPLT]\d) — (.+?)(?: · (.+))?$')
LABEL_RE = re.compile(r'^\*\*(WATCH / READ|WATCH|TALK|DO|TEACH|CHECK)(:?)\*\*\s*(.*)$')
PAGE_BREAK_BEFORE = re.compile(r'^([MPL]\d — |4\. |5\. |7\. )')


def parse(md):
    lines = md.split('\n')
    story, answers, toc = [], [], []
    title_done = False
    i = 0
    used_names = set()

    def unique(name):
        base, k = name or 'item', 1
        while name in used_names or not name:
            k += 1
            name = f'{base}_{k}'
        used_names.add(name)
        return name

    def label_row(label, rest):
        chip = Chip(label)
        if not rest:
            return Table([[chip]], colWidths=[CONTENT_W], hAlign='LEFT',
                         style=[('LEFTPADDING', (0, 0), (-1, -1), 0),
                                ('TOPPADDING', (0, 0), (-1, -1), 6),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 3)])
        return Table([[chip, Paragraph(inline(rest), S['item'])]],
                     colWidths=[chip.width + 8, CONTENT_W - chip.width - 8], hAlign='LEFT',
                     style=[('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('TOPPADDING', (0, 0), (0, 0), 1.5),
                            ('TOPPADDING', (1, 0), (1, 0), 0),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6)])

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped == '---':
            i += 1
            continue

        if line.startswith('# ') and not title_done:
            story.append(Paragraph(inline(line[2:]), S['title']))
            story.append(Paragraph('Team eYRC#4817 · Khoj-o-Drone (primary) · PacBot (secondary)',
                                   S['subtitle']))
            story.append('__TOC__')
            title_done = True
            i += 1
            continue

        if line.startswith('## '):
            text = line[3:].strip()
            if PAGE_BREAK_BEFORE.match(text) and story:
                story.append(PageBreak())
            m = BAND_RE.match(text)
            if m or text.startswith('PacBot side-track'):
                if m:
                    code, title, meta = m.group(1), m.group(2), plain(m.group(3) or '')
                else:
                    code, title = 'PB', 'PacBot side-track'
                    meta = plain(text.split(' · ', 1)[1]) if ' · ' in text else ''
                key = code
                story.append(Bookmarked(key, f'{code} — {plain(title)}'))
                story.append(ModuleBand(code, plain(title), meta, accent=code in ('M1', 'M3', 'M6', 'M7', 'P2', 'P3')))
                story.append(Spacer(1, 8))
                toc.append((key, f'<b>{code}</b> — {esc(plain(title))}', 1))
            else:
                key = slug(text, 20)
                story.append(Bookmarked(key, plain(text)))
                story.append(Paragraph(inline(text), S['h1']))
                toc.append((key, esc(plain(text)), 0))
            i += 1
            continue

        if line.startswith('### '):
            story.append(Paragraph(inline(line[4:]), S['h2']))
            i += 1
            continue

        if stripped.startswith('```'):
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                block.append(lines[i])
                i += 1
            i += 1
            if any(b.startswith('M0 →') for b in block):
                story.append(map_drawing(CONTENT_W))
                story.append(Spacer(1, 6))
            continue

        if stripped.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            body = rows[1:]
            if body and all(all(not c for c in r) for r in body):   # fillable log table
                head = [plain(c) for c in rows[0]]
                if 'Axis' in head:
                    story.append(FormTable(head, [0.9, 0.7, 0.6, 0.6, 0.6, 3.2], 8, 22, 'tune'))
                else:
                    story.append(FormTable(head, [0.8, 1.2, 1.4, 1.4, 1.5, 1.4], 7, 34, 'log'))  # 9 rows keep the answers on the same page
                story.append(Spacer(1, 8))
            else:
                story.append(md_table(rows))
                story.append(Spacer(1, 8))
            continue

        m = LABEL_RE.match(stripped)
        if m:
            rest = m.group(3)
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(
                    r'^(\s*[-|#]|\s*\d+\. |\*\*[A-Z])', lines[i]):
                rest += ' ' + lines[i].strip()
                i += 1
            story.append(label_row(m.group(1), rest.strip()))
            continue

        item = re.match(r'^(- \[ \] |- |(\d+)\. )(.*)$', line)
        if item:
            text = item.group(3)
            i += 1
            while i < len(lines) and lines[i].startswith('  ') and lines[i].strip():
                text += ' ' + lines[i].strip()
                i += 1
            if item.group(1) == '- [ ] ':
                det = re.search(r'<details><summary>.*?</summary>(.*?)</details>', text)
                if det:
                    tag = re.search(r'([MPLT]\d-[a-z])', text)
                    answers.append((tag.group(1) if tag else '?', det.group(1).strip()))
                    text = text.replace(det.group(0), '<i>(Answers on the last page.)</i>')
                para = Paragraph(inline(text).replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>'),
                                 S['item'])
                story.append(CheckItem(para, unique('cb_' + slug(text)), plain(text)))
            elif item.group(2):
                story.append(Paragraph(inline(text), S['bullet'], bulletText=f'{item.group(2)}.'))
            else:
                story.append(Paragraph(inline(text), S['bullet'], bulletText='•'))
            continue

        para = [stripped]
        i += 1
        # a line opening with bold ("**Why it matters:** ...") starts a new paragraph
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^(#|\||- |\d+\. |```|---|\*\*)', lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        story.append(Paragraph(inline(' '.join(para)), S['body']))

    if answers:
        story.append(Bookmarked('answers', 'Answers'))
        story.append(Paragraph('Answers', S['h1']))
        toc.append(('answers', 'Answers', 0))
        for tag, text in answers:
            story.append(Paragraph(f'<b>{esc(tag)}</b> — {inline(text)}', S['body']))

    # table of contents (internal links to the bookmarks)
    toc_rows, left, right = [], [], []
    for key, label, level in toc:
        target = right if level == 1 else left
        target.append(Paragraph(f'<link href="#{key}" color="{LINK}">{label}</link>', S['toc']))
    for r in range(max(len(left), len(right))):
        toc_rows.append([left[r] if r < len(left) else '', right[r] if r < len(right) else ''])
    toc_table = Table(toc_rows, colWidths=[CONTENT_W * 0.46, CONTENT_W * 0.54], hAlign='LEFT',
                      style=[('BACKGROUND', (0, 0), (-1, -1), ZEBRA),
                             ('BOX', (0, 0), (-1, -1), 0.6, RULE),
                             ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                             ('LEFTPADDING', (0, 0), (-1, -1), 8),
                             ('TOPPADDING', (0, 0), (-1, -1), 1),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 1)])
    idx = story.index('__TOC__')
    story[idx:idx + 1] = [Paragraph('<b>Contents</b> <font size="8" color="#5b6475">'
                                    '(click to jump; the sidebar has bookmarks too)</font>',
                                    S['h2']),
                          KeepTogether([toc_table]), Spacer(1, 6)]
    return story


def footer(canv, doc):
    canv.saveState()
    canv.setFont('DV', 7.5)
    canv.setFillColor(MUTED)
    canv.drawString(MARGIN, 9 * mm, "Saurabh's Learning Roadmap · eYRC 2026-27 · Team 4817")
    canv.drawRightString(PAGE_W - MARGIN, 9 * mm, f'Page {doc.page}')
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canv.restoreState()


def main():
    if os.path.exists(OUT):
        backups = os.path.join(HERE, 'backups')
        os.makedirs(backups, exist_ok=True)
        stamp = time.strftime('%Y%m%d-%H%M%S', time.localtime(os.path.getmtime(OUT)))
        shutil.copy2(OUT, os.path.join(backups, f'LEARNING-ROADMAP-{stamp}.pdf'))

    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=MARGIN, bottomMargin=MARGIN + 4 * mm,
                          title="Saurabh's Learning Roadmap — eYRC 2026-27",
                          author='Team eYRC#4817 (prepared with Claude)',
                          subject='Learning roadmap: drones, PID, ROS 2, MuJoCo, MQTT')
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='body',
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='page', frames=[frame], onPage=footer)])
    story = parse(open(SRC, encoding='utf-8').read())
    doc.build(story)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
