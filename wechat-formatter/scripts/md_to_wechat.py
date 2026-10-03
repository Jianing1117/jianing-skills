#!/usr/bin/env python3
"""
md_to_wechat.py
将 Markdown 文章转换为「加宁慢慢来」品牌风格的微信公众号内联 HTML。

用法：
    python3 md_to_wechat.py --input article.md --output output.html
    python3 md_to_wechat.py --input article.md  # 输出到 stdout
    cat article.md | python3 md_to_wechat.py    # 从 stdin 读入
"""

import re
import sys
import argparse
from pathlib import Path

# ─────────────────────────────────────────────
# 品牌色板 v7.0
# ─────────────────────────────────────────────
C_NAVY   = "#171717"   # 近黑 · 正文、标题、strong
C_TEAL   = "#607EA5"   # 展陈蓝 · 英文标签、有序列表数字
C_BLUE   = "#B8D9EA"   # 天蓝 · 列表圆点、分隔短线
C_LBLUE  = "#EBF4F9"   # 天蓝白 · TIP 提示框底色
C_CODE   = "#F5F4F0"   # 雾白 · 代码块底色
C_BORDER = "#D5D5D2"   # 陈列灰 · 代码块边框
C_TEXT   = "#171717"   # 近黑 · 正文文字
C_PINK   = "#E7C4C8"   # 樱粉
C_DPINK  = "#D9A8B2"   # 玫瑰粉
C_GREY   = "#A9AAAB"   # 中灰 · END 灰字

# ─────────────────────────────────────────────
# Emoji → 品牌色 HTML 图标映射
# ─────────────────────────────────────────────
EMOJI_LINE_RE = re.compile(
    r'^[\s]*([\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
    r'\U0001F900-\U0001F9FF\U00002600-\U000027BF\U00002700-\U000027BF'
    r'\U0000FE00-\U0000FE0F\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF'
    r'\U00002702-\U000027B0\U00002600-\U000026FF'
    r'✅❌⭐⚠ℹ❤✨✔✖'
    r'\U0001F534\U0001F7E1\U0001F7E2\U0001F7E0\U0001F535\U0001F7E3'
    r'\U0001F4CC\U0001F4A1\U0001F4E2]+)\s*(.*)'
)

EMOJI_ICON_MAP = {
    '✅': f'<span style="display:inline-block;width:16px;height:16px;background:{C_BLUE};border-radius:50%;text-align:center;line-height:16px;font-size:10px;color:#FFFFFF;margin-right:8px;vertical-align:middle;">✓</span>',
    '❌': f'<span style="display:inline-block;width:16px;height:16px;background:{C_BLUE};border-radius:50%;text-align:center;line-height:16px;font-size:10px;color:#FFFFFF;margin-right:8px;vertical-align:middle;">✗</span>',
    '⭐': f'<span style="color:{C_BLUE};margin-right:6px;vertical-align:middle;">★</span>',
}

def _replace_leading_emoji(emoji: str, text: str) -> str:
    icon = EMOJI_ICON_MAP.get(emoji)
    if not icon:
        icon = f'<span style="display:inline-block;width:8px;height:8px;background:{C_BLUE};border-radius:50%;margin-right:8px;vertical-align:middle;"></span>'
    return icon + text

# ─────────────────────────────────────────────
# 底部（固定模板）
# ─────────────────────────────────────────────
FOOTER_HTML = f"""
<!-- END 结尾 -->
<section style="margin-top:72px;text-align:center;">
  <p style="font-size:11px;color:{C_GREY};margin:0 0 16px;letter-spacing:5px;">— END —</p>
  <p style="font-size:15px;color:{C_NAVY};margin:0;line-height:1.8;letter-spacing:0.3px;">欢迎大家关注我的公众号 👇</p>
</section>

<!-- 底部品牌卡片：请手动插入图片 -->
<section style="margin:20px 0 0;padding:20px;background:{C_LBLUE};border-radius:12px;text-align:center;">
  <p style="font-size:11px;color:{C_TEAL};letter-spacing:3px;margin:0;line-height:1.8;">📌 此处请插入底部品牌卡片图片</p>
</section>
"""


# ─────────────────────────────────────────────
# 列表紧凑判断
# ─────────────────────────────────────────────
def _is_compact_list(items: list) -> bool:
    if not items:
        return False
    _strip_md = re.compile(r'\*{1,2}|`[^`]*`|\[[^\]]*\]\([^)]*\)')
    single_line_count = sum(
        1 for t in items if len(_strip_md.sub('', t)) <= 60
    )
    return single_line_count / len(items) >= 0.8


