## Phase 3: 生成演示

**Phase 1 已确认内容，Phase 2 已确认风格 → 直接生成，无需再确认**

`PROJECT_DIR` 已由主 `SKILL.md` 确定。本文中的输出与素材操作都以它为根。

### Step 3.0: 加载已确认数据

从 Phase 1 获取：
- `slide_outline`: [{ type, title, content, images? }, ...]
- `slide_count`: number

从 Phase 2 获取：
- `style_id`: "01"-"30" 或
- `custom_style`: { colors, fonts, traits, vibe, logo? } 或
- `template_analysis`: { logo, backgrounds, colors, fonts, ... }（Path B）

**检查 assets/ 文件夹：**
```bash
ls -la "$PROJECT_DIR/assets/"
```
- 如果有图片（Logo、背景、插图），记住路径用于 HTML 生成
- 图片引用使用相对路径：`assets/xxx.png`

### Step 3.1: 加载风格定义

**如果是预设编号：**
1. 读取 [STYLE_PRESETS.md](../STYLE_PRESETS.md) 中对应风格
2. 提取 colors、fonts、traits

**如果是定制风格：**
1. 读取 `.slide-design/custom-style.json`
2. 检查是否有 `logo` 字段

### Step 3.2: 加载模板文件

**必须读取：**
- [viewport-base.css](../viewport-base.css) → 完整复制到 `<style>` 中
- [html-template.md](../html-template.md) → 参考 HTML 结构
- [animation-patterns.md](../animation-patterns.md) → 参考动画实现

### Step 3.3: 设计思考

**在生成代码前，先思考设计方向：**

1. **整体调性** — 根据风格定义确认调性：是极简克制，还是丰富热烈？是经典优雅，还是前卫大胆？
2. **记忆点** — 这个演示稿最让人记住的一个视觉特征是什么？
3. **动画策略** — 选择 1-2 种核心动画效果，贯穿始终（不要每页不同）

**调性参考：**
- 极简克制 → 大量留白、精确的间距、微妙的动画
- 丰富热烈 → 层叠渐变、动态背景、大胆的排版
- 经典优雅 → 衬线字体、对称布局、克制的装饰
- 前卫大胆 → 非对称、打破网格、意外的颜色组合

### Step 3.4: 设计美学指南

**字体：**
- 选择独特、有性格的字体，避免 Inter、Roboto、Arial
- 标题用 Display 字体（衬线/装饰性），正文用 Body 字体（易读）
- 从 Google Fonts 或 Fontshare 加载

**颜色：**
- 用 CSS 变量统一管理
- 主色占主导，强调色只用于关键点
- 背景要有层次：渐变、纹理、或微妙的图案

**动画：**
- 一致性 > 多样性：选择一种动画风格贯穿始终
- 重点时刻用动画：页面进入、关键数据、章节转换
- 支持 `prefers-reduced-motion`

**空间：**
- 可以尝试非对称布局、元素重叠、对角线流动
- 不要每页都居中，创造视觉节奏
- 内容密度要克制，留白是设计的一部分

**背景：**
- 避免纯色背景，添加：渐变 mesh、噪点纹理、几何图案、层叠透明度

**避免 "AI slop"：**
- ❌ 紫色渐变 + 白色背景
- ❌ 居中对称的卡片布局
- ❌ 统一的圆角
- ❌ Inter / Roboto / Space Grotesk
- ❌ 每页相同的模板结构

---

### Step 3.5: 内容密度限制

**每页内容有上限，超出则拆分：**

| 页面类型 | 最大内容 |
|----------|----------|
| 标题页 | 1 个标题 + 1 个副标题 + 可选 tagline |
| 内容页 | 1 个标题 + 4-6 个要点 或 2 段文字 |
| 功能网格 | 1 个标题 + 最多 6 张卡片（2x3 或 3x2）|
| 引用页 | 1 段引用（最多 3 行）+ 署名 |
| 代码页 | 1 个标题 + 8-10 行代码 |
| 图片页 | 1 个标题 + 1 张图片（最高 60vh）|

