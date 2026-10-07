---
name: wechat-formatter
description: 把一篇 Markdown 格式的文章转成可直接粘贴到微信公众号编辑器的 HTML 推文 + 900x383px 封面图片，严格遵循「加宁慢慢来」品牌视觉规范 v7.0。当用户说"排版公众号""帮我生成推文""把这篇文章转成公众号格式""做微信封面""WeChat Article Formatter""WeChat Formatter""wechat-formatter""微信文章排版""微信排版"等相关指令时激活此 skill。
---

# Wechat Article Formatter

## 概述

将用户提供的 Markdown 文章，转换成符合「加宁慢慢来」品牌视觉规范 v7.0、可一键复制粘贴到微信公众号编辑器的纯内联样式 HTML，**并自动生成配套的微信封面图片**。

全流程自动化：AI 根据文章内容自动判断文章类型、选择主色、生成封面信息，用户只需提供 Markdown 原文。

### 输出内容

每次执行会生成两个文件，放在同一文件夹：
1. **微信公众号 HTML**：`wechat-[标题].html` - 可直接复制粘贴到微信公众号后台
2. **微信封面图片**：`wechat-cover-[标题].png` - 900x383px，2.35:1 比例

核心参考：
- 样式与品牌规范：本 `SKILL.md` 中的色板、排版约束和元素映射规则
- 文章转换脚本：`scripts/md_to_wechat.py`
- 封面生成脚本：`scripts/generate_cover.py`
- 底部卡片脚本：`scripts/generate_footer_card.py`
- 封面模板：`templates/cover_template.html`
- 文章模板：`templates/article-*.html`（三种文章类型的完整示例）

执行前先解析当前 Skill 目录为 `SKILL_DIR`，并为本次任务创建 `OUTPUT_DIR`。所有脚本和输出都通过这两个变量引用，不要硬编码用户名、桌面、主目录或 Obsidian 路径。

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

## 品牌视觉规范 v7.0（快速参考）

### 色板

| 名称 | 色号 | 用途 |
|------|------|------|
| 展厅白 | `#FFFFFF` | 页面背景、正文底色、封面底色 |
| 雾白 | `#F5F4F0` | 代码块底色 |
| 天蓝 | `#B8D9EA` | 知识/清单类主色：列表圆点、分隔短线、封面色签 |
| 樱粉 | `#E7C4C8` | 随笔/观点类主色：列表圆点、分隔短线 |
| 天蓝白 | `#EBF4F9` | TIP 提示框底色、IMAGE 占位底色 |
| 樱粉白 | `#F8EDEE` | NOTE 提示框底色（随笔模板） |
| 展陈蓝 | `#607EA5` | 所有英文标签（CHAPTER/POINT/TIP/ESSAY/NOTE）、有序列表数字、封面副标题。彩色的字只用展陈蓝，樱粉系文章也一样 |
| 近黑 | `#171717` | 正文文字、标题、strong、表头下线 |
| 注脚灰 | `#77787A` | 注脚、说明文字、封面描述 |
| 中灰 | `#A9AAAB` | END 灰字、DON'T 标签 |
| 陈列灰 | `#D5D5D2` | 细线 |

### 色彩分配规则

按内容类型选主色，**一篇文章只用一个色系**：

- **天蓝系**（知识 / 方法 / 工具 / 清单 / 教程）：
  - 英文标签：展陈蓝 `#607EA5`
  - 圆点 / 短线：天蓝 `#B8D9EA`
  - 提示框：天蓝白 `#EBF4F9` 底 + `TIP` 标签
  - 封面色签：天蓝 `#B8D9EA`

- **樱粉系**（个人 / 情感 / 生活 / 随笔 / 观点）：
  - 英文标签：展陈蓝 `#607EA5`（标签字不随主色变）
  - 圆点 / 短线：樱粉 `#E7C4C8`
  - 提示框：樱粉白 `#F8EDEE` 底 + `NOTE` 标签
  - 封面色签：樱粉 `#E7C4C8`

### 自动判断文章类型

AI 读完文章后自动选择模板，不需要用户指定：

