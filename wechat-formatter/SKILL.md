---
name: wechat-formatter
description: 把一篇 Markdown 格式的文章转成可直接粘贴到微信公众号编辑器的 HTML 推文 + 900x383px 封面图片，严格遵循「加宁慢慢来」品牌视觉规范。当用户说"排版公众号""帮我生成推文""把这篇文章转成公众号格式""做微信封面"等相关指令时激活此 skill。
---

# Wechat Article Formatter

## 概述

将用户提供的 Markdown 文章，转换成符合「加宁慢慢来」品牌视觉规范、可一键复制粘贴到微信公众号编辑器的纯内联样式 HTML，**并自动生成配套的微信封面图片**。

### 输出内容

每次执行会生成两个文件，放在同一文件夹：
1. **微信公众号 HTML**：`wechat-[标题].html` - 可直接复制粘贴到微信公众号后台
2. **微信封面图片**：`wechat-cover-[标题].png` - 900x383px，2.35:1 比例

核心参考：
- 样式风格：`/Users/jnx/Desktop/wechat-preview.html`（已验证可用的完整排版样本）
- 品牌规范：`/Users/jnx/Documents/aiasme/aiasme/projects/IP/系统规则/【审美】品牌视觉规范文档.md`
- 文章转换脚本：`~/.claude/skills/wechat-formatter/scripts/md_to_wechat.py`
- 封面生成脚本：`~/.claude/skills/wechat-formatter/scripts/generate_cover.py`
- 封面模板：`~/.claude/skills/wechat-formatter/templates/cover_template.html`

---

## 何时激活

以下表达均视为本 skill 触发信号：

- "帮我排版成公众号格式"
- "把这篇 md 转成推文"
- "生成微信公众号 HTML"
- "帮我做公众号排版"
- "转成可以粘贴到公众号的格式"
- "排版公众号"

---

## 品牌视觉规范（快速参考）

### 色板

| 名称 | 色号 | 用途 |
|------|------|------|
| 雾霾蓝 | `#C8D9E6` | 主视觉色，章节数字、边框、分割线 |
| 浅雾蓝 | `#EAF3F8` | 提示框/引用块底色 |
| 白色 | `#FFFFFF` | 页面背景、正文底色 |
| Navy 深蓝 | `#2F4156` | 正文文字、标题、strong |
| Teal 青蓝 | `#567C8D` | 副标题、次级文字 |
| 雾粉 | `#E8CECA` | 底部品牌标识辅助文字、特殊标签 |
| 深粉 | `#B07A72` | 底部品牌 Tag 文字、社群引流文字 |

### 微信排版约束

1. **所有样式必须内联**（inline style），不能用 `<style>` 或 `<class>`，微信编辑器会过滤掉
2. **不能使用外部字体引入**，使用系统字体栈：`'PingFang SC','Noto Sans SC',-apple-system,sans-serif`
3. **图片不处理**，保留原始 `![alt](url)` 提示用户手动上传
4. **最大宽度 680px**，居中显示
5. **链接在公众号中不可点击**，转换为加粗文字或脚注形式

---

## 默认工作流

### 第 0 步：确认输入

收到用户提供的 Markdown 文本后，先检查：

1. 文章是否以 Obsidian YAML frontmatter 开头（`---` 包裹的 key-value 块）——**直接跳过，不渲染**
2. 文章是否有明确的 H1 标题
3. 文章结构（段落、标题层级、是否有列表/表格/引用/代码块）
4. 是否包含需要特殊处理的元素（图片、链接、数学公式）
5. **提取封面信息**：主标题、适合做副标题的英文句子或重要句子、描述文字

### 第 1 步：生成微信公众号 HTML

使用脚本转换（首选）：

```bash
python3 ~/.claude/skills/wechat-formatter/scripts/md_to_wechat.py \
  --input "文章.md" \
  --output "/Users/jnx/Desktop/wechat-[标题]/wechat-[标题].html"
```

或直接传入文本内容进行转换（stdin 模式）：

```bash
python3 ~/.claude/skills/wechat-formatter/scripts/md_to_wechat.py \
  --output "/Users/jnx/Desktop/wechat-[标题]/wechat-[标题].html"
# 然后将文章内容通过 stdin 传入
```

生成后，用 `open` 打开让用户查看：

```bash
open "/Users/jnx/Desktop/wechat-[标题]/wechat-[标题].html"
```

### 第 2 步：生成微信封面图片

使用封面生成脚本：

```bash
python3 ~/.claude/skills/wechat-formatter/scripts/generate_cover.py \
  --title "主标题" \
  --subtitle "副标题（英文或重要句子）" \
  --description "描述文字" \
  --output "/Users/jnx/Desktop/wechat-[标题]/wechat-cover-[标题].png" \
  --highlight "关键词1" "关键词2"
```

