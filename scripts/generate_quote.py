#!/usr/bin/env python3
"""
Toiture Fortin — Quote/Soumission PDF Generator
Usage: python3 generate_quote.py --date "7 mars 2026" --address "868 chemin des Hirondelles, Saint-Bruno-de-Montarville" --items "Lavage à pression avec dégraisseur;0" "Inspection du toit;0" "Application d'une couche d'élastomère Uniflex noir au fusil, épaisseur 30 millièmes;7500.00" --out /tmp/soumission.pdf
"""

import argparse
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether

RED = colors.HexColor('#C0392B')
DARK = colors.HexColor('#1a1a1a')
GREY = colors.HexColor('#555555')
WHITE = colors.white
LIGHT_GREY = colors.HexColor('#f5f5f5')

TPS_RATE = 0.05
TVQ_RATE = 0.09975
TPS_NUM = "793797606RT0001"
TVQ_NUM = "1228528567TQ001"
RBQ = "5802-4886-01"
NEQ = "1176568310"

PHONE_COLS = [
    ("Trois-Rivières", "819 414-1347"),
    ("Montréal",       "514 216-2436"),
    ("Québec",         "418 800-2782"),
    ("Ottawa",         "613 604-2852"),
    ("Gatineau",       "819 414-1347"),
    ("Toronto",        "647 361-7093"),
]

WARRANTY_FR = (
    "<b>3 ans de garantie</b> sur la peinture ou élastomère contre l'écaillement et la décoloration. "
    "Aucune réparation concernant vis, calfeutrage, joint et infiltration d'eau n'est garantie sous "
    "aucune forme que ce soit et <i>Toiture Fortin</i> se dégage de toute responsabilité ou dommage "
    "qui pourrait en découler."
)


