# -*- coding: utf-8 -*-
"""Генерация ассетов для Яндекс.Игр: иконка 512x512 и обложка 800x470."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.dirname(os.path.abspath(__file__))
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
BLACK = "C:/Windows/Fonts/ariblk.ttf"   # Arial Black — жирный, кириллица
BOLD  = "C:/Windows/Fonts/arialbd.ttf"

GOLD   = (255, 180, 60)
GOLD2  = (255, 217, 138)
CREAM  = (244, 230, 212)
LINE   = (90, 60, 34)
DARK   = (21, 15, 10)
PANEL  = (42, 26, 14)

def vgrad(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img

def emoji_img(ch, px):
    """Растеризует один цветной эмодзи в RGBA нужного размера."""
    strike = 109  # Segoe UI Emoji отдаёт битмапы страйком 109px
    f = ImageFont.truetype(EMOJI, strike)
    tmp = Image.new("RGBA", (strike * 2, strike * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text((strike * 0.5, strike * 0.4), ch, font=f, embedded_color=True, anchor="mm")
    bbox = tmp.getbbox()
    tmp = tmp.crop(bbox)
    scale = px / max(tmp.size)
    return tmp.resize((int(tmp.width * scale), int(tmp.height * scale)), Image.LANCZOS)

def paste_center(base, layer, cx, cy):
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def rounded_border(draw, box, rad, color, width):
    draw.rounded_rectangle(box, radius=rad, outline=color, width=width)

# ---------- ИКОНКА 512x512 ----------
def make_icon():
    S = 512
    img = vgrad((S, S), (61, 39, 22), (17, 11, 7)).convert("RGBA")
    # тёплое свечение сверху
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-120, -260, S + 120, 240), fill=(255, 180, 60, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img.alpha_composite(glow)

    d = ImageDraw.Draw(img)
    # золотая рамка-скругление
    rounded_border(d, (14, 14, S - 14, S - 14), 70, LINE, 10)
    rounded_border(d, (24, 24, S - 24, S - 24), 62, GOLD, 6)

    # кабан крупно
    boar = emoji_img("🐗", 300)
    paste_center(img, boar, S / 2, 220)

    # чипсы под пятаком
    chips = emoji_img("🥔", 110)
    paste_center(img, chips, S / 2 - 96, 360)
    fries = emoji_img("🍟", 110)
    paste_center(img, fries, S / 2 + 96, 360)

    # надпись КАБАН
    f = ImageFont.truetype(BLACK, 96)
    d.text((S / 2 + 3, 455 + 3), "КАБАН", font=f, fill=(40, 22, 6), anchor="mm")
    d.text((S / 2, 455), "КАБАН", font=f, fill=GOLD, anchor="mm")
    return img.convert("RGB")

# ---------- ОБЛОЖКА 800x470 ----------
def make_cover():
    W, H = 800, 470
    img = vgrad((W, H), (61, 39, 22), (17, 11, 7)).convert("RGBA")
    # деревянные полосы-фон
    stripes = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripes)
    for x in range(0, W, 76):
        sd.rectangle((x, 0, x + 38, H), fill=(255, 255, 255, 8))
    img.alpha_composite(stripes)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-160, -320, W + 160, 260), fill=(255, 180, 60, 55))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    img.alpha_composite(glow)

    d = ImageDraw.Draw(img)
    rounded_border(d, (10, 10, W - 10, H - 10), 26, LINE, 8)
    rounded_border(d, (18, 18, W - 18, H - 18), 22, GOLD, 4)

    # кабан слева
    boar = emoji_img("🐗", 250)
    paste_center(img, boar, 175, 235)
    chips = emoji_img("🥔", 84)
    paste_center(img, chips, 78, 388)
    fries = emoji_img("🍟", 84)
    paste_center(img, fries, 232, 398)

    # ООО
    fo = ImageFont.truetype(BOLD, 22)
    d.text((470, 108), "О О О", font=fo, fill=(169, 138, 107), anchor="mm")
    # заголовок
    ft = ImageFont.truetype(BLACK, 78)
    for line, y in (("«КАБАН", 185), ("БЛИН»", 268)):
        d.text((470 + 3, y + 3), line, font=ft, fill=(40, 22, 6), anchor="mm")
        d.text((470, y), line, font=ft, fill=GOLD, anchor="mm")
    # подзаголовок-плашка
    d.rounded_rectangle((330, 325, 610, 372), radius=12, fill=(42, 26, 14), outline=LINE, width=2)
    fs = ImageFont.truetype(BOLD, 25)
    d.text((470, 349), "ЧИПСЫ  КАБАНА", font=fs, fill=GOLD2, anchor="mm")
    fh = ImageFont.truetype(BOLD, 18)
    d.text((510, 402), "торгуй за прилавком • ХРУСТИМ С 1997", font=fh, fill=(169, 138, 107), anchor="mm")
    return img.convert("RGB")

icon = make_icon()
icon.save(os.path.join(OUT, "icon-512.png"))
cover = make_cover()
cover.save(os.path.join(OUT, "cover-800x470.png"))
print("saved:", icon.size, cover.size)
