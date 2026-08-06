---
name: super-slides
description: >-
  创建美观、实用的演示材料，主输出为 HTML 互动演示稿，可选导出 PPT/PDF。用于用户要做演示、PPT、
  分享稿、演讲稿、培训材料、答辩、路演、汇报、产品介绍、pitch deck 或课件。即使只说“帮我做个分享”
  或“我要汇报一下”，只要需要结构化演示也应触发。
---

# Super Slides

用分阶段、按需加载的方式生成演示稿。不要一次读取所有参考文件。

## 交付合约

1. 先确认或建立内容大纲，再做视觉设计。
2. 主交付是一个可移植文件夹，至少包含 `index.html` 和离线字体备份 `index-backup.html`。
3. 每页只传达一个主要判断；内容超载时拆页，不压缩字号硬塞。
4. 网络研究、PDF/PPT 导出和在线部署都是按需步骤，不是默认副作用。
5. 只有用户明确选择“部署到线上”后，才可调用外部托管服务。

## 输出边界

开始写文件前，确定一个 `PROJECT_DIR`：

- 优先使用当前项目已授权的交付目录。
- 没有现成项目时，在当前工作目录下创建 `[topic]-slides/`。
- 只有用户明确选择桌面时才写桌面。
- 参考文件中的 `$PROJECT_DIR` 始终指向这个已确认目录。

一旦确定，所有大纲、图表数据、素材、HTML 和导出文件都保持在该目录内。

## 分阶段路由

### 1. 项目与内容

仅读 [project-and-content.md](references/project-and-content.md)。

- 选择“现有文件”、“现有内容”或“从主题开始”。
- 用户已给出足够信息时不重复提问。
- 为事实、数据和外部案例保留来源；用户确认大纲后，再移除面向编辑的临时标记。
- 产出 `PROJECT_DIR/.slide-design/outline.md`。

用户确认大纲前，不进入完整视觉生成。

### 2. 风格发现

大纲确认后，仅读 [style-discovery.md](references/style-discovery.md)。

- 无参考时从 [STYLE_PRESETS.md](STYLE_PRESETS.md) 和 `style-preview.html` 中选。
- 有模板、Logo 或品牌文档时，先分析它们，再提炼配色、字体、网格和图片规则。
- 风格不明时给出少量候选供用户选；已有明确品牌规范时直接遵循。

### 3. 生成与验证

内容和风格都确认后，读 [html-generation.md](references/html-generation.md)，并按需读：

- [viewport-base.css](viewport-base.css)：必须完整纳入演示稿。
- [html-template.md](html-template.md)：HTML 结构参考。
- [animation-patterns.md](animation-patterns.md)：只选 1–2 种统一动画。
- [STYLE_PRESETS.md](STYLE_PRESETS.md)：只读用户选中的风格段落。

交付前检查：

- 导航点数量与页数一致。
- 每页适配 `100vh/100dvh`，不出现滚动溢出。
- 字号使用 `clamp()`，图片有高度上限。
- 键盘、触摸和减少动效偏好都可用。
- 本地图片使用相对路径，备份版离线仍可读。
- 使用真实浏览器进行至少一次完整预览。

### 4. 修改、导出与部署

用户看过 HTML 后，才读 [delivery-and-export.md](references/delivery-and-export.md)。

- 小改直接修改 HTML 并重新验证。
- 结构性改动返回内容阶段；换视觉方向返回风格阶段。
- PDF 导出可用 `scripts/export-pdf.sh`。
- `scripts/extract-pptx.py` 需要 `python-pptx`，只在确实需要抽取 PPTX 时安装。
- 在线部署可用 `scripts/deploy.sh`，但必须有用户当次明确授权。

## 回退策略

- 无法加载网络字体：交付 `index-backup.html`，不阻塞整个演示稿。
- 无法安装导出依赖：保留已验证 HTML，如实说明 PDF/PPT 未生成。
- 外部部署失败：不重复发布未经确认的版本，保留本地交付并报告错误。