生成后，用 `open` 打开让用户查看：

```bash
open "/Users/jnx/Desktop/wechat-[标题]/wechat-cover-[标题].png"
```

**封面设计规范（2026-04-20 最终确认版）**：
- 尺寸：900 x 383 像素（微信标准 2.35:1 比例）
- **正方形缩略图兼容**：必须保证内容区域在正方形裁剪时（微信公众号小图模式）标题完整显示
  - **左右 padding 必须 ≥ 180px**，确保正方形裁剪时左右边缘不切到标题
  - 主标题字号控制在 32-38px，避免过大导致正方形时边缘被切
  - 装饰元素缩小并往中间集中，不要贴边放置
- 配色：雾霾蓝渐变背景（`#C8D9E6` → `#EAF3F8` → `#FFFFFF`）
- 布局：
  - 顶部：副标题（Teal青蓝色，10-11px，letter-spacing:2px）
  - 中间：主标题（Navy深蓝色，32-38px，加粗，letter-spacing:1px）
  - 分割线：雾霾蓝，50px 宽，2px 粗
  - 描述：1-2句话，Teal青蓝色，13px
  - 底部：品牌标签"加宁慢慢来"（雾霾蓝胶囊，11px）
- 装饰元素：圆形几何装饰（缩小，往中间靠）、左侧装饰线（缩短）、右侧小圆点（垂直排列）

> ⚠️ **正方形裁剪注意**：
> - 左右 padding 至少 180px，这是微信封面小图（正方形）裁剪的安全边距
> - 主标题字号建议 32-38px，字号过大会导致正方形时边缘文字被切掉
> - 装饰元素不要贴边放置，留出至少 30px 的安全边距

### 第 3 步：组织输出文件

将生成的两个文件放在同一文件夹：

```
/Users/jnx/Desktop/wechat-[文章标题]/
├── wechat-[标题].html          # 公众号排版 HTML
└── wechat-cover-[标题].png     # 封面图片
```

### 第 4 步：手动构建（脚本不可用时的兜底）

如果脚本不可用，按照以下元素映射规则，逐一将 Markdown 转为内联 HTML。

---

## Markdown → 微信 HTML 元素映射规则

### 外层容器（所有内容的包裹层）

```html
<section style="max-width:680px;margin:0 auto;padding:32px 44px;font-family:'PingFang SC','Noto Sans SC',-apple-system,sans-serif;color:#333333;background:#FFFFFF;border-radius:4px;">
  <!-- 内容 -->
</section>
```

---

### H1 标题（文章主标题，通常在正文前，可选）

H1 一般不单独渲染为标题块，而是融入第一个段落，或者直接跳过（公众号标题在后台设置）。

---

### H2 标题（章节大标题）

用带编号的居中标题块，编号从 01 开始自动递增。**每个 H2 标题必须包含一根分隔横线**，位于数字和标题文字之间。

**样式规范（2026-04-20 最终确认版）**：
- 数字：26px，加粗，`letter-spacing:2px`
- **横线：必须用 `<hr>` 标签**，这是微信编辑器唯一能正常显示的横线实现方式
  - 宽度：60px
  - 粗细：2px
  - 颜色：`#567C8D`（品牌 Teal）
  - 上下间距：`margin:12px auto`（确保数字和标题到横线的距离相等）
- 标题文字：18px，加粗
- 整体居中

> ⚠️ **微信兼容注意**：
> - **横线必须用 `<hr>` 标签**，不能用 `<span border-top>`、`<div>` 或 CSS `border` 属性，微信编辑器会过滤掉这些
> - `<hr>` 标签需要设置 `margin:12px auto` 保证上下间距均匀
> - 禁止用 `display:flex` / `display:inline-block`（微信过滤）

```html
<section style="margin:80px 0 56px;text-align:center;">
  <p style="font-size:26px;font-weight:bold;color:#2F4156;line-height:1;margin:0;padding:0 0 12px;letter-spacing:2px;">01</p>
  <hr style="width:60px;margin:12px auto;border:none;border-top:2px solid #567C8D;">
  <p style="font-size:18px;font-weight:bold;color:#2F4156;line-height:1.6;margin:0;padding:12px 0 0;letter-spacing:0.5px;">章节标题文字</p>
</section>
```

---

### H3 小节标题

```html
<section style="margin:48px 0 16px;">
  <p style="font-size:19px;font-weight:bold;color:#2F4156;line-height:1.5;margin:0 0 8px;letter-spacing:0.3px;">小节标题</p>
  <div style="width:40px;height:4px;background:#C8D9E6;border-radius:2px;"></div>
</section>
```

---

### H4 四级标题

```html
<p style="font-size:17px;font-weight:bold;color:#2F4156;line-height:1.6;margin:32px 0 10px;padding-left:12px;border-left:4px solid #567C8D;letter-spacing:0.3px;">四级标题文字</p>
```

