#!/usr/bin/env python3
"""
Toiture Fortin — Fill Quote Template using overlay on original PDF
Usage: python3 fill_quote.py --date "7 mars 2026" --address "868 chemin des Hirondelles, Saint-Bruno-de-Montarville" --items "Description;Price" --out /tmp/quote.pdf
"""

import argparse
import fitz  # pymupdf
import os

TEMPLATE = os.path.expanduser(
    "~/.openclaw/workspace/memory/toiture_fortin_blank_template.pdf"
)

TPS_RATE = 0.05
TVQ_RATE = 0.09975

# Colors (RGB 0-1)
BLACK = (0.0, 0.0, 0.0)
RED   = (0.75, 0.22, 0.17)

def insert_text(page, x, y, text, fontsize=9.5, color=BLACK, fontname="helv", bold=False):
    """Insert text at exact position."""
    if bold:
        fontname = "Helvetica-Bold"
    page.insert_text(
        (x, y),
        text,
        fontsize=fontsize,
        color=color,
        fontname=fontname,
    )

def insert_text_right(page, right_x, y, text, fontsize=9.5, color=BLACK):
    """Insert text right-aligned to right_x."""
    tw = fitz.get_text_length(text, fontname="helv", fontsize=fontsize)
    x = right_x - tw
    page.insert_text((x, y), text, fontsize=fontsize, color=color, fontname="helv")


def make_quote(date_str, address, items, out_path):
    doc = fitz.open(TEMPLATE)
    page = doc[0]

    # ── DATE (after "Date" label at x=421.38, y=155.33) ──────────────────
    insert_text(page, 455, 155.5, date_str, fontsize=9.5)

    # ── ADDRESS (after "Adresse :" at x=38.86, y=177.59) ─────────────────
    insert_text(page, 98, 177.7, address, fontsize=9.5)

    # ── LINE ITEMS ─────────────────────────────────────────────────────────
    # Table header row: y=242.44. First data row starts at y≈260
    desc_x   = 42.0   # left of Description column
    price_rx = 575.0  # right edge of Prix column (right-align to here)
    row_h    = 18.0   # height per row
    y_start  = 262.0

    subtotal = 0.0
    for i, (desc, price_str) in enumerate(items):
        y = y_start + i * row_h
        try:
            price = float(price_str)
        except:
            price = 0.0
        subtotal += price

        insert_text(page, desc_x, y, desc, fontsize=9.5)
        if price > 0:
            insert_text_right(page, price_rx, y, f"{price:,.2f}", fontsize=9.5)

    # ── TOTALS ─────────────────────────────────────────────────────────────
    tps   = subtotal * TPS_RATE
    tvq   = subtotal * TVQ_RATE
    total = subtotal + tps + tvq

    # "Sous-total" label is at x=424.11, y=592.72 → value right-aligned
    insert_text_right(page, price_rx, 592.8, f"{subtotal:,.2f}")
    insert_text_right(page, price_rx, 612.2, f"{tps:,.2f}")
    insert_text_right(page, price_rx, 631.0, f"{tvq:,.2f}")
    insert_text_right(page, price_rx, 649.7, f"{total:,.2f}")

    doc.save(out_path)
    doc.close()
    print(f"PDF saved: {out_path}")
    return total


def main():
    parser = argparse.ArgumentParser(description="Fill Toiture Fortin quote template")
    parser.add_argument('--date',    required=True)
    parser.add_argument('--address', required=True)
    parser.add_argument('--items',   required=True, nargs='+',
                        help='"Description;Price" — price 0 = blank')
    parser.add_argument('--out',     default='/tmp/toiture_fortin_soumission.pdf')
    args = parser.parse_args()

    items = []
    for item in args.items:
        parts = item.split(';', 1)
        desc  = parts[0].strip()
        price = parts[1].strip() if len(parts) > 1 else "0"
        items.append((desc, price))

    total = make_quote(args.date, args.address, items, args.out)
    tps   = sum(float(p) for _, p in items if p != "0") * TPS_RATE
    tvq   = sum(float(p) for _, p in items if p != "0") * TVQ_RATE
    subtotal = sum(float(p) for _, p in items if p != "0")
    print(f"Subtotal: {subtotal:,.2f}  TPS: {tps:,.2f}  TVQ: {tvq:,.2f}  Total: {total:,.2f}")


if __name__ == '__main__':
    main()
