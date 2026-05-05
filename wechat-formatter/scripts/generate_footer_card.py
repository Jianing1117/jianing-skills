#!/usr/bin/env python3
"""
generate_footer_card.py
生成「加宁慢慢来」品牌底部卡片图片，用于微信公众号文章末尾手动插入。

用法：
    python3 generate_footer_card.py --output /path/to/footer-card.png
    python3 generate_footer_card.py  # 默认输出到 Desktop
"""

import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("请先安装 Pillow：pip3 install pillow")
    raise

# ─────────────────────────────────────────────
# 品牌色板
# ─────────────────────────────────────────────
def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

C_NAVY  = hex_rgb("#2F4156")
C_TEAL  = hex_rgb("#567C8D")
C_BLUE  = hex_rgb("#C8D9E6")
C_LBLUE = hex_rgb("#EAF3F8")
C_DPINK = hex_rgb("#B07A72")
C_TEXT  = hex_rgb("#333333")
C_WHITE = (255, 255, 255)

AVATAR_PATH = Path("/Users/jnx/Desktop/jianing-avatar.JPG")
QRCODE_PATH = Path("/Users/jnx/Desktop/jianing-qrcode.JPG")

# ─────────────────────────────────────────────
# 工具
# ─────────────────────────────────────────────

def load_font(size):
    candidates = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
        "/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def circle_crop(img, size):
    img = img.resize((size, size), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def rounded_rect_fill(draw, x0, y0, x1, y1, r, fill):
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
    draw.ellipse([x0, y0, x0+2*r, y0+2*r], fill=fill)
    draw.ellipse([x1-2*r, y0, x1, y0+2*r], fill=fill)
    draw.ellipse([x0, y1-2*r, x0+2*r, y1], fill=fill)
    draw.ellipse([x1-2*r, y1-2*r, x1, y1], fill=fill)


def tw(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


# ─────────────────────────────────────────────
# 布局常量
# ─────────────────────────────────────────────
W          = 1080   # 总宽
CARD_PAD   = 44     # 卡片外边距
INNER_PAD  = 60     # 卡片内左右间距
AVATAR_D   = 152    # 头像直径
QR_SIZE    = 168    # 二维码尺寸
GAP_AV_TX  = 40     # 头像到文字左边距
GAP_TX_QR  = 36     # 文字区到二维码左边距
CARD_X0    = CARD_PAD
CARD_X1    = W - CARD_PAD
CARD_W     = CARD_X1 - CARD_X0
# 各列 x 位置
AV_CX      = CARD_X0 + INNER_PAD + AVATAR_D // 2
TEXT_X     = AV_CX + AVATAR_D // 2 + GAP_AV_TX
QR_X       = CARD_X1 - INNER_PAD - QR_SIZE   # 二维码左边 x
TEXT_MAX_W = QR_X - GAP_TX_QR - TEXT_X        # 文字区可用宽度


# ─────────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────────

def generate_footer_card(output_path: str):
    # 字体
    f_name  = load_font(50)
    f_tag   = load_font(28)
    f_body  = load_font(26)
    f_bold  = load_font(28)
    f_id    = load_font(30)
    f_small = load_font(24)

    # 先在临时画布上量出文字区总高度，再定最终 H
    tmp = Image.new("RGB", (W, 800), C_WHITE)
    d   = ImageDraw.Draw(tmp)

    lines = [
        ("name",   "加宁慢慢来",                         f_name,  C_NAVY),
        ("sep",    None,                                 None,    None),
        ("tag1",   "建立人生OS，活得更幸福",               f_tag,   C_TEAL),
        ("tag2",   "用AI搭建人生系统，每周分享干货、实践与思考", f_body, C_TEAL),
        ("cta",    None,                                 None,    None),  # 混色行，单独处理
        ("id",     None,                                 None,    None),  # 混色行
        ("remark", "请备注城市和行业",                    f_small, C_TEAL),
    ]

    LINE_H = {
        "name":   60,
        "sep":    20,   # 分割线 + 间隙
        "tag1":   44,
        "tag2a":  36,   # 第一行：用AI搭建人生系统，每周
        "tag2b":  40,   # 第二行：分享干货、实践与思考
        "cta":    44,
        "id":     44,
        "remark": 36,
    }
    total_text_h = sum(LINE_H.values())

    # 卡片高度 = 头像 or 文字区（取较大者）+ 上下 padding
    content_h = max(AVATAR_D + 20, total_text_h)
    CARD_V_PAD = 52
    H = content_h + CARD_V_PAD * 2 + CARD_PAD * 2

    # 正式画布
    img  = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(img)

    CARD_Y0 = CARD_PAD
    CARD_Y1 = H - CARD_PAD

    # 卡片背景
    rounded_rect_fill(draw, CARD_X0, CARD_Y0, CARD_X1, CARD_Y1, r=36, fill=C_LBLUE)

    mid_y = (CARD_Y0 + CARD_Y1) // 2   # 垂直中心线

    # ── 头像 ──
    av_cy = mid_y
    av_paste_x = AV_CX - AVATAR_D // 2
    av_paste_y = av_cy - AVATAR_D // 2

    if AVATAR_PATH.exists():
        av = circle_crop(Image.open(AVATAR_PATH), AVATAR_D)
        # 白底
        wb = Image.new("RGBA", (AVATAR_D, AVATAR_D), C_WHITE + (255,))
        wm = Image.new("L", (AVATAR_D, AVATAR_D), 0)
        ImageDraw.Draw(wm).ellipse([0, 0, AVATAR_D, AVATAR_D], fill=255)
        img.paste(wb.convert("RGB"), (av_paste_x, av_paste_y), wm)
        # 头像
        img_rgba = img.convert("RGBA")
        img_rgba.paste(av, (av_paste_x, av_paste_y), av.split()[3])
        img = img_rgba.convert("RGB")
        draw = ImageDraw.Draw(img)
        # 圆边框
        bd = AVATAR_D + 14
        border_img = Image.new("RGBA", (bd, bd), (0, 0, 0, 0))
        ImageDraw.Draw(border_img).ellipse([0, 0, bd, bd], outline=C_BLUE + (255,), width=5)
        img_rgba2 = img.convert("RGBA")
        img_rgba2.paste(border_img, (av_paste_x - 7, av_paste_y - 7), border_img)
        img = img_rgba2.convert("RGB")
        draw = ImageDraw.Draw(img)
    else:
        draw.ellipse([av_paste_x, av_paste_y, av_paste_x+AVATAR_D, av_paste_y+AVATAR_D],
                     fill=C_BLUE)
        draw.text((AV_CX - 18, av_cy - 24), "宁", fill=C_NAVY, font=load_font(44))

    # ── 文字区（垂直居中于 mid_y） ──
    ty = mid_y - total_text_h // 2

    # 名字
    draw.text((TEXT_X, ty), "加宁慢慢来", fill=C_NAVY, font=f_name)
    ty += LINE_H["name"]

    # 分割线
    draw.rectangle([TEXT_X, ty, TEXT_X + 180, ty + 2], fill=C_BLUE)
    ty += LINE_H["sep"]

    # 建立人生OS
    draw.text((TEXT_X, ty), "建立人生OS，活得更幸福", fill=C_TEAL, font=f_tag)
    ty += LINE_H["tag1"]

    # 用AI搭建人生系统（两行）
    draw.text((TEXT_X, ty), "用AI搭建人生系统，每周分享", fill=C_TEAL, font=f_body)
    ty += LINE_H["tag2a"]
    draw.text((TEXT_X, ty), "干货、实践与思考", fill=C_TEAL, font=f_body)
    ty += LINE_H["tag2b"]

    # 想要加入「智愈+」（混色行）
    t1 = "想要加入 "
    t2 = "「智愈+」AI赋能个人成长社群"
    draw.text((TEXT_X, ty), t1, fill=C_TEXT, font=f_body)
    draw.text((TEXT_X + tw(draw, t1, f_body), ty), t2, fill=C_DPINK, font=f_bold)
    ty += LINE_H["cta"]

    # 微信请加（混色行）
    t3 = "微信请加："
    t4 = "jianingplux"
    draw.text((TEXT_X, ty), t3, fill=C_TEXT, font=f_body)
    draw.text((TEXT_X + tw(draw, t3, f_body), ty), t4, fill=C_NAVY, font=f_id)
    ty += LINE_H["id"]

    # 请备注
    draw.text((TEXT_X, ty), "请备注城市和行业", fill=C_TEAL, font=f_small)

    # ── 二维码 ──
    qr_y = mid_y - QR_SIZE // 2

    if QRCODE_PATH.exists():
        qr = Image.open(QRCODE_PATH).resize((QR_SIZE, QR_SIZE), Image.LANCZOS).convert("RGB")
        # 白底背景
        pad = 10
        qr_bg = Image.new("RGB", (QR_SIZE + pad*2, QR_SIZE + pad*2), C_WHITE)
        img.paste(qr_bg, (QR_X - pad, qr_y - pad))
        img.paste(qr, (QR_X, qr_y))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(
            [QR_X - pad, qr_y - pad, QR_X + QR_SIZE + pad, qr_y + QR_SIZE + pad],
            radius=12, outline=C_BLUE, width=3
        )
    else:
        draw.rectangle([QR_X, qr_y, QR_X + QR_SIZE, qr_y + QR_SIZE], fill=C_BLUE)
        draw.text((QR_X + 20, qr_y + 60), "二维码", fill=C_NAVY, font=f_body)

    # ── 保存 ──
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out), "PNG", optimize=True)
    print(f"✅ 底部卡片已生成：{out}")
    return str(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成加宁慢慢来底部品牌卡片")
    parser.add_argument("--output", "-o", default="/Users/jnx/Desktop/jianing-footer-card.png")
    args = parser.parse_args()
    generate_footer_card(args.output)