| 类型 | 判断依据 | 模板 | 英文标签 |
|------|----------|------|----------|
| 知识干货 | 有明确章节结构、步骤、对比、表格 | `article-knowledge.html` | `CHAPTER 01` |
| 清单技巧 | 以列表/要点为主，3-7 个平行项 | `article-listicle.html` | `POINT 01` |
| 随笔观点 | 叙事为主，少标题，个人视角 | `article-essay.html` | `ESSAY` |

### 微信排版约束

1. **所有样式必须内联**（inline style），不能用 `<style>` 或 `<class>`，微信编辑器会过滤掉
2. **不能使用外部字体引入**，使用系统字体栈：`'PingFang SC','Noto Sans SC',-apple-system,sans-serif`
3. **用户原文中的图片**保留为占位提示框；**长文自动插图**由 AI 生成（见第 1.5 步）
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
5. **自动判断文章类型**：根据结构选知识/清单/随笔模板和对应主色
6. **提取封面信息**：主标题、英文副标题、描述文字、色签颜色

### 第 1 步：生成微信公众号 HTML

使用脚本转换（首选）：

```bash
SKILL_DIR="<已安装的 wechat-formatter 目录>"
OUTPUT_DIR="./outputs/wechat-<标题>"
mkdir -p "$OUTPUT_DIR"

python3 "$SKILL_DIR/scripts/md_to_wechat.py" \
  --input "文章.md" \
  --output "$OUTPUT_DIR/wechat-<标题>.html"
```

或直接传入文本内容进行转换（stdin 模式）：

```bash
python3 "$SKILL_DIR/scripts/md_to_wechat.py" \
  --output "$OUTPUT_DIR/wechat-<标题>.html"
# 然后将文章内容通过 stdin 传入
```

生成后，用 `open` 打开让用户查看：

```bash
open "$OUTPUT_DIR/wechat-<标题>.html"
```

### 第 1.5 步：自动插图（长文自动触发）

当文章正文超过 **3000 字**或包含 **3 个及以上 H2 章节**时，自动为文章生成品牌风格的配图，插入 HTML 中。短文（<3000 字且 <3 个 H2）不插图。

#### 插图数量

| 文章长度 | H2 章节数 | 插图数 |
|---------|---------|-------|
| 3000–5000 字 | 3–4 | 1 张 |
| 5000–8000 字 | 4–6 | 2 张 |
| 8000 字以上 | 6+ | 2–3 张（最多 3 张） |

#### 插入位置

- 在 **H2 章节之间**插入，不在文章开头或结尾
- 均匀分布：如 2 张图 + 6 个章节，分别放在第 2 和第 4 章节之后
- 插图前后各留 `margin:40px 0`，与正文有呼吸空间

#### 插图风格（严格遵循 brand-kit imagery-prompts.md）

三种风格按文章内容自动选择，**不混用**——一篇文章只用一种：

| 风格 | 适合的文章内容 | 关键词 |
|------|-------------|-------|
| 物件 OBJECT | 工具、方法、清单、具体事物 | 纯白底、一件真实物件、留白四分之三以上、档案馆展签感 |
| 摄影 PHOTOGRAPHY | 生活、人物、场景、叙事 | 低饱和冷灰调、胶片颗粒、韩国画册感、留出空处 |
| 弥散光 DIFFUSED | 抽象、情感、观点、内省 | 雾白底、一团天蓝/樱粉色光晕开、纸纹颗粒、实验感 |

**色相规则**：插图只用文章主色——天蓝系文章用天蓝 `#B8D9EA`，樱粉系文章用樱粉 `#E7C4C8`。其余只有灰和白。

**禁止项**：满版深色、高饱和、插画、3D 渲染、霓虹、光泽反光、彩虹渐变、stock photo 感。

#### 图片尺寸

- 宽度：680px（与正文等宽）
- 比例：16:9（680×383px）或 3:2（680×453px）
- 格式：PNG 或 JPG，单张 <500KB

#### 生成方式

**需要图片生成能力**（如 DALL-E、Midjourney、Flux 等）。按以下优先级：

1. **AI 直接生成**（首选）：如果当前环境有图片生成能力，AI 根据章节内容 + 下面的提示词模板自动生成。
2. **输出提示词让用户生成**（兜底）：如果当前环境没有图片生成能力，为每张插图输出完整的中英文提示词（遵循 brand-kit `06-imagery/imagery-prompts.md` 格式），并在 HTML 中放占位框标注「请用以下提示词生成图片后替换」。

