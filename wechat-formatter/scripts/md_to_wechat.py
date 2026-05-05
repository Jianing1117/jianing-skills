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
# 品牌色板
# ─────────────────────────────────────────────
C_NAVY   = "#2F4156"   # 正文、标题、strong
C_TEAL   = "#567C8D"   # 副标题、次级文字
C_BLUE   = "#C8D9E6"   # 雾霾蓝（主视觉色）
C_LBLUE  = "#EAF3F8"   # 浅雾蓝（引用/提示框底色）
C_CODE   = "#F5F8FB"   # 代码块底色
C_BORDER = "#DDE8EF"   # 边框灰蓝
C_TEXT   = "#333333"   # 正文文字
C_PINK   = "#E8CECA"   # 雾粉
C_DPINK  = "#B07A72"   # 深粉
C_GREY   = "#BBBBBB"   # END 灰字
C_ALTROW = "#F9FBFC"   # 表格奇偶交替行

# ─────────────────────────────────────────────
# Emoji → 品牌色 HTML 图标映射
# ─────────────────────────────────────────────
# 检测行首 emoji 的正则（常见图标类 emoji）
EMOJI_LINE_RE = re.compile(
    r'^[\s]*([\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
    r'\U0001F900-\U0001F9FF\U00002600-\U000027BF\U00002700-\U000027BF'
    r'\U0000FE00-\U0000FE0F\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF'
    r'\U00002702-\U000027B0\U00002600-\U000026FF'
    r'\u2705\u274C\u2B50\u26A0\u2139\u2764\u2728\u2714\u2716'
    r'\U0001F534\U0001F7E1\U0001F7E2\U0001F7E0\U0001F535\U0001F7E3'
    r'\U0001F4CC\U0001F4A1\U0001F4E2]+)\s*(.*)'
)

# 品牌色 HTML 图标替换表（emoji → inline HTML）
EMOJI_ICON_MAP = {
    '✅': f'<span style="display:inline-block;width:16px;height:16px;background:{C_BLUE};border-radius:50%;text-align:center;line-height:16px;font-size:10px;color:#FFFFFF;margin-right:8px;vertical-align:middle;">✓</span>',
    '❌': f'<span style="display:inline-block;width:16px;height:16px;background:{C_BLUE};border-radius:50%;text-align:center;line-height:16px;font-size:10px;color:#FFFFFF;margin-right:8px;vertical-align:middle;">✗</span>',
    '⭐': f'<span style="color:{C_BLUE};margin-right:6px;vertical-align:middle;">★</span>',
}

def _replace_leading_emoji(emoji: str, text: str) -> str:
    """将行首 emoji 替换为品牌色图标，未映射的 emoji 用通用蓝色圆点替代"""
    icon = EMOJI_ICON_MAP.get(emoji)
    if not icon:
        # 通用品牌色圆点替代
        icon = f'<span style="display:inline-block;width:8px;height:8px;background:{C_BLUE};border-radius:50%;margin-right:8px;vertical-align:middle;"></span>'
    return icon + text

# ─────────────────────────────────────────────
# 底部品牌卡片（固定模板）
# ─────────────────────────────────────────────
FOOTER_HTML = f"""
<!-- END 结尾 -->
<section style="margin-top:64px;text-align:center;">
  <p style="font-size:11px;color:{C_GREY};margin:0 0 16px;letter-spacing:5px;">— END —</p>
  <p style="font-size:15px;color:{C_NAVY};margin:0;line-height:1.8;letter-spacing:0.3px;">欢迎大家关注我的公众号 👇</p>
</section>

<!-- 底部品牌卡片：请手动插入图片 jianing-footer-card.png -->
<section style="margin:20px 0 0;padding:20px;background:{C_LBLUE};border-radius:12px;text-align:center;">
  <p style="font-size:13px;color:{C_TEAL};margin:0;line-height:1.8;">📌 此处请插入底部品牌卡片图片<br><span style="font-size:12px;color:#BBBBBB;">文件：Desktop/jianing-footer-card.png</span></p>
</section>
"""