def make_pdf(date_str, address, items, out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        rightMargin=0.6*inch,
        leftMargin=0.6*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
    )

    styles = getSampleStyleSheet()
    W = letter[0] - 1.2*inch  # usable width

    story = []

    # ── HEADER ──────────────────────────────────────────────────────────────
    # Company name + subtitle
    title_style = ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=26,
                                  textColor=DARK, alignment=TA_CENTER, spaceAfter=2)
    sub_style   = ParagraphStyle('sub', fontName='Helvetica', fontSize=9,
                                  textColor=DARK, alignment=TA_CENTER,
                                  charSpace=3, spaceAfter=4)
    soum_style  = ParagraphStyle('soum', fontName='Helvetica-Bold', fontSize=18,
                                  textColor=DARK, alignment=TA_RIGHT)

    # Header row: logo area | company name | SOUMISSION
    header_data = [[
        Paragraph("🏠", ParagraphStyle('logo', fontSize=28, alignment=TA_LEFT)),
        Paragraph("TOITURE FORTIN<br/><font size=9 color='#555555'>&nbsp;&nbsp;PEINTURE DE TOITURE - ROOF PAINTER</font>",
                  ParagraphStyle('hdr', fontName='Helvetica-Bold', fontSize=22,
                                  textColor=DARK, alignment=TA_CENTER)),
        Paragraph("SOUMISSION", soum_style),
    ]]
    header_table = Table(header_data, colWidths=[0.9*inch, W-2.2*inch, 1.3*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(header_table)

    # Address line
    story.append(Paragraph(
        "243 boul. St-Joseph, St-Jean-sur-Richelieu (Québec) J3B1W8",
        ParagraphStyle('addr', fontName='Helvetica', fontSize=8,
                        textColor=GREY, alignment=TA_CENTER, spaceAfter=4)
    ))

    # Red divider
    story.append(HRFlowable(width="100%", thickness=1.5, color=RED, spaceAfter=5))

    # Phone numbers — 3 columns of 2 rows
    ph_style   = ParagraphStyle('ph', fontName='Helvetica', fontSize=8, textColor=DARK)
    city_style = ParagraphStyle('city', fontName='Helvetica-Bold', fontSize=8, textColor=RED)

    ph_rows = []
    for i in range(0, len(PHONE_COLS), 3):
        row = []
        for city, num in PHONE_COLS[i:i+3]:
            row.append(Paragraph(f"<font color='#C0392B'><b>{city}</b></font>  {num}", ph_style))
        ph_rows.append(row)

    ph_table = Table(ph_rows, colWidths=[W/3]*3)
    ph_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(ph_table)
    story.append(Spacer(1, 6))

    # ── INFO ROW: RBQ / NEQ / DATE ───────────────────────────────────────
    lbl = ParagraphStyle('lbl', fontName='Helvetica-Bold', fontSize=8, textColor=DARK)
    val = ParagraphStyle('val', fontName='Helvetica', fontSize=8, textColor=DARK)

    info_data = [[
        Paragraph(f"<b>R.B.Q</b> {RBQ}", lbl),
        Paragraph(f"<b>NEQ</b> {NEQ}", lbl),
        Paragraph(f"<b>Date</b>&nbsp;&nbsp;{date_str}", lbl),
    ]]
    info_table = Table(info_data, colWidths=[W*0.35, W*0.35, W*0.30])
    info_table.setStyle(TableStyle([
        ('BOX',    (0,0), (-1,-1), 0.5, DARK),
        ('INNERGRID', (0,0), (-1,-1), 0.5, DARK),
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GREY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(info_table)

    # ── ADDRESS ROW ──────────────────────────────────────────────────────
    addr_data = [[
        Paragraph("<b>Adresse :</b>", lbl),
        Paragraph(address, val),
    ]]
    addr_table = Table(addr_data, colWidths=[0.85*inch, W-0.85*inch])
    addr_table.setStyle(TableStyle([
        ('BOX',    (0,0), (-1,-1), 0.5, DARK),
        ('INNERGRID', (0,0), (-1,-1), 0.5, DARK),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(addr_table)

    # ── DESCRIPTION / PRICE TABLE ────────────────────────────────────────
    desc_hdr = ParagraphStyle('dh', fontName='Helvetica-Bold', fontSize=9, textColor=DARK)
    desc_body = ParagraphStyle('db', fontName='Helvetica', fontSize=8.5, textColor=DARK)
    price_style = ParagraphStyle('pr', fontName='Helvetica', fontSize=8.5,
                                  textColor=DARK, alignment=TA_RIGHT)

    table_data = [
        [Paragraph("<b>Description</b>", desc_hdr), Paragraph("<b>Prix</b>", desc_hdr)]
    ]

    subtotal = 0.0
    for desc, price_str in items:
        try:
            price = float(price_str)
        except:
            price = 0.0
        subtotal += price
        price_cell = Paragraph(f"{price:,.2f}" if price else "", price_style)
        table_data.append([Paragraph(desc, desc_body), price_cell])

    # Pad with empty rows to fill space (min 8 rows total)
    while len(table_data) < 10:
        table_data.append([Paragraph("", desc_body), Paragraph("", price_style)])

    desc_table = Table(table_data, colWidths=[W*0.82, W*0.18])
    desc_style = TableStyle([
        ('BOX',       (0,0), (-1,-1), 0.5, DARK),
        ('INNERGRID', (0,0), (-1,-1), 0.5, DARK),
        ('BACKGROUND',(0,0), (-1,0), LIGHT_GREY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])
    desc_table.setStyle(desc_style)
    story.append(desc_table)

    # ── TOTALS ────────────────────────────────────────────────────────────
    tps = subtotal * TPS_RATE
    tvq = subtotal * TVQ_RATE
    total = subtotal + tps + tvq

    total_lbl = ParagraphStyle('tl', fontName='Helvetica-Bold', fontSize=8.5,
                                textColor=DARK, alignment=TA_RIGHT)
    total_val = ParagraphStyle('tv', fontName='Helvetica', fontSize=8.5,
                                textColor=DARK, alignment=TA_RIGHT)
    total_big = ParagraphStyle('tb', fontName='Helvetica-Bold', fontSize=9,
                                textColor=DARK, alignment=TA_RIGHT)

    totals_data = [
        [Paragraph("<b>Sous-total</b>", total_lbl), Paragraph(f"{subtotal:,.2f}", total_val)],
        [Paragraph(f"<b>TPS : {TPS_NUM}</b>", total_lbl), Paragraph(f"{tps:,.2f}", total_val)],
        [Paragraph(f"<b>TVQ : {TVQ_NUM}</b>", total_lbl), Paragraph(f"{tvq:,.2f}", total_val)],
        [Paragraph("<b>Total</b>", total_big), Paragraph(f"<b>{total:,.2f}</b>", total_big)],
    ]
    totals_table = Table(totals_data, colWidths=[W*0.72, W*0.28])
    totals_table.setStyle(TableStyle([
        ('BOX',       (0,0), (-1,-1), 0.5, DARK),
        ('INNERGRID', (0,0), (-1,-1), 0.5, DARK),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,3), (-1,3), LIGHT_GREY),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 10))

    # ── FOOTER: WARRANTY + WEBSITE ────────────────────────────────────────
    warranty_style = ParagraphStyle('ws', fontName='Helvetica', fontSize=7.5,
                                     textColor=DARK, leading=11)
    site_style     = ParagraphStyle('ss', fontName='Helvetica-Bold', fontSize=16,
                                     textColor=DARK, alignment=TA_CENTER)
    merci_style    = ParagraphStyle('ms', fontName='Helvetica-Oblique', fontSize=13,
                                     textColor=DARK, alignment=TA_LEFT)
    thanks_style   = ParagraphStyle('ts', fontName='Helvetica-Oblique', fontSize=13,
                                     textColor=RED, alignment=TA_RIGHT)

    footer_data = [[
        [
            Paragraph("<b>GARANTIE :</b>", ParagraphStyle('gh', fontName='Helvetica-Bold',
                       fontSize=8, textColor=DARK, spaceAfter=3)),
            Paragraph(WARRANTY_FR, warranty_style),
        ],
        [
            Paragraph("toiturefortin.com", site_style),
            Spacer(1, 6),
            Table([[
                Paragraph("Merci !", merci_style),
                Paragraph("|", ParagraphStyle('pipe', fontName='Helvetica-Bold',
                           fontSize=13, textColor=RED, alignment=TA_CENTER)),
                Paragraph("Thank you !", thanks_style),
            ]], colWidths=[1.2*inch, 0.3*inch, 1.4*inch]),
        ],
    ]]

    footer_table = Table(footer_data, colWidths=[W*0.6, W*0.4])
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(footer_table)

    doc.build(story)
    print(f"PDF saved: {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate Toiture Fortin quote PDF")
    parser.add_argument('--date',    required=True, help='Quote date (e.g. "7 mars 2026")')
    parser.add_argument('--address', required=True, help='Client address')
    parser.add_argument('--items',   required=True, nargs='+',
                        help='Line items as "Description;Price" (price 0 = no price shown)')
    parser.add_argument('--out',     default='/tmp/toiture_fortin_soumission.pdf',
                        help='Output PDF path')
    args = parser.parse_args()

    items = []
    for item in args.items:
        parts = item.split(';', 1)
        desc  = parts[0].strip()
        price = parts[1].strip() if len(parts) > 1 else "0"
        items.append((desc, price))

    make_pdf(args.date, args.address, items, args.out)


if __name__ == '__main__':
    main()