**提示词模板**（以摄影类为例，其他类型见 imagery-prompts.md）：

```
编辑式生活摄影。[根据章节内容描述一个具体场景]。
冷灰调，低饱和，只带一丝极淡的[主色名]（[主色 hex]）。
胶片颗粒，柔焦，大量留白。像韩国服装品牌的画册页。
680x383px，16:9。
```

```
Editorial lifestyle photograph. [scene description from section content].
Cool pale-grey cast, low saturation, only a whisper of [main color name] [hex].
Film grain, soft focus, generous negative space.
Like a lookbook page from a Korean fashion label.
No text, no logo. --ar 16:9 --stylize low
```

**负面词（所有风格通用）**：illustration, cartoon, 3D render, neon, glossy, high contrast, rainbow, busy background, stock photo, dark full-bleed, high saturation

#### 插图的 HTML 格式

生成的图片保存到输出目录，在 HTML 中用以下格式嵌入：

```html
<section style="margin:40px 0;text-align:center;">
  <img src="insert-01.png" alt="章节相关描述" style="width:100%;max-width:680px;border-radius:4px;display:block;margin:0 auto;">
</section>
```

> **注意**：粘贴到微信公众号后台时，图片需要手动上传替换。HTML 中的 `src` 仅用于本地预览。

#### 输出文件

插图文件与 HTML 和封面放在同一目录：

```
<OUTPUT_DIR>/
├── wechat-[标题].html
├── wechat-cover-[标题].png
├── insert-01.png              # 第 1 张插图
├── insert-02.png              # 第 2 张（如有）
└── insert-03.png              # 第 3 张（如有）
```

### 第 2 步：生成微信封面图片

使用封面生成脚本：

```bash
python3 "$SKILL_DIR/scripts/generate_cover.py" \
  --title "主标题" \
  --subtitle "英文副标题（大写，2-5 词）" \
  --description "描述文字" \
  --output "$OUTPUT_DIR/wechat-cover-<标题>.png"
```

生成后，用 `open` 打开让用户查看：

```bash
open "$OUTPUT_DIR/wechat-cover-<标题>.png"
```

**封面设计规范**：
- 尺寸：900 x 383 像素（微信标准 2.35:1 比例）
- 背景：展厅白 `#FFFFFF`（纯白，不用渐变，不加装饰元素）
- 左右 padding：72px，内容靠左对齐
- 布局（从上到下）：
  - 右上角色签：48×4px 色条贴顶边，`right:72px`，颜色跟文章主色（天蓝 or 樱粉）
  - 英文副标题：展陈蓝 `#607EA5`，11px，`letter-spacing:5px`，大写
  - 主标题：宋体衬线（`'Songti SC','Source Han Serif SC','Noto Serif CJK SC',serif`），46px，近黑 `#171717`，`font-weight:600`，`letter-spacing:3px`，最大宽度 720px
  - 描述：注脚灰 `#77787A`，14px，`line-height:1.6`，最大宽度 480px
  - 底部品牌标识：wordmark（已内嵌为 base64，无外部依赖），左下角 `bottom:32px;left:72px`，高度 26px，`opacity:0.8`
- 字体对比：标题用宋体衬线，副标题和描述用无衬线，形成杂志感的软硬对比

### 第 3 步：组织输出文件

将所有文件放在同一文件夹：

```
<OUTPUT_DIR>/
├── wechat-[标题].html          # 公众号排版 HTML
├── wechat-cover-[标题].png     # 封面图片
├── insert-01.png              # 自动插图（长文才有）
├── insert-02.png              # 第 2 张（如有）
└── insert-03.png              # 第 3 张（如有）
```

### 第 4 步：手动构建（脚本不可用时的兜底）

如果脚本不可用，按照以下元素映射规则，逐一将 Markdown 转为内联 HTML。也可参考 `templates/article-*.html` 中的完整示例。

---

## Markdown → 微信 HTML 元素映射规则

### 外层容器（所有内容的包裹层）

```html
<section style="max-width:680px;margin:0 auto;padding:40px 44px;font-family:'PingFang SC','Noto Sans SC',-apple-system,sans-serif;color:#171717;background:#FFFFFF;border-radius:4px;">
  <!-- 内容 -->
</section>
```