---

### 正文段落

```html
<p style="font-size:16px;color:#333333;line-height:1.9;margin:0 0 32px;letter-spacing:0.5px;">段落内容</p>
```

---

### 加粗（**text**）

```html
<strong style="color:#2F4156;font-weight:bold;">加粗文字</strong>
```

---

### 无序列表（- item）

每个 li 转为带圆点的段落，**左边缘与正文段落对齐，不缩进**：

```html
<p style="font-size:16px;color:#333333;line-height:1.9;margin:0 0 32px;letter-spacing:0.5px;">
  <span style="color:#2F4156;font-weight:bold;margin-right:6px;">·</span>列表项内容
</p>
```

---

### 有序列表（1. item）

左边缘与正文段落对齐，不缩进：

```html
<p style="font-size:16px;color:#333333;line-height:1.9;margin:0 0 32px;letter-spacing:0.5px;">
  <span style="color:#2F4156;font-weight:bold;margin-right:4px;">1.</span>列表项内容
</p>
```

> ⚠️ **重要**：脚本仅识别 Markdown 标准列表语法（`- item` / `1. item`）并转换。  
> 原文中以"第一步""第二步"等中文序号开头的段落，**不得修改文字内容**，按普通段落原样渲染。

---

### Emoji 紧凑列表

当连续多行以 emoji 图标开头（如 ✅、❌、🔴 等），脚本自动识别为**紧凑列表组**，emoji 替换为品牌浅蓝色圆形图标。

```html
<section style="margin:0 0 32px;">
  <p style="font-size:16px;color:#333333;line-height:2.2;margin:0;letter-spacing:0.5px;">
    <span style="display:inline-block;width:16px;height:16px;background:#C8D9E6;border-radius:50%;text-align:center;line-height:16px;font-size:10px;color:#FFFFFF;margin-right:8px;vertical-align:middle;">✓</span>列表项内容
  </p>
</section>
```

---

### 引用块（> blockquote）

```html
<section style="margin:24px 0;padding:16px 20px;background:#EAF3F8;border-left:4px solid #C8D9E6;border-radius:0 8px 8px 0;">
  <p style="font-size:15px;color:#333333;line-height:1.8;margin:0;">引用内容</p>
</section>
```

---

### 代码块（``` code ```）

```html
<section style="margin:18px 0;padding:16px 20px;background:#F5F8FB;border:1px solid #DDE8EF;border-radius:6px;">
  <code style="font-size:13px;color:#2F4156;font-family:'Courier New',Menlo,monospace;white-space:pre-wrap;display:block;line-height:1.7;">代码内容</code>
</section>
```

---

### 表格

```html
<section style="margin:22px 0;overflow-x:auto;-webkit-overflow-scrolling:touch;">
  <table style="border-collapse:collapse;font-size:14px;color:#333333;min-width:100%;">
    <thead>
      <tr>
        <th style="background:#C8D9E6;color:#2F4156;padding:10px 14px;text-align:left;font-weight:bold;border:1px solid #DDE8EF;white-space:nowrap;">列名</th>
      </tr>
    </thead>
    <tbody>
      <tr><td style="padding:10px 14px;border:1px solid #DDE8EF;background:#FFFFFF;line-height:1.6;white-space:nowrap;">内容</td></tr>
      <tr><td style="padding:10px 14px;border:1px solid #DDE8EF;background:#F9FBFC;line-height:1.6;white-space:nowrap;">内容（奇偶行交替）</td></tr>
    </tbody>
  </table>
</section>
```

---

### 链接（[text](url)）

微信公众号文章不支持超链接，转换为括号注释形式：

```html
<span style="color:#2F4156;font-weight:bold;">链接文字</span><span style="font-size:12px;color:#567C8D;">（链接：url）</span>
```

---

### 图片（![alt](url)）

微信图片需要手动上传，转换为占位提示：

```html
<section style="margin:24px 0;padding:14px 18px;background:#EAF3F8;border-left:4px solid #C8D9E6;border-radius:0 8px 8px 0;">
  <p style="font-size:14px;color:#567C8D;line-height:1.8;margin:0;">📷 图片：alt文字（请手动上传图片）</p>
</section>
```

---

### 文章结尾（固定）

每篇文章末尾自动加入结尾区 + **底部品牌卡片图片占位提示**：