# ─────────────────────────────────────────────
# 内联样式渲染器
# ─────────────────────────────────────────────
class WechatRenderer:
    def __init__(self):
        self.h2_counter = 0

    def render_inline(self, text: str) -> str:
        text = re.sub(
            r'`([^`]+)`',
            lambda m: f'<code style="font-size:14px;color:{C_NAVY};background:{C_LBLUE};padding:1px 5px;border-radius:3px;font-family:\'Courier New\',Menlo,monospace;">{m.group(1)}</code>',
            text
        )
        text = re.sub(
            r'\*\*(.+?)\*\*',
            lambda m: f'<strong style="color:{C_NAVY};font-weight:bold;">{m.group(1)}</strong>',
            text
        )
        text = re.sub(
            r'\*(.+?)\*',
            lambda m: f'<em style="color:{C_TEAL};">{m.group(1)}</em>',
            text
        )
        text = re.sub(
            r'\[(.+?)\]\((.+?)\)',
            lambda m: f'<span style="color:{C_NAVY};font-weight:bold;">{m.group(1)}</span>'
                      f'<span style="font-size:12px;color:{C_TEAL};">（链接：{m.group(2)}）</span>',
            text
        )
        return text

    def h2(self, text: str) -> str:
        """CHAPTER 01 英文标签 + 中文标题"""
        self.h2_counter += 1
        num = str(self.h2_counter).zfill(2)
        return (
            f'<section style="margin:72px 0 48px;">\n'
            f'  <p style="font-size:11px;color:{C_TEAL};letter-spacing:4px;margin:0 0 6px;font-weight:500;">CHAPTER {num}</p>\n'
            f'  <p style="font-size:22px;font-weight:bold;color:{C_NAVY};line-height:1.5;margin:0;letter-spacing:0.5px;">{self.render_inline(text)}</p>\n'
            f'</section>\n'
        )

    def h3(self, text: str) -> str:
        return (
            f'<p style="font-size:17px;font-weight:600;color:{C_NAVY};line-height:1.5;margin:48px 0 12px;letter-spacing:0.3px;">{self.render_inline(text)}</p>\n'
            f'<div style="width:32px;height:3px;background:{C_BLUE};border-radius:2px;margin:0 0 20px;"></div>\n'
        )

    def h4(self, text: str) -> str:
        return (
            f'<p style="font-size:17px;font-weight:600;color:{C_NAVY};line-height:1.5;margin:48px 0 12px;letter-spacing:0.3px;">{self.render_inline(text)}</p>\n'
            f'<div style="width:32px;height:3px;background:{C_BLUE};border-radius:2px;margin:0 0 20px;"></div>\n'
        )

    def paragraph(self, text: str) -> str:
        return (
            f'<p style="font-size:16px;color:{C_TEXT};line-height:1.9;margin:0 0 28px;letter-spacing:0.5px;">'
            f'{self.render_inline(text)}</p>\n'
        )

    def compact_list(self, items: list) -> str:
        inner = ''
        for emoji, text in items:
            icon_html = _replace_leading_emoji(emoji, self.render_inline(text))
            inner += (
                f'  <p style="font-size:16px;color:{C_TEXT};line-height:2.2;margin:0;letter-spacing:0.5px;">'
                f'{icon_html}</p>\n'
            )
        return (
            f'<section style="margin:0 0 28px;">\n'
            f'{inner}'
            f'</section>\n'
        )

    def ul_list(self, items: list) -> str:
        compact = _is_compact_list(items)
        parts = []
        for text in items:
            inline = self.render_inline(text)
            dot = f'<span style="display:inline-block;width:6px;height:6px;background:{C_BLUE};border-radius:50%;margin-right:10px;vertical-align:middle;"></span>'
            if compact:
                parts.append(
                    f'<p style="font-size:16px;color:{C_TEXT};line-height:2.2;margin:0;letter-spacing:0.5px;">'
                    f'{dot}{inline}</p>\n'
                )
            else:
                parts.append(
                    f'<p style="font-size:16px;color:{C_TEXT};line-height:1.9;margin:0 0 28px;letter-spacing:0.5px;">'
                    f'{dot}{inline}</p>\n'
                )
        if compact:
            return f'<section style="margin:0 0 28px;">\n{"".join(parts)}</section>\n'
        return ''.join(parts)

    def ol_list(self, items: list) -> str:
        compact = _is_compact_list(items)
        parts = []
        for idx, text in enumerate(items, 1):
            inline = self.render_inline(text)
            num = f'<span style="color:{C_TEAL};font-weight:600;margin-right:6px;">{idx}.</span>'
            if compact:
                parts.append(
                    f'<p style="font-size:16px;color:{C_TEXT};line-height:2.2;margin:0;letter-spacing:0.5px;">'
                    f'{num}{inline}</p>\n'
                )
            else:
                parts.append(
                    f'<p style="font-size:16px;color:{C_TEXT};line-height:1.9;margin:0 0 28px;letter-spacing:0.5px;">'
                    f'{num}{inline}</p>\n'
                )
        if compact:
            return f'<section style="margin:0 0 28px;">\n{"".join(parts)}</section>\n'
        return ''.join(parts)

    def blockquote(self, lines: list) -> str:
        """TIP 提示框：浅底色面 + TIP 标签，无边框"""
        non_empty = [l for l in lines if l.strip()]
        if not non_empty:
            return ''
        parts = []
        for idx, l in enumerate(non_empty):
            is_last = (idx == len(non_empty) - 1)
            margin = 'margin:0;' if is_last else 'margin:0 0 10px;'
            parts.append(
                f'<p style="font-size:15px;color:{C_TEXT};line-height:1.8;{margin}">'
                f'{self.render_inline(l)}</p>\n'
            )
        return (
            f'<section style="margin:28px 0;padding:20px 24px;background:{C_LBLUE};border-radius:8px;">\n'
            f'  <p style="font-size:11px;color:{C_TEAL};letter-spacing:3px;margin:0 0 8px;font-weight:600;">TIP</p>\n'
            f'{"".join(parts)}'
            f'</section>\n'
        )

    def code_block(self, code: str, lang: str = '') -> str:
        escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return (
            f'<section style="margin:18px 0;padding:16px 20px;background:{C_CODE};border:1px solid {C_BORDER};border-radius:6px;">\n'
            f'  <code style="font-size:13px;color:{C_NAVY};font-family:\'Courier New\',Menlo,monospace;white-space:pre-wrap;display:block;line-height:1.7;">{escaped}</code>\n'
            f'</section>\n'
        )

    def hr(self) -> str:
        return f'<div style="width:100%;height:1px;background:{C_BORDER};margin:28px 0;"></div>\n'

    def image(self, alt: str, src: str) -> str:
        label = alt if alt else src
        return (
            f'<section style="margin:28px 0;padding:20px 24px;background:{C_LBLUE};border-radius:8px;">\n'
            f'  <p style="font-size:11px;color:{C_TEAL};letter-spacing:3px;margin:0 0 8px;font-weight:600;">IMAGE</p>\n'
            f'  <p style="font-size:14px;color:{C_TEAL};line-height:1.8;margin:0;">{label}（请手动上传图片）</p>\n'
            f'</section>\n'
        )

    def table(self, header: list, rows: list) -> str:
        th_cells = ''.join(
            f'<th style="padding:10px 14px;text-align:left;font-weight:600;border-bottom:2px solid {C_NAVY};white-space:nowrap;">{self.render_inline(h)}</th>'
            for h in header
        )
        tr_rows = ''
        for row in rows:
            cells = ''.join(
                f'<td style="padding:10px 14px;line-height:1.6;white-space:nowrap;">{self.render_inline(c)}</td>'
                for c in row
            )
            tr_rows += f'<tr>{cells}</tr>\n'
        return (
            f'<section style="margin:28px 0;overflow-x:auto;-webkit-overflow-scrolling:touch;">\n'
            f'  <table style="border-collapse:collapse;font-size:14px;color:{C_TEXT};min-width:100%;">\n'
            f'    <thead><tr>{th_cells}</tr></thead>\n'
            f'    <tbody>\n{tr_rows}    </tbody>\n'
            f'  </table>\n'
            f'</section>\n'
        )


