#!/usr/bin/env python3
"""Generate an editable Excalidraw cover for Xiaohongshu or Douyin."""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path


PLATFORMS = {
    "xiaohongshu": (900, 1200, "小红书"),
    "douyin": (1080, 1920, "抖音"),
    "square": (1080, 1080, "通用"),
}

INK = "#1E2A30"
MUTED = "#506570"
BLUE = "#DDE7ED"
BLUE_DARK = "#3D6A82"
GREEN = "#E2EDDF"
GREEN_DARK = "#3A6B42"
ROSE = "#F2E8E6"
ROSE_DARK = "#8F3F3A"
WHITE = "#FFFFFF"


def element_id() -> str:
    return uuid.uuid4().hex[:16]


def base_element(kind: str, x: float, y: float, width: float, height: float) -> dict:
    return {
        "id": element_id(),
        "type": kind,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "fillStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "index": None,
        "roundness": None,
        "seed": 1,
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
    }


def rect(x: float, y: float, width: float, height: float, fill: str, radius: int = 24) -> dict:
    item = base_element("rectangle", x, y, width, height)
    item.update(
        {
            "strokeColor": fill,
            "backgroundColor": fill,
            "roundness": {"type": 3, "value": radius},
        }
    )
    return item


def text(
    x: float,
    y: float,
    value: str,
    size: int,
    color: str,
    width: float,
    *,
    align: str = "left",
    line_height: float = 1.25,
) -> dict:
    lines = value.count("\n") + 1
    height = max(size * line_height * lines, size * 1.25)
    item = base_element("text", x, y, width, height)
    item.update(
        {
            "strokeColor": color,
            "backgroundColor": "transparent",
            "text": value,
            "fontSize": size,
            "fontFamily": 1,
            "textAlign": align,
            "verticalAlign": "top",
            "containerId": None,
            "originalText": value,
            "autoResize": False,
            "lineHeight": line_height,
        }
    )
    return item


def visual_width(value: str) -> float:
    return sum(1.0 if "\u4e00" <= char <= "\u9fff" else 0.55 for char in value)


def wrap_text(value: str, max_units: float) -> str:
    lines: list[str] = []
    current = ""
    current_width = 0.0
    for char in value.strip():
        char_width = 1.0 if "\u4e00" <= char <= "\u9fff" else 0.55
        if current and current_width + char_width > max_units:
            lines.append(current.rstrip())
            current = ""
            current_width = 0.0
        current += char
        current_width += char_width
    if current:
        lines.append(current.rstrip())
    return "\n".join(lines)


def build_cover(
    title: str,
    subtitle: str | None,
    bullets: list[str],
    platform: str,
    author: str | None,
) -> dict:
    canvas_width, canvas_height, platform_label = PLATFORMS[platform]
    margin = int(canvas_width * 0.085)
    content_width = canvas_width - margin * 2
    tall = canvas_height / canvas_width > 1.4
    title_size = 76 if canvas_width >= 1000 else 64
    title_units = 10.5 if tall else 12.5
    title_value = wrap_text(title, title_units)
    title_lines = title_value.count("\n") + 1

    elements: list[dict] = []
    elements.append(rect(margin, margin, 150, 48, BLUE, 24))
    elements.append(text(margin, margin + 8, platform_label, 24, BLUE_DARK, 150, align="center"))

    y = margin + (170 if tall else 145)
    elements.append(text(margin, y, title_value, title_size, INK, content_width, line_height=1.18))
    y += title_lines * title_size * 1.18 + 36

    elements.append(rect(margin, y, min(210, content_width * 0.28), 10, BLUE_DARK, 5))
    y += 52

    if subtitle:
        subtitle_value = wrap_text(subtitle, 24 if tall else 30)
        elements.append(text(margin, y, subtitle_value, 34, MUTED, content_width, line_height=1.35))
        y += (subtitle_value.count("\n") + 1) * 46 + 42

    card_colors = [(BLUE, BLUE_DARK), (GREEN, GREEN_DARK), (ROSE, ROSE_DARK)]
    available_height = canvas_height - y - margin - (80 if author else 25)
    card_gap = 24
    card_count = min(len(bullets), 3)
    card_height = min(170 if tall else 145, (available_height - card_gap * max(card_count - 1, 0)) / max(card_count, 1))

    for index, bullet in enumerate(bullets[:3], start=1):
        fill, color = card_colors[index - 1]
        bullet_value = wrap_text(bullet, 25 if tall else 30)
        elements.append(rect(margin, y, content_width, card_height, fill, 26))
        elements.append(text(margin + 28, y + 27, f"{index:02d}", 24, color, 62))
        elements.append(text(margin + 102, y + 24, bullet_value, 30, INK, content_width - 132, line_height=1.3))
        y += card_height + card_gap

    if author:
        author_value = author.strip()
        author_width = min(content_width, max(180, visual_width(author_value) * 24))
        elements.append(
            text(
                canvas_width - margin - author_width,
                canvas_height - margin - 38,
                author_value,
                22,
                MUTED,
                author_width,
                align="right",
            )
        )

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": WHITE,
            "gridSize": None,
            "scrollX": 0,
            "scrollY": 0,
            "zoom": {"value": 0.75},
        },
        "files": {},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Cover title")
    parser.add_argument("--subtitle", help="Optional subtitle")
    parser.add_argument("--bullet", action="append", default=[], help="Optional bullet; repeat up to three times")
    parser.add_argument("--platform", choices=PLATFORMS, default="xiaohongshu")
    parser.add_argument("--author", help="Optional signature or brand")
    parser.add_argument("--output", type=Path, default=Path.cwd() / "cover.excalidraw")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.title.strip():
        raise SystemExit("--title cannot be empty")
    if len(args.bullet) > 3:
        raise SystemExit("Use no more than three --bullet values")
    if args.output.suffix.lower() != ".excalidraw":
        raise SystemExit("--output must end with .excalidraw")

    document = build_cover(
        title=args.title.strip(),
        subtitle=args.subtitle.strip() if args.subtitle else None,
        bullets=[item.strip() for item in args.bullet if item.strip()],
        platform=args.platform,
        author=args.author.strip() if args.author else None,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