---

### H1 标题（文章主标题，通常在正文前，可选）

H1 一般不单独渲染为标题块，而是融入第一个段落，或者直接跳过（公众号标题在后台设置）。

---

### H2 标题（章节大标题）

用英文标签 + 中文标题的组合，编号从 01 开始自动递增。不同模板用不同标签词和颜色。

**知识类（CHAPTER）**：
- 英文标签：11px，展陈蓝 `#607EA5`，`letter-spacing:4px`，`font-weight:500`
- 中文标题：22px，加粗，近黑 `#171717`
- 上间距 72px，与前段拉开距离

```html
<section style="margin:72px 0 48px;">
  <p style="font-size:11px;color:#607EA5;letter-spacing:4px;margin:0 0 6px;font-weight:500;">CHAPTER 01</p>
  <p style="font-size:22px;font-weight:bold;color:#171717;line-height:1.5;margin:0;letter-spacing:0.5px;">章节标题文字</p>
</section>
```

**清单类（POINT）**：
- 英文标签：同上格式
- 中文标题：19px，加粗
- 上间距 56px

```html
<section style="margin:56px 0 20px;">
  <p style="font-size:11px;color:#607EA5;letter-spacing:4px;margin:0 0 6px;font-weight:500;">POINT 01</p>
  <p style="font-size:19px;font-weight:bold;color:#171717;line-height:1.5;margin:0;letter-spacing:0.3px;">要点标题文字</p>
</section>
```

**随笔类（ESSAY）**：
- 不编号，只在文章开头出现一次 `ESSAY` 标签
- 标签用展陈蓝 `#607EA5`
- 段落之间用短线分隔，不用标题

```html
<p style="font-size:11px;color:#607EA5;letter-spacing:4px;margin:0 0 24px;font-weight:500;">ESSAY</p>
```

---

### H3 小节标题

标题下方一道 32px 天蓝短线作为视觉锚点（随笔类用樱粉 `#E7C4C8`）。

```html
<p style="font-size:17px;font-weight:600;color:#171717;line-height:1.5;margin:48px 0 12px;letter-spacing:0.3px;">小节标题</p>
<div style="width:32px;height:3px;background:#B8D9EA;border-radius:2px;margin:0 0 20px;"></div>
```

---

### H4 四级标题

与 H3 相同结构，共用短线样式。

```html
<p style="font-size:17px;font-weight:600;color:#171717;line-height:1.5;margin:48px 0 12px;letter-spacing:0.3px;">四级标题文字</p>
<div style="width:32px;height:3px;background:#B8D9EA;border-radius:2px;margin:0 0 20px;"></div>
```

---

### 正文段落

```html
<p style="font-size:16px;color:#171717;line-height:1.9;margin:0 0 28px;letter-spacing:0.5px;">段落内容</p>
```

---

### 加粗（**text**）

公众号正文可以加粗，这是品牌规范 05 章「正文隐形」在公众号上的例外（2026-10-07 定）。加粗只用近黑，不变色。

```html
<strong style="color:#171717;font-weight:bold;">加粗文字</strong>
```

---

### 无序列表（- item）

用品牌色小圆点（6px），知识/清单类用天蓝 `#B8D9EA`，随笔类用樱粉 `#E7C4C8`。连续列表项紧凑排列。

```html
<section style="margin:0 0 28px;">
<p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;"><span style="display:inline-block;width:6px;height:6px;background:#B8D9EA;border-radius:50%;margin-right:10px;vertical-align:middle;"></span>列表项一</p>
<p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;"><span style="display:inline-block;width:6px;height:6px;background:#B8D9EA;border-radius:50%;margin-right:10px;vertical-align:middle;"></span>列表项二</p>
<p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;"><span style="display:inline-block;width:6px;height:6px;background:#B8D9EA;border-radius:50%;margin-right:10px;vertical-align:middle;"></span>列表项三</p>
</section>
```

---

### 有序列表（1. item）

数字用展陈蓝 `#607EA5`，紧凑排列。