**内容超出？拆成多页，不要硬塞。**

---

### Step 3.6: Viewport 适配规则

**这些规则不可违反：**

```css
/* 每个 slide 必须有 */
.slide {
  height: 100vh;
  height: 100dvh;  /* 移动端动态视口 */
  overflow: hidden;
}

/* 所有字号必须用 clamp() */
h1 { font-size: clamp(2rem, 5vw, 4rem); }
p  { font-size: clamp(1rem, 2vw, 1.25rem); }

/* 图片必须有 max-height */
img { max-height: min(50vh, 400px); }

/* 需要断点适配 */
@media (max-height: 700px) { /* 紧凑布局 */ }
@media (max-height: 600px) { /* 更紧凑 */ }
@media (max-height: 500px) { /* 最小高度适配 */ }
```

**完整规则在 [viewport-base.css](../viewport-base.css) 中，必须完整复制到每个演示稿。**

---

### Step 3.7: 生成 HTML

**输出结构：**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[主题]</title>

  <!-- 字体加载：选择独特字体 -->
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

  <style>
    /* ========================================
       SECTION 1: VIEWPORT BASE（完整复制）
       ======================================== */
    /* viewport-base.css 的完整内容 */

    /* ========================================
       SECTION 2: CSS 变量
       ======================================== */
    :root {
      --color-primary: ...;
      --color-secondary: ...;
      --color-accent: ...;
      --color-bg: ...;
      --font-display: "Font Name", serif;
      --font-body: "Font Name", sans-serif;
      --radius: ...;
      --shadow: ...;
    }

    /* ========================================
       SECTION 3: 背景与氛围
       ======================================== */
    /* 渐变、纹理、图案 */

    /* ========================================
       SECTION 4: 动画定义
       ======================================== */
    /* 入场动画、微交互 */
    /* 必须包含 prefers-reduced-motion 支持 */

    /* ========================================
       SECTION 5: 布局与 Slide 样式
       ======================================== */
    .slide { ... }
    .slide-title { ... }
    .slide-content { ... }

    /* ========================================
       SECTION 6: 导航
       ======================================== */
    .nav-dots { ... }

    /* ========================================
       SECTION 7: 特殊页面样式
       ======================================== */
    /* 标题页、引用页、网格页等 */
  </style>
</head>
<body>
  <!-- Logo（如有）-->
  <img class="brand-logo" src="..." alt="Logo">

  <div class="slides-container">
    <!-- 按大纲逐页生成 -->
    <section class="slide" data-slide="1">
      <!-- 内容 -->
    </section>
    ...
  </div>

  <nav class="nav-dots">
    <button class="nav-dot" data-slide="1"></button>
    ...
  </nav>

  <script>
    /* ========================================
       SECTION 1: 导航逻辑（垂直滚动）
       ======================================== */
    // 键盘：↑ ↓ 方向键 / Page Up / Page Down / Home / End
    // 触屏：上下滑动
    // 滚动：scroll-snap 自动吸附

    /* ========================================
       SECTION 2: 动画逻辑
       ======================================== */
    // Intersection Observer 触发入场动画

    /* ========================================
       SECTION 3: 可选功能
       ======================================== */
    // 进度条、计时器等
  </script>
</body>
</html>
```

**Logo 处理：**
- 固定定位在所有 slide 上层
- 位置由 `logo.position` 决定：`top-left` / `top-right` / `bottom-right` / `center`

---

### Step 3.8: 代码质量标准

- **分区清晰** — 每个主要 section 用注释块分隔
- **命名一致** — CSS 类名使用统一命名规范
- **响应式** — 所有尺寸用 `clamp()` 或 `vw`/`vh`
- **可访问性** — 语义化标签、焦点状态、键盘导航
- **性能** — CSS 优先动画，避免复杂 JS

---

### Step 3.9: 自动验证

- [ ] 每个 `.slide` 有 `height: 100vh; overflow: hidden;`
- [ ] 所有字号使用 `clamp()`
- [ ] 图片有 `max-height` 限制
- [ ] 导航点数量 = slide 数量
- [ ] `prefers-reduced-motion` 支持
- [ ] Logo 位置正确（如有）
- [ ] 代码分区清晰，有注释
- [ ] 无 "AI slop" 特征（紫色渐变、居中卡片、Inter 字体等）

### Step 3.10: 生成输出文件夹

**统一输出为一个文件夹，方便移植：**

```
$PROJECT_DIR/
├── index.html              # 主版本（VI 字体）
├── index-backup.html       # 备份版本（系统字体）
└── assets/                 # 图片资源（如有）
    ├── logo.png
    ├── chart-data-1.png
    └── ...