# ─────────────────────────────────────────────
# 列表紧凑判断：超过 80% 的项为"单行"则视为紧凑列表
# 单行定义：去除 Markdown 标记后，纯文本字符数 ≤ 60
# ─────────────────────────────────────────────
def _is_compact_list(items: list) -> bool:
    """判断一组列表项是否应使用紧凑行距（超过 80% 的项为单行内容）"""
    if not items:
        return False
    # 去除 Markdown 加粗/斜体/链接/代码标记后估算纯文本长度
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
        """处理行内标记：加粗、行内代码、链接"""
        # 行内代码
        text = re.sub(
            r'`([^`]+)`',
            lambda m: f'<code style="font-size:14px;color:{C_NAVY};background:{C_LBLUE};padding:1px 5px;border-radius:3px;font-family:\'Courier New\',Menlo,monospace;">{m.group(1)}</code>',
            text
        )
        # 加粗
        text = re.sub(
            r'\*\*(.+?)\*\*',
            lambda m: f'<strong style="color:{C_NAVY};font-weight:bold;">{m.group(1)}</strong>',
            text
        )
        # 斜体
        text = re.sub(
            r'\*(.+?)\*',
            lambda m: f'<em style="color:{C_TEAL};">{m.group(1)}</em>',
            text
        )
        # 链接 → 文字 + 括号注释
        text = re.sub(
            r'\[(.+?)\]\((.+?)\)',
            lambda m: f'<span style="color:{C_NAVY};font-weight:bold;">{m.group(1)}</span>'
                      f'<span style="font-size:12px;color:{C_TEAL};">（链接：{m.group(2)}）</span>',
            text
        )
        return text

    def h2(self, text: str) -> str:
        """
        章节标题（H2）样式：编号 + 横线 + 标题文字
        
        横线实现方案说明（微信兼容）：
        - ❌ border-top: 微信后台会过滤掉，不显示
        - ❌ div + background: 微信可能过滤 div 样式
        - ✅ hr + background: 微信支持，且语义正确
        - ⚠️  文字下划线(━━━): 字符方式，线会断开，不美观
        
        间距设计：
        - 数字(01) 下边距 16px → 横线
        - 横线 上下间距 16px → 文字
        """
        self.h2_counter += 1
        num = str(self.h2_counter).zfill(2)
        return (
            f'<section style="margin:80px 0 56px;text-align:center;">\n'
            f'  <p style="font-size:26px;font-weight:bold;color:{C_NAVY};line-height:1;margin:0 0 16px;letter-spacing:2px;">{num}</p>\n'
            f'  <hr style="width:60px;height:2px;background:{C_TEAL};border:none;margin:16px auto;">\n'
            f'  <p style="font-size:18px;font-weight:bold;color:{C_NAVY};line-height:1.6;margin:0;letter-spacing:0.5px;">{self.render_inline(text)}</p>\n'
            f'</section>\n'
        )

    def h3(self, text: str) -> str:
        return (
            f'<section style="margin:48px 0 16px;">\n'
            f'  <p style="font-size:19px;font-weight:bold;color:{C_NAVY};line-height:1.5;margin:0 0 8px;letter-spacing:0.3px;">{self.render_inline(text)}</p>\n'
            f'  <div style="width:40px;height:4px;background:{C_BLUE};border-radius:2px;"></div>\n'
            f'</section>\n'
        )

    def h4(self, text: str) -> str:
        return (
            f'<p style="font-size:17px;font-weight:bold;color:{C_NAVY};line-height:1.6;'
            f'margin:32px 0 10px;padding-left:12px;'
            f'border-left:4px solid {C_TEAL};letter-spacing:0.3px;">'
            f'{self.render_inline(text)}</p>\n'
        )

    def paragraph(self, text: str) -> str:
        return (
            f'<p style="font-size:16px;color:{C_TEXT};line-height:1.9;margin:0 0 32px;letter-spacing:0.5px;">'
            f'{self.render_inline(text)}</p>\n'
        )

    def compact_list(self, items: list) -> str:
        """渲染 emoji 开头的连续短行为紧凑列表（行间距代替段落间距）"""
        inner = ''
        for emoji, text in items:
            icon_html = _replace_leading_emoji(emoji, self.render_inline(text))
            inner += (
                f'  <p style="font-size:16px;color:{C_TEXT};line-height:2.2;margin:0;letter-spacing:0.5px;">'
                f'{icon_html}</p>\n'
            )
        return (
            f'<section style="margin:0 0 32px;">\n'
            f'{inner}'
            f'</section>\n'
        )

    def ul_list(self, items: list) -> str:
        """渲染无序列表组。超过 80% 为单行时用紧凑行距，否则用段落间距。"""
        compact = _is_compact_list(items)
        parts = []
        for text in items:
            inline = self.render_inline(text)
            if compact:
                parts.append(
                    f'<p style="font-size:16px;color:{C_TEXT};line-height:2.2;margin:0;letter-spacing:0.5px;">'
                    f'<span style="color:{C_NAVY};font-weight:bold;margin-right:6px;">·</span>'
                    f'{inline}</p>\n'
                )
            else:
                parts.append(
                    f'<p style="font-size:16px;color:{C_TEXT};line-height:1.9;margin:0 0 32px;letter-spacing:0.5px;">'
                    f'<span style="color:{C_NAVY};font-weight:bold;margin-right:6px;">·</span>'
                    f'{inline}</p>\n'
                )
        if compact:
            return f'<section style="margin:0 0 32px;">\n{"".join(parts)}</section>\n'
        return ''.join(parts)

    def ol_list(self, items: list) -> str:
        """渲染有序列表组。超过 80% 为单行时用紧凑行距，否则用段落间距。"""
        compact = _is_compact_list(items)
        parts = []
        for idx, text in enumerate(items, 1):
            inline = self.render_inline(text)
            if compact:
                parts.append(
                    f'<p style="font-size:16px;color:{C_TEXT};line-height:2.2;margin:0;letter-spacing:0.5px;">'
                    f'<span style="color:{C_NAVY};font-weight:bold;margin-right:4px;">{idx}.</span>'
                    f'{inline}</p>\n'
                )
            else:
                parts.append(
                    f'<p style="font-size:16px;color:{C_TEXT};line-height:1.9;margin:0 0 32px;letter-spacing:0.5px;">'
                    f'<span style="color:{C_NAVY};font-weight:bold;margin-right:4px;">{idx}.</span>'
                    f'{inline}</p>\n'
                )
        if compact:
            return f'<section style="margin:0 0 32px;">\n{"".join(parts)}</section>\n'
        return ''.join(parts)

    def blockquote(self, lines: list) -> str:
        # 过滤掉空行
        non_empty = [l for l in lines if l.strip()]
        if not non_empty:
            return ''

        # 判断第一行是否是独立标题行：
        # 条件：整个 blockquote 超过 1 行非空内容，且第一行去除 Markdown 标记后纯文本 ≤ 50 字
        _strip_md = re.compile(r'\*{1,2}|`[^`]*`|\[[^\]]*\]\([^)]*\)|⚙️|💡')
        first_clean = _strip_md.sub('', non_empty[0]).strip()
        is_title_line = len(non_empty) > 1 and len(first_clean) <= 50 and first_clean != ''

        parts = []
        for idx, l in enumerate(non_empty):
            is_last = (idx == len(non_empty) - 1)
            margin = 'margin:0;' if is_last else 'margin:0 0 10px;'
            if idx == 0 and is_title_line:
                # 标题行：17px + 加粗 + Navy + 小齿轮图标前缀
                icon = f'<span style="display:inline-block;width:14px;height:14px;background:{C_NAVY};border-radius:3px;margin-right:7px;vertical-align:middle;"></span>'
                parts.append(
                    f'<p style="font-size:17px;font-weight:bold;color:{C_NAVY};line-height:1.6;margin:0 0 12px;letter-spacing:0.3px;">'
                    f'{icon}{self.render_inline(l)}</p>\n'
                )
            else:
                parts.append(
                    f'<p style="font-size:15px;color:{C_TEXT};line-height:1.8;{margin}">'
                    f'{self.render_inline(l)}</p>\n'
                )
        return (
            f'<section style="margin:24px 0;padding:16px 20px;background:{C_LBLUE};border-left:4px solid {C_BLUE};border-radius:0 8px 8px 0;">\n'
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
        return f'<div style="width:100%;height:1px;background:{C_BORDER};margin:32px 0;"></div>\n'

    def image(self, alt: str, src: str) -> str:
        label = alt if alt else src
        return (
            f'<section style="margin:24px 0;padding:14px 18px;background:{C_LBLUE};border-left:4px solid {C_BLUE};border-radius:0 8px 8px 0;">\n'
            f'  <p style="font-size:14px;color:{C_TEAL};line-height:1.8;margin:0;">📷 图片：{label}（请手动上传图片）</p>\n'
            f'</section>\n'
        )

    def table(self, header: list, rows: list) -> str:
        th_cells = ''.join(
            f'<th style="background:{C_BLUE};color:{C_NAVY};padding:10px 14px;text-align:left;font-weight:bold;border:1px solid {C_BORDER};white-space:nowrap;">{self.render_inline(h)}</th>'
            for h in header
        )
        tr_rows = ''
        for i, row in enumerate(rows):
            bg = '#FFFFFF' if i % 2 == 0 else C_ALTROW
            cells = ''.join(
                f'<td style="padding:10px 14px;border:1px solid {C_BORDER};background:{bg};line-height:1.6;white-space:nowrap;">{self.render_inline(c)}</td>'
                for c in row
            )
            tr_rows += f'<tr>{cells}</tr>\n'
        return (
            f'<section style="margin:22px 0;overflow-x:auto;-webkit-overflow-scrolling:touch;">\n'
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

        # ── 跳过 Obsidian YAML frontmatter（--- 包裹的头部）──
        i = 0
        if lines and lines[0].strip() == '---':
            i = 1
            while i < len(lines) and lines[i].strip() != '---':
                i += 1
            i += 1  # 跳过结尾的 ---

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
                i += 2  # skip separator row
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
                        # H1 融入段落作为简介前缀（不单独渲染为标题块）
                        first_h1_skipped = True
                        # 跳过 H1，让内容自然展开；标题在公众号后台单独设置
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

            # ── 图片（独立行）──
            m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', line)
            if m:
                html_parts.append(self.r.image(m.group(1), m.group(2)))
                i += 1
                continue

            # ── 空行 ──
            if line.strip() == '':
                i += 1
                continue

            # ── Emoji 开头的紧凑列表行 ──
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

<section style="max-width:680px;margin:0 auto;padding:32px 44px;font-family:'PingFang SC','Noto Sans SC',-apple-system,sans-serif;color:{C_TEXT};background:#FFFFFF;border-radius:4px;">

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