# ─────────────────────────────────────────────
# Markdown 解析器（轻量、无外部依赖）
# ─────────────────────────────────────────────
class MarkdownParser:
    def __init__(self):
        self.r = WechatRenderer()

    def parse(self, md: str) -> str:
        lines = md.splitlines()
        html_parts = []
        first_h1_skipped = False

        # ── 跳过 Obsidian YAML frontmatter ──
        i = 0
        if lines and lines[0].strip() == '---':
            i = 1
            while i < len(lines) and lines[i].strip() != '---':
                i += 1
            i += 1

        while i < len(lines):
            line = lines[i]

            # ── 代码块 ──
            if line.startswith('```'):
                lang = line[3:].strip()
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                html_parts.append(self.r.code_block('\n'.join(code_lines), lang))
                i += 1
                continue

            # ── 引用块 ──
            if line.startswith('>'):
                block = []
                while i < len(lines) and lines[i].startswith('>'):
                    block.append(lines[i][1:].strip())
                    i += 1
                html_parts.append(self.r.blockquote(block))
                continue

            # ── 分割线 ──
            if re.match(r'^[-*_]{3,}\s*$', line):
                html_parts.append(self.r.hr())
                i += 1
                continue

            # ── 表格 ──
            if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?[\s\-:|]+\|', lines[i+1]):
                header = [c.strip() for c in line.strip().strip('|').split('|')]
                i += 2
                rows = []
                while i < len(lines) and '|' in lines[i]:
                    rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                    i += 1
                html_parts.append(self.r.table(header, rows))
                continue

            # ── 标题 ──
            m = re.match(r'^(#{1,4})\s+(.*)', line)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                if level == 1:
                    if not first_h1_skipped:
                        first_h1_skipped = True
                        i += 1
                        continue
                    else:
                        html_parts.append(self.r.h2(text))
                elif level == 2:
                    html_parts.append(self.r.h2(text))
                elif level == 3:
                    html_parts.append(self.r.h3(text))
                else:
                    html_parts.append(self.r.h4(text))
                i += 1
                continue

            # ── 无序列表 ──
            if re.match(r'^[-*+]\s+', line):
                items = []
                while i < len(lines) and re.match(r'^[-*+]\s+', lines[i]):
                    items.append(re.sub(r'^[-*+]\s+', '', lines[i]))
                    i += 1
                html_parts.append(self.r.ul_list(items))
                continue

            # ── 有序列表 ──
            if re.match(r'^\d+\.\s+', line):
                items = []
                while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                    items.append(re.sub(r'^\d+\.\s+', '', lines[i]))
                    i += 1
                html_parts.append(self.r.ol_list(items))
                continue

            # ── 图片 ──
            m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', line)
            if m:
                html_parts.append(self.r.image(m.group(1), m.group(2)))
                i += 1
                continue

            # ── 空行 ──
            if line.strip() == '':
                i += 1
                continue

            # ── Emoji 紧凑列表 ──
            em = EMOJI_LINE_RE.match(line.strip())
            if em:
                items = []
                while i < len(lines):
                    stripped = lines[i].strip()
                    if stripped == '':
                        break
                    m_emoji = EMOJI_LINE_RE.match(stripped)
                    if m_emoji:
                        items.append((m_emoji.group(1), m_emoji.group(2)))
                        i += 1
                    else:
                        break
                if items:
                    html_parts.append(self.r.compact_list(items))
                    continue

            # ── 普通段落 ──
            html_parts.append(self.r.paragraph(line.strip()))
            i += 1

        return ''.join(html_parts)