```

**文件夹结构说明：**

| 文件/文件夹 | 内容 | 必须 |
|-------------|------|------|
| `index.html` | 主版本 HTML | ✅ |
| `index-backup.html` | 备份版本（系统字体） | ✅ |
| `assets/` | 用户上传的图片 | 如有则生成 |

**图片路径引用：**
```html
<!-- HTML 中使用相对路径 -->
<img src="assets/logo.png" alt="Logo">
```

**备份版本字体映射：**

```css
/* 主版本（VI 字体）*/
--font-display: "Clash Display", sans-serif;
--font-body: "Satoshi", sans-serif;

/* 备份版本（系统字体）*/
--font-display: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
--font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
```

**生成方式：**
1. 确认 `$PROJECT_DIR/` 已创建
2. 生成主版本 `index.html`
3. 复制一份为 `index-backup.html`，只替换字体变量
4. 如有图片，创建 `assets/` 文件夹，复制图片进去

### Step 3.11: 保存并打开

```bash
open "$PROJECT_DIR/index.html"
```

---

## Slide 模板库

| 模板类型 | 用途 | 核心元素 |
|----------|------|----------|
| `title` | 标题页 | `<h1>`, `<h2>`, tagline |
| `content` | 内容页 | `<h2>` + `<ul>` / `<ol>` |
| `two-column` | 对比 | 左右两个 `<div>` |
| `feature-grid` | 功能网格 | 2x3 或 3x2 卡片 |
| `quote` | 引用 | `<blockquote>` + `<cite>` |
| `chart` | 数据图表 | 内联 `<svg>` + 标题 + 说明 |
| `image-left` | 图左文右 | `<img>` + `<div>` |
| `image-right` | 图右文左 | `<div>` + `<img>` |
| `full-image` | 全屏图 | `<img>` + 叠加标题 |
| `section` | 章节分隔 | 大号 `<h2>` |
| `ending` | 结束页 | 感谢语 / Q&A / 联系方式 |

根据 Phase 1 大纲中每页的 `type` 字段选择对应模板。

---

## 图表 SVG 生成指南

**当 Phase 1 中标记了 `{{chart: xxx}}` 时，读取对应的 `.slide-design/charts/xxx.json`，生成内联 SVG。**

### 图表类型与 SVG 结构

**柱状图：**
```svg
<svg class="chart bar-chart" viewBox="0 0 600 400">
  <!-- 标题 -->
  <text class="chart-title" x="300" y="30">[图表标题]</text>

  <!-- Y 轴 -->
  <g class="axis y-axis">
    <line x1="60" y1="60" x2="60" y2="320" stroke="var(--text-secondary)"/>
    <!-- 刻度和标签 -->
  </g>

  <!-- X 轴 -->
  <g class="axis x-axis">
    <line x1="60" y1="320" x2="560" y2="320" stroke="var(--text-secondary)"/>
    <!-- 类别标签 -->
  </g>

  <!-- 柱子 -->
  <g class="bars">
    <rect class="bar" x="80" y="100" width="60" height="220" fill="var(--color-primary)"/>
    <!-- 更多柱子... -->
  </g>

  <!-- 数值标签 -->
  <g class="value-labels">
    <text x="110" y="90" class="value">420</text>
    <!-- 更多标签... -->
  </g>
