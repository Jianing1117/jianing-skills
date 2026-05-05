#!/usr/bin/env python3
"""
微信封面生成脚本
使用 playwright 将 HTML 模板转换为 PNG 图片
"""

import argparse
import asyncio
import os
import re
import tempfile
from pathlib import Path
from string import Template

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ 错误：未安装 playwright")
    print("请运行：python3 -m pip install playwright")
    print("然后运行：python3 -m playwright install chromium")
    exit(1)


# 模板路径
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "cover_template.html"


def sanitize_filename(text):
    """将文本转换为安全的文件名"""
    # 移除或替换不安全的字符
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.strip('-')[:50]  # 限制长度
    return text or "cover"


def extract_keywords_from_content(content, max_length=60):
    """从文章内容中提取关键描述"""
    # 移除 markdown 标记
    content = re.sub(r'#+\s+', '', content)
    content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
    content = re.sub(r'\*(.+?)\*', r'\1', content)
    content = re.sub(r'`(.+?)`', r'\1', content)
    content = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', content)

    # 提取前几句
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    description = ' · '.join(lines[:2])

    # 限制长度
    if len(description) > max_length:
        description = description[:max_length] + '...'

    return description


async def generate_cover_async(
    title: str,
    subtitle: str,
    description: str,
    output_path: str,
    highlight_keywords: list = None
):
    """异步生成封面图片"""

    # 读取模板
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"模板文件不存在：{TEMPLATE_PATH}")

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_html = f.read()

    # 处理关键词高亮
    if highlight_keywords:
        for keyword in highlight_keywords:
            if keyword in title:
                title = title.replace(keyword, f'<span class="highlight">{keyword}</span>')

    # 替换占位符
    html_content = template_html.replace('{{TITLE}}', title)
    html_content = html_content.replace('{{SUBTITLE}}', subtitle)
    html_content = html_content.replace('{{DESCRIPTION}}', description)

    # 创建临时 HTML 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        temp_html_path = f.name

    try:
        # 使用 playwright 截图
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={'width': 900, 'height': 383})

            # 打开临时 HTML 文件
            await page.goto(f'file://{temp_html_path}')
            await page.wait_for_load_state('networkidle')

            # 截图
            await page.screenshot(path=output_path, full_page=False)

            await browser.close()

    finally:
        # 清理临时文件
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)


def generate_cover(
    title: str,
    subtitle: str = None,
    description: str = None,
    output_path: str = None,
    highlight_keywords: list = None
):
    """
    生成微信封面图片

    Args:
        title: 主标题
        subtitle: 副标题（英文或重要句子），如果为 None 则从标题生成
        description: 描述文字，如果为 None 则使用默认描述
        output_path: 输出路径，如果为 None 则保存到桌面
        highlight_keywords: 需要高亮的关键词列表

    Returns:
        str: 生成的 PNG 文件路径
    """

    # 默认副标题
    if not subtitle:
        subtitle = "From Hierarchy to Intelligence"  # 默认英文

    # 默认描述
    if not description:
        description = "AI 如何重新定义组织架构 · 加宁慢慢来"

    # 默认输出路径
    if not output_path:
        desktop = Path.home() / 'Desktop'
        filename = f"wechat-cover-{sanitize_filename(title)}.png"
        output_path = str(desktop / filename)

    # 确保输出目录存在
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 运行异步函数
    asyncio.run(generate_cover_async(
        title=title,
        subtitle=subtitle,
        description=description,
        output_path=output_path,
        highlight_keywords=highlight_keywords
    ))

    return output_path


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='生成微信封面图片')
    parser.add_argument('--title', required=True, help='主标题')
    parser.add_argument('--subtitle', help='副标题（英文或重要句子）')
    parser.add_argument('--description', help='描述文字')
    parser.add_argument('--output', help='输出 PNG 文件路径')
    parser.add_argument('--highlight', nargs='*', help='需要高亮的关键词')

    args = parser.parse_args()

    try:
        output_path = generate_cover(
            title=args.title,
            subtitle=args.subtitle,
            description=args.description,
            output_path=args.output,
            highlight_keywords=args.highlight
        )
        print(f"✅ 封面已生成：{output_path}")
        return 0
    except Exception as e:
        print(f"❌ 生成失败：{e}")
        return 1


if __name__ == '__main__':
    exit(main())