```html
<section style="margin:0 0 28px;">
<p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;"><span style="color:#607EA5;font-weight:600;margin-right:6px;">1.</span>列表项一</p>
<p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;"><span style="color:#607EA5;font-weight:600;margin-right:6px;">2.</span>列表项二</p>
<p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;"><span style="color:#607EA5;font-weight:600;margin-right:6px;">3.</span>列表项三</p>
</section>
```

> **重要**：脚本仅识别 Markdown 标准列表语法（`- item` / `1. item`）并转换。
> 原文中以"第一步""第二步"等中文序号开头的段落，**不得修改文字内容**，按普通段落原样渲染。

---

### Emoji 紧凑列表

当连续多行以 emoji 图标开头（如 ✅、❌、🔴 等），脚本自动识别为**紧凑列表组**，emoji 替换为品牌主色圆形图标。

```html
<section style="margin:0 0 28px;">
  <p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;">
    <span style="display:inline-block;width:16px;height:16px;background:#B8D9EA;border-radius:50%;text-align:center;line-height:16px;font-size:10px;color:#FFFFFF;margin-right:8px;vertical-align:middle;">✓</span>列表项内容
  </p>
</section>
```

---

### 引用块（> blockquote）→ TIP / NOTE 提示框

不用左边框，用浅底色面 + 英文标签。知识/清单类用天蓝白 + TIP，随笔类用樱粉白 + NOTE。

**知识/清单类：TIP**

```html
<section style="margin:28px 0;padding:20px 24px;background:#EBF4F9;border-radius:8px;">
  <p style="font-size:11px;color:#607EA5;letter-spacing:3px;margin:0 0 8px;font-weight:600;">TIP</p>
  <p style="font-size:15px;color:#171717;line-height:1.8;margin:0;">引用内容</p>
</section>
```

**随笔类：NOTE**

```html
<section style="margin:28px 0;padding:20px 24px;background:#F8EDEE;border-radius:8px;">
  <p style="font-size:11px;color:#607EA5;letter-spacing:3px;margin:0 0 8px;font-weight:600;">NOTE</p>
  <p style="font-size:15px;color:#171717;line-height:1.8;margin:0;">引用内容</p>
</section>
```

---

### 代码块（``` code ```）

```html
<section style="margin:18px 0;padding:16px 20px;background:#F5F4F0;border:1px solid #D5D5D2;border-radius:6px;">
  <code style="font-size:13px;color:#171717;font-family:'Courier New',Menlo,monospace;white-space:pre-wrap;display:block;line-height:1.7;">代码内容</code>
</section>
```

---

### 表格

只保留表头下方一根近黑线（2px），不加行线、列线、单元格边框、表头底色。

```html
<section style="margin:28px 0;overflow-x:auto;-webkit-overflow-scrolling:touch;">
  <table style="border-collapse:collapse;font-size:14px;color:#171717;min-width:100%;">
    <thead>
      <tr>
        <th style="padding:10px 14px;text-align:left;font-weight:600;border-bottom:2px solid #171717;white-space:nowrap;">列名</th>
      </tr>
    </thead>
    <tbody>
      <tr><td style="padding:10px 14px;line-height:1.6;white-space:nowrap;">内容</td></tr>
      <tr><td style="padding:10px 14px;line-height:1.6;white-space:nowrap;">内容</td></tr>
    </tbody>
  </table>
</section>
```

---

### 链接（[text](url)）

微信公众号文章不支持超链接，转换为括号注释形式：

```html
<span style="color:#171717;font-weight:bold;">链接文字</span><span style="font-size:12px;color:#607EA5;">（链接：url）</span>
```

---

### 图片（![alt](url)）

分两种情况：

**1. 用户在 Markdown 中写的 `![alt](url)`** → 转为占位提示框（微信图片需手动上传）：

```html
<section style="margin:28px 0;padding:20px 24px;background:#EBF4F9;border-radius:8px;">
  <p style="font-size:11px;color:#607EA5;letter-spacing:3px;margin:0 0 8px;font-weight:600;">IMAGE</p>
  <p style="font-size:14px;color:#607EA5;line-height:1.8;margin:0;">alt文字（请手动上传图片）</p>
</section>
```

**2. AI 自动生成的插图**（见第 1.5 步） → 直接嵌入 `<img>` 标签用于本地预览，粘贴到公众号后台时手动上传替换：