```html
<!-- END 结尾 -->
<section style="margin-top:64px;text-align:center;">
  <p style="font-size:11px;color:#BBBBBB;margin:0 0 16px;letter-spacing:5px;">— END —</p>
  <p style="font-size:15px;color:#2F4156;margin:0;line-height:1.8;letter-spacing:0.3px;">欢迎大家关注我的公众号 👇</p>
</section>

<!-- 底部品牌卡片：请手动插入图片 jianing-footer-card.png -->
<section style="margin:20px 0 0;padding:20px;background:#EAF3F8;border-radius:12px;text-align:center;">
  <p style="font-size:13px;color:#567C8D;margin:0;line-height:1.8;">📌 此处请插入底部品牌卡片图片<br><span style="font-size:12px;color:#BBBBBB;">文件：Desktop/jianing-footer-card.png</span></p>
</section>
```

> **底部卡片说明**：底部品牌卡片已预先生成为图片文件 `~/Desktop/jianing-footer-card.png`。粘贴到微信公众号后台后，在文章末尾手动插入该图片即可。  
> 如需重新生成：  
> ```bash
> python3 ~/.claude/skills/wechat-formatter/scripts/generate_footer_card.py --output ~/Desktop/jianing-footer-card.png
> ```

---

## 输出格式要求

### 1. 微信公众号 HTML

生成完整的 HTML 文件，外层包裹 `body { background: #f0f0f0 }` 供浏览器预览，内容区是可复制的白色内联样式 section。

### 2. 微信封面图片

- 尺寸：900 x 383 像素
- 格式：PNG
- 文件名：`wechat-cover-[标题].png`

### 3. 输出文件夹结构

```
/Users/jnx/Desktop/wechat-[文章标题]/
├── wechat-[标题].html          # 公众号排版 HTML
└── wechat-cover-[标题].png     # 封面图片
```

生成完毕后，用 `open` 命令打开两个文件让用户查看：
```bash
open "/Users/jnx/Desktop/wechat-[标题]/wechat-[标题].html"
open "/Users/jnx/Desktop/wechat-[标题]/wechat-cover-[标题].png"
```

---

## 质检清单（交付前自检）

### HTML 排版

- [ ] Obsidian YAML frontmatter 已跳过，不出现在输出中
- [ ] 所有样式已内联，无 `class` 属性
- [ ] 外层容器左右 padding 为 `44px`
- [ ] H2 章节编号从 01 开始，按顺序递增
- [ ] 加粗文字颜色为 `#2F4156`
- [ ] 引用块使用浅雾蓝底色 + 左边框
- [ ] 代码块使用 `#F5F8FB` 底色
- [ ] 表格奇偶行颜色交替（白 / `#F9FBFC`）
- [ ] 链接已转换为文字+括号注释
- [ ] 图片已转换为占位提示
- [ ] 列表项左边缘与正文段落对齐，不缩进
- [ ] **未修改原文任何文字内容**
- [ ] 结尾已加入品牌卡片占位提示
- [ ] 已用 `open` 命令打开 HTML 预览

### 封面图片

- [ ] 尺寸为 900 x 383 像素（2.35:1 比例）
- [ ] 主标题清晰可读，字号 32-38px，加粗
- [ ] 副标题/英文句子在顶部，Teal 青蓝色
- [ ] 描述文字简洁，1-2 句话
- [ ] 品牌标签"加宁慢慢来"在底部，雾霾蓝胶囊样式
- [ ] 配色符合品牌视觉规范（雾霾蓝渐变背景，Navy 文字）
- [ ] 左右 padding ≥ 180px，正方形裁剪时标题不被切
- [ ] 已用 `open` 命令打开 PNG 预览

---

## 封面内容提取规则

### 主标题

- 优先使用文章 H1 标题
- 如果 H1 太长（超过 20 字），提取核心关键词
- 格式：尽量控制在 10-15 字，可拆分为 2 行

### 副标题（顶部英文或重要句子）

从文章中提取，优先级：
1. 文章中出现的英文标题或重要英文句子
2. 文章中加粗的关键句子（不超过 60 字符）
3. 如果没有合适的，根据主题生成一句英文

### 描述文字

- 提取文章第一段或摘要中的关键信息
- 格式：1-2 句话，不超过 60 字符
- 可以用 "·" 分隔多个要点

### 高亮关键词

- 自动识别主标题中的核心概念词
- 一般高亮 2-3 个关键词

---

## 执行偏好

- 默认直接输出完整 HTML 文件和封面图片，而不是只给代码片段
- **两个文件必须保存在同一文件夹**
- 非阻塞问题不等用户确认，先做再说
- H1 标题默认融入文章简介段落，不单独生成标题块（公众号标题在后台单独设置）
- 有疑问的地方（如图片、特殊格式）先做合理处理，交付后再提示用户核查
- 封面副标题优先从文章中提取英文或重要句子，而不是默认生成

---

## 依赖说明

- **md_to_wechat.py**：无外部依赖，Python 3 标准库即可
- **generate_cover.py**：需要 `playwright`（`pip3 install playwright && python3 -m playwright install chromium`）
- **generate_footer_card.py**：需要 `Pillow`（`pip3 install pillow`）
