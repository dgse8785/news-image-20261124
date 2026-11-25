#!/usr/bin/env python3
"""Poster generator for the Tuesday 24 November 2026 news edition.

The artwork is a single square page that reads like the front of a
broadsheet: a masthead naming the day, one dominant lead story, four
smaller stories arranged as a two-by-two grid, a wide markets panel
underneath, and a closing strip that sweeps up the rest of the day.
All of the wording lives in plain data structures below, and the
drawing helpers only care about boxes, fonts and wrapped lines, so
the editorial content can be swapped without touching the layout
machinery.  Every coordinate and string is fixed, which makes the
rendered PNG fully deterministic.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 36
CONTENT = PAGE - MARGIN * 2
GAP = 12

BACKGROUND = (9, 19, 36)
PANEL = (18, 36, 61)
PANEL_LINE = (54, 79, 110)
INK = (236, 241, 248)
MUTED = (168, 184, 204)
YELLOW = (219, 181, 65)
RED = (235, 99, 84)
TEAL = (86, 199, 181)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_BOLD = "DejaVuSans-Bold.ttf"
FONT_PLAIN = "DejaVuSans.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(HERE, "entry.png")

LEAD = {
    "kicker": "LEAD - MIDDLE EAST",
    "headline": "HOUTHIS HIT RIYADH TOWER AGAIN",
    "body": (
        "Yemen's Houthis strike the PIF tower in Riyadh's financial "
        "district for the second time in five days, injuring 11 people: "
        "two Saudis, two Indians, three Nepalis and four Egyptians. "
        "Yemen's army says Houthi fighters are about 60 km from Aden "
        "and vows the city will hold."
    ),
    "accent": RED,
}

GRID = [
    {
        "kicker": "NATO - SPACE WARNING",
        "headline": "NATO SPACE WARNING",
        "body": (
            "NATO chief Mark Rutte vows the alliance will defend against "
            "any threat in space after reports that Russia is preparing "
            "to launch a nuclear-armed satellite."
        ),
        "accent": YELLOW,
    },
    {
        "kicker": "MIDDLE EAST - GAZA",
        "headline": "GAZA STRIKE",
        "body": (
            "Israeli airstrikes kill Hamas internal security chief Naeem "
            "Abu Nahal and six others, including two police officers, "
            "despite a ceasefire in place since last year."
        ),
        "accent": TEAL,
    },
    {
        "kicker": "SOUTH KOREA - EXAMS",
        "headline": "SEOUL AI CHEATING",
        "body": (
            "South Korea offers rewards of up to $375,000 to catch "
            "students using AI to cheat in the College Scholastic "
            "Ability Test, days after the education minister resigned "
            "over the scandal."
        ),
        "accent": TEAL,
    },
    {
        "kicker": "UKRAINE - ZAPORIZHZHIA",
        "headline": "ZAPORIZHZHIA HIT",
        "body": (
            "An overnight Russian attack on Zaporizhzhia kills two "
            "people and wounds 40, including four children, striking "
            "an apartment building."
        ),
        "accent": YELLOW,
    },
]

WIDE = {
    "kicker": "MARKETS - TARIFFS LOOM",
    "headline": "TARIFFS LOOM",
    "body": (
        "Trump is expected to announce tariffs on China, the EU and "
        "others; markets slip as a Fed official signals higher rates "
        "could come, and the S&P 500 falls 0.95%."
    ),
    "accent": YELLOW,
}

ALSO = [
    "Senegal reinstated as 2025 Africa Cup of Nations champion after sport's top court rules in its favour",
    "Russia warns Estonia of open war over its plan to close border crossings on 1 December",
    "China opens a corruption probe into Politburo member Chen Jining",
    "Spain's Supreme Court amnesties Carles Puigdemont",
    "Iraq's PM orders a takeover of Kurdish-controlled oilfields",
    "A US jury convicts Huawei of stealing trade secrets",
    "Saudi Arabia approves a SR1.39tn budget for 2027",
    "South Korea tells island residents to shelter after Russian jets enter its air defence zone",
]


def load_font(size, bold=False):
    name = FONT_BOLD if bold else FONT_PLAIN
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, width):
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_block(draw, x, y, text, font, colour, width, leading):
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=colour)
        y += leading
    return y


def draw_panel(draw, x, y, width, height, story, headline_size, body_size):
    draw.rounded_rectangle(
        [x, y, x + width, y + height], radius=12,
        fill=PANEL, outline=PANEL_LINE, width=2,
    )
    draw.rectangle([x, y + 10, x + 5, y + 52], fill=story["accent"])
    inner = width - 34
    cursor = draw_text_block(
        draw, x + 17, y + 11, story["kicker"],
        load_font(14, bold=True), story["accent"], inner, 18,
    )
    cursor = draw_text_block(
        draw, x + 17, cursor + 2, story["headline"],
        load_font(headline_size, bold=True), INK, inner, headline_size + 4,
    )
    draw_text_block(
        draw, x + 17, cursor + 4, story["body"],
        load_font(body_size), MUTED, inner, body_size + 5,
    )


def centred(draw, text, y, size, colour):
    font = load_font(size, bold=True)
    w = draw.textlength(text, font=font)
    draw.text(((PAGE - w) / 2, y), text, font=font, fill=colour)


def build():
    # One fresh canvas per call: no state is shared between renders,
    # so two consecutive builds cannot drift apart.
    image = Image.new("RGB", (PAGE, PAGE), BACKGROUND)
    draw = ImageDraw.Draw(image)

    centred(draw, "THE WORLD IN ONE IMAGE", 22, 40, INK)
    centred(draw, "TUESDAY - 24 NOVEMBER 2026", 74, 21, YELLOW)
    draw.rectangle([MARGIN, 110, PAGE - MARGIN, 114], fill=YELLOW)

    y = 126
    draw_panel(draw, MARGIN, y, CONTENT, 182, LEAD, 30, 17)
    y += 182 + GAP

    half = (CONTENT - GAP) // 2
    for row in range(2):
        for col in range(2):
            story = GRID[row * 2 + col]
            draw_panel(
                draw, MARGIN + col * (half + GAP), y, half, 158,
                story, 20, 14,
            )
        y += 158 + GAP

    draw_panel(draw, MARGIN, y, CONTENT, 106, WIDE, 20, 15)
    y += 106 + GAP

    draw.rectangle([MARGIN, y, PAGE - MARGIN, y + 3], fill=YELLOW)
    y = draw_text_block(
        draw, MARGIN, y + 11, "ALSO TODAY",
        load_font(16, bold=True), YELLOW, CONTENT, 20,
    )
    joined = "  /  ".join(ALSO)
    draw_text_block(draw, MARGIN, y + 4, joined, load_font(14), INK, CONTENT, 19)

    centred(draw, "Wire reports of 24 November 2026 - One page, one day", 990, 13, MUTED)
    image.save(OUT_FILE, format="PNG")
    return OUT_FILE


if __name__ == "__main__":
    print("Poster saved to", build())
