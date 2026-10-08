#!/usr/bin/env python3
"""
generate_footer_card.py
输出「加宁慢慢来」公众号文末品牌卡片（2026-10-08 定稿，2160 × 1720）。

卡片是固定的成品图 templates/footer-card.png，不再按头像、二维码现场生成。
要改卡片，改 brand kit 里的 05-templates/wechat/footer-card.html，导出后替换这张图。

用法：
    python3 generate_footer_card.py --output ./outputs/footer-card.png
"""

import argparse
import shutil
from pathlib import Path

CARD = Path(__file__).resolve().parent.parent / "templates" / "footer-card.png"


def main():
    ap = argparse.ArgumentParser(description="输出加宁慢慢来公众号文末品牌卡片")
    ap.add_argument("--output", default="footer-card.png")
    a = ap.parse_args()
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CARD, out)
    print(f"✅ 底部卡片已输出：{out}")


if __name__ == "__main__":
    main()