```html
<section style="margin:40px 0;text-align:center;">
  <img src="insert-01.png" alt="描述" style="width:100%;max-width:680px;border-radius:4px;display:block;margin:0 auto;">
</section>
```

---

### 段落分隔短线（随笔类专用）

随笔类文章不用编号章节，用一道 32px 短线分隔段落组。颜色跟主色。

```html
<div style="width:32px;height:3px;background:#E7C4C8;border-radius:2px;margin:52px 0 48px;"></div>
```

---

### DO / DON'T 对照标签（清单类可选）

```html
<p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;"><span style="display:inline-block;padding:2px 10px;background:#EBF4F9;border-radius:10px;font-size:12px;color:#607EA5;font-weight:600;margin-right:8px;vertical-align:middle;">DO</span>推荐做法</p>
<p style="font-size:16px;color:#171717;line-height:2.2;margin:0;letter-spacing:0.5px;"><span style="display:inline-block;padding:2px 10px;background:#F5F4F0;border-radius:10px;font-size:12px;color:#A9AAAB;font-weight:600;margin-right:8px;vertical-align:middle;">DON'T</span>避免做法</p>
```

---

### 文章结尾（固定）

每篇文章末尾自动加入结尾区 + **底部品牌卡片图片占位提示**。占位框颜色跟文章主色。

```html
<!-- END 结尾 -->
<section style="margin-top:72px;text-align:center;">
  <p style="font-size:11px;color:#A9AAAB;margin:0 0 16px;letter-spacing:5px;">— END —</p>
  <p style="font-size:15px;color:#171717;margin:0;line-height:1.8;letter-spacing:0.3px;">欢迎大家关注我的公众号</p>
</section>

<!-- 底部品牌卡片（天蓝版） -->
<section style="margin:20px 0 0;padding:20px;background:#EBF4F9;border-radius:12px;text-align:center;">
  <p style="font-size:11px;color:#607EA5;letter-spacing:3px;margin:0;line-height:1.8;">此处插入底部品牌卡片图片</p>
</section>

<!-- 底部品牌卡片（樱粉版，用于随笔类） -->
<section style="margin:20px 0 0;padding:20px;background:#F8EDEE;border-radius:12px;text-align:center;">
  <p style="font-size:11px;color:#607EA5;letter-spacing:3px;margin:0;line-height:1.8;">此处插入底部品牌卡片图片</p>
</section>
```

> **底部卡片说明**：卡片是定稿的成品图 `templates/footer-card.png`（白底：IP 头像与主标识、Think long / Grow slowly / Compound quietly、慢复利社群与三个板块、网址、小助理二维码）。每篇直接用这张，粘贴到微信公众号后台后，在文章末尾手动插入即可。要改卡片，改 brand kit 的 `05-templates/wechat/footer-card.html` 再导出替换。
> 示例：
> ```bash
> python3 "$SKILL_DIR/scripts/generate_footer_card.py" \
>   --output "$OUTPUT_DIR/jianing-footer-card.png"
> ```

---

## 文章模板

`templates/` 目录下提供三种文章类型的完整示例，手动排版时可作为起点：

| 模板 | 主色 | 适用场景 |
|------|------|----------|
| `article-knowledge.html` | 天蓝 | 知识干货类：CHAPTER 编号章节、TIP 提示框、表格、列表 |
| `article-listicle.html` | 天蓝 | 清单/技巧类：POINT 编号要点、DO/DON'T 对照标签 |
| `article-essay.html` | 樱粉 | 随笔/观点类：ESSAY 标签、NOTE 提示框、短线分隔、无编号 |

---

## 输出格式要求

### 1. 微信公众号 HTML

生成完整的 HTML 文件，外层包裹 `body { background: #f0f0f0 }` 供浏览器预览，内容区是可复制的白色内联样式 section。

### 2. 微信封面图片

- 尺寸：900 x 383 像素
- 格式：PNG
- 文件名：`wechat-cover-[标题].png`

### 3. 自动插图（长文才有）

- 触发条件：正文 >3000 字 或 ≥3 个 H2
- 风格：物件 / 摄影 / 弥散光，一篇只用一种
- 色相：只用文章主色（天蓝或樱粉）+ 灰 + 白
- 尺寸：680px 宽，16:9 或 3:2
- 文件名：`insert-01.png`、`insert-02.png`、`insert-03.png`