# ─────────────────────────────────────────────
# 完整 HTML 包装
# ─────────────────────────────────────────────
def wrap_html(content: str, title: str = '微信排版预览') -> str:
    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>微信排版预览 - {title}</title>
<style>
  body {{ background: #f0f0f0; padding: 40px 20px; }}
  .tip {{ text-align:center; font-family:sans-serif; font-size:13px; color:#888; margin-bottom:20px; }}
</style>
</head>
<body>
<p class="tip">点进白色内容区域 → 全选（Cmd+A）→ 复制（Cmd+C）→ 粘贴到微信编辑器</p>

<section style="max-width:680px;margin:0 auto;padding:40px 44px;font-family:'PingFang SC','Noto Sans SC',-apple-system,sans-serif;color:{C_TEXT};background:#FFFFFF;border-radius:4px;">

{content}
{FOOTER_HTML}
</section>
</body>
</html>
"""


# ─────────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Markdown → 微信公众号 HTML 转换器')
    parser.add_argument('--input', '-i', type=str, help='输入 Markdown 文件路径')
    parser.add_argument('--output', '-o', type=str, help='输出 HTML 文件路径（不指定则输出到 stdout）')
    args = parser.parse_args()

    if args.input:
        md_text = Path(args.input).read_text(encoding='utf-8')
        title = Path(args.input).stem
    else:
        md_text = sys.stdin.read()
        title = '微信排版预览'

    p = MarkdownParser()
    body = p.parse(md_text)
    html = wrap_html(body, title)

    if args.output:
        Path(args.output).write_text(html, encoding='utf-8')
        print(f'✅ 已生成：{args.output}')
    else:
        print(html)


if __name__ == '__main__':
    main()