</svg>
```

**折线图：**
```svg
<svg class="chart line-chart" viewBox="0 0 600 400">
  <!-- 坐标轴 -->

  <!-- 数据线 -->
  <polyline
    class="data-line"
    points="80,280 160,220 240,180 320,200 400,140 480,100"
    fill="none"
    stroke="var(--color-primary)"
    stroke-width="3"
  />

  <!-- 数据点 -->
  <g class="data-points">
    <circle cx="80" cy="280" r="6" fill="var(--color-accent)"/>
    <!-- 更多点... -->
  </g>
</svg>
```

**饼图/环形图：**
```svg
<svg class="chart pie-chart" viewBox="0 0 600 400">
  <!-- 使用 stroke-dasharray 技巧绘制扇形 -->
  <circle
    class="pie-segment"
    cx="200" cy="200" r="120"
    fill="none"
    stroke="var(--color-primary)"
    stroke-width="120"
    stroke-dasharray="377 754"  <!-- 周长的一半 = 2πr/2 -->
    stroke-dashoffset="0"
    transform="rotate(-90 200 200)"
  />
  <!-- 更多扇形... -->

  <!-- 图例 -->
  <g class="legend" transform="translate(400, 100)">
    <rect width="16" height="16" fill="var(--color-primary)"/>
    <text x="24" y="14">类别 A</text>
    <!-- 更多图例项... -->
  </g>
</svg>
```

### 图表样式规范

```css
/* 图表容器 */
.chart {
  max-width: 100%;
  max-height: min(50vh, 400px);
  margin: 0 auto;
}

/* 文字使用主题字体 */
.chart-title {
  font-family: var(--font-display);
  font-size: clamp(1rem, 2vw, 1.25rem);
  fill: var(--text-primary);
  text-anchor: middle;
}

.chart text {
  font-family: var(--font-body);
  font-size: clamp(0.75rem, 1.2vw, 0.875rem);
  fill: var(--text-secondary);
}

/* 数值标签突出 */
.value {
  font-weight: 600;
  fill: var(--text-primary);
}

/* 柱子/线条动画 */
.bar, .data-line, .pie-segment {
  animation: chartGrow 0.8s var(--ease-out-expo) forwards;
}

@keyframes chartGrow {
  from { transform: scaleY(0); opacity: 0; }
  to { transform: scaleY(1); opacity: 1; }
}

/* 支持 prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .bar, .data-line, .pie-segment {
    animation: none;
  }
}
```

### 颜色分配

当图表有多个数据系列时，按顺序使用：
1. `var(--color-primary)`
2. `var(--color-secondary)`
3. `var(--color-accent)`
4. 自动生成同色系变体（加深/变浅）

### 图表页面模板

```html
<section class="slide chart-slide">
  <h2 class="reveal">[图表标题]</h2>
  <div class="chart-container reveal">
    <!-- 内联 SVG 图表 -->
    <svg class="chart" ...>...</svg>
  </div>
  <p class="chart-insight reveal">
    <!-- 核心洞察，一句话说明图表的关键信息 -->
  </p>
</section>
```

### 图表可靠性保障

**SVG 图表的优势：**
- ✅ 完全内联，不依赖外部文件
- ✅ 矢量格式，任意缩放不失真
- ✅ 随 HTML 一起部署，无额外请求
- ✅ 支持动画和交互

**唯一风险：字体**

SVG 中的文字使用 `var(--font-body)` 引用主题字体。如果字体从 CDN 加载：
- 在线环境 → 正常显示
- 离线环境 → fallback 到系统字体（视觉略有差异，但内容完整）

**重要演示保障方案：**

| 场景 | 推荐方案 |
|------|----------|
| 正常使用 | HTML 即可，图表 100% 可靠 |
| 重要演讲 | 同时导出 PDF 作为备份 |
| 完全离线 | 内联字体（增加 ~100KB）或用 PDF |
| 投影仪/陌生电脑 | 提前测试，或用 PDF |

**结论：图表本身不会出现"无法显示"的情况，唯一变量是字体。**

---