### 4. 输出文件夹结构

```
<OUTPUT_DIR>/
├── wechat-[标题].html          # 公众号排版 HTML
├── wechat-cover-[标题].png     # 封面图片
├── insert-01.png              # 自动插图（长文才有）
├── insert-02.png
└── insert-03.png
```

生成完毕后，用 `open` 命令打开文件让用户查看：
```bash
open "$OUTPUT_DIR/wechat-<标题>.html"
open "$OUTPUT_DIR/wechat-cover-<标题>.png"
```

---

## 质检清单（交付前自检）

### HTML 排版

- [ ] Obsidian YAML frontmatter 已跳过，不出现在输出中
- [ ] 所有样式已内联，无 `class` 属性
- [ ] 外层容器左右 padding 为 `44px`
- [ ] 已按内容类型选对主色（天蓝 or 樱粉）
- [ ] 英文标签（CHAPTER/POINT/ESSAY/TIP/NOTE）格式正确
- [ ] 提示框用浅底色面 + 标签，无边框
- [ ] 表格只有表头下方一根近黑线，无其他边框
- [ ] 列表用品牌色小圆点（6px），紧凑排列
- [ ] 代码块使用雾白 `#F5F4F0` 底色
- [ ] 链接已转换为文字+括号注释
- [ ] 用户原文图片已转换为 IMAGE 占位提示
- [ ] 长文（>3000 字或 ≥3 H2）已自动生成插图，风格符合 brand-kit imagery-prompts
- [ ] 插图只用文章主色，无高饱和/满版深色/插画
- [ ] **未修改原文任何文字内容**
- [ ] 结尾已加入品牌卡片占位提示（颜色跟主色）
- [ ] 已用 `open` 命令打开 HTML 预览

### 封面图片

- [ ] 尺寸为 900 x 383 像素（2.35:1 比例）
- [ ] 白色背景，无渐变、无装饰
- [ ] 主标题用宋体衬线字体（Songti SC），46px
- [ ] 英文副标题用展陈蓝 `#607EA5`，大写，宽字距
- [ ] 右上角色签颜色与文章主色一致（天蓝 or 樱粉）
- [ ] 底部 wordmark PNG 可见
- [ ] 已用 `open` 命令打开 PNG 预览

---

## 封面内容提取规则

AI 自动从文章内容中提取以下信息，不需要用户手动指定：

### 主标题

- 优先使用文章 H1 标题
- 如果 H1 太长（超过 20 字），提取核心关键词
- 格式：尽量控制在 10-15 字，宋体衬线字体可拆分为 2 行

### 英文副标题

从文章中提取，优先级：
1. 文章中出现的英文标题或关键短语
2. 根据主题生成简短英文标签（2-5 个词）
3. 大写，宽字距，用作杂志式分类标签

### 描述文字

- 提取文章第一段或摘要中的关键信息
- 格式：1-2 句话，不超过 60 字符
- 注脚灰 `#77787A`，14px

### 色签颜色

- 知识/方法/工具/清单类：天蓝 `#B8D9EA`
- 个人/情感/生活/随笔类：樱粉 `#E7C4C8`

---

## 执行偏好

- 默认直接输出完整 HTML 文件和封面图片，而不是只给代码片段
- **两个文件必须保存在同一文件夹**
- 非阻塞问题不等用户确认，先做再说
- H1 标题默认融入文章简介段落，不单独生成标题块（公众号标题在后台单独设置）
- 有疑问的地方（如图片、特殊格式）先做合理处理，交付后再提示用户核查
- AI 自动判断文章类型、主色、封面信息，用户只需提供 Markdown 原文
- 封面副标题优先从文章中提取英文或重要句子，而不是默认生成
- **长文自动插图**：超过 3000 字或 3 个 H2 的文章，AI 自动生成 1-3 张品牌风格配图插入章节之间，风格严格遵循 brand-kit `06-imagery/imagery-prompts.md`

---

## 依赖说明

- **md_to_wechat.py**：无外部依赖，Python 3 标准库即可
- **generate_cover.py**：需要 `playwright`（`pip3 install playwright && python3 -m playwright install chromium`）
- **generate_footer_card.py**：无外部依赖，只是把 `templates/footer-card.png` 复制到输出目录
