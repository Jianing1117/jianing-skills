## Phase 2: 风格发现

**这是"展示而非讲述"的阶段。** 大多数人无法用语言表达设计偏好。

`PROJECT_DIR` 已由主 `SKILL.md` 确定。本文中的素材和配置都必须保存在该目录内。

### Step 2.0: 询问风格路径

询问用户（header: "风格"）：
"你想怎么确定演示稿的风格？"

选项：
- **"浏览风格库"（推荐）** — 从 30 种精选风格中选择
- **"使用我的模板"** — 我有现成的模板/参考图片，帮我套用
- **"上传参考素材"** — 上传 PPT、图片或品牌文档，我来提炼风格

---

### 路径 A: 浏览风格库

**触发：** 用户选择"浏览风格库"或没有参考素材

**Step 2.1A: 打开风格库**

```bash
open ~/.claude/skills/super-slides/style-preview.html
```

风格库包含 30 种风格，按使用场景组织：
- 🔮 科技未来 (5) — 技术演讲、产品发布、AI/区块链
- 💼 商务专业 (5) — 商业提案、财务报告、投资人路演
- 🎨 创意设计 (5) — 设计分享、创意提案、作品集
- 📖 优雅文艺 (6) — 文化分享、读书会、品牌故事
- 🌿 温暖友好 (4) — 教育讲座、社区分享、新手培训
- ⬜ 极简聚焦 (5) — TED 演讲、大会开场、金句展示

**Step 2.2A: 用户选择**

询问用户（header: "选择"）：
"你喜欢哪种风格？告诉我编号（如 05、12、23）"

记住选择，用于 Phase 3。风格定义在 [STYLE_PRESETS.md](../STYLE_PRESETS.md)。

---

### 路径 B: 使用我的模板

**触发：** 用户选择"使用我的模板"或有现成的模板/参考图片

**Step 2.1B: 检查素材文件夹**

首先检查 `assets/` 文件夹是否有素材：
```bash
ls -la "$PROJECT_DIR/assets/"
```

**如果有素材：**
- 继续下一步
- 娡板图片建议命名为 `template-*.jpg/png` 或按顺序命名
- Logo 建议命名为 `logo.*` 或包含"logo"字样

**如果没有素材：**
- 提醒用户："请把模板图片或 Logo 放到 assets/ 文件夹里"
- 等待用户放入后，重新检查再继续

**Step 2.2B: 分析模板图片**

**用 Read 工具读取 assets/ 中的模板图片，使用 analyze_image 分析每张模板：**

对于每张模板，识别：

1. **页面类型**：封面 / 目录 / 内容页 / 结尾页 / 特殊页

2. **背景类型**：
   - 实景照片（校园/建筑/场景）
   - 纯色背景（什么颜色？）
   - 渐变背景（什么颜色？）

3. **Logo 位置**：
   - 封面页：top-center / top-left / top-right / 无
   - 内容页：top-right / top-left / bottom-right / 无
   - 结尾页：top-center / top-left / top-right / 无

4. **配色方案**：
   - 主色（Primary）
   - 辅助色（Secondary）
   - 强调色（Accent）
   - 背景色（Background）

5. **字体信息**：
   - 标题字体：衬线 / 无衬线？粗细？
   - 正文字体：衬线 / 无衬线？粗细？
   - 字号比例：标题是正文的几倍？

6. **叠加层样式**（针对实景照片背景）：
   - 封面/结尾页：深色蒙版（如蓝色 rgba(30,39,97,0.75)）
   - 内容页：浅色蒙版（如 rgba(245,243,239,0.92)）

7. **排版特征**：
   - 标题位置：居中 / 左对齐 / 右对齐
   - 内容布局：单栏 / 双栏 / 网格 / 自由
   - 页码位置：有/无，在哪里

8. **装饰元素**：
   - 分隔线：有/无，样式？
   - 几何形状：有/无？
   - 图标：有/无，风格？

9. **特殊组件样式**：
   - 信息框：背景色、圆角、边框
   - 卡片：阴影、圆角、边框
   - 按钮/链接：样式

10. **页面结构比例**：
   - 标题区高度占比
   - 内容区留白比例
   - 页脚/页码位置

**Step 2.3B: 提取 Logo**

**如果模板中有 Logo：**

1. **定位 Logo**：找到 Logo 所在的模板图片

2. **裁剪 Logo**（需要 Pillow）：

   **先检查 Pillow 是否安装：**
   ```bash
   python3 -c "from PIL import Image; print('Pillow 已安装')" 2>/dev/null || pip3 install Pillow
   ```

   **裁剪代码：**
   ```python
   # 使用 Pillow 从模板中裁剪 Logo 区域
   from PIL import Image
   import os

   assets_dir = os.path.join(os.environ["PROJECT_DIR"], "assets")

   # 打开包含 Logo 的模板
   img = Image.open(os.path.join(assets_dir, "template-01.jpg"))
   w, h = img.size

   # 根据分析结果确定 Logo 位置（通常在角落）
   # 示例：右上角 Logo
   logo_size = int(w * 0.1)  # Logo 大约占宽度 10%
   margin = int(w * 0.03)

   left = w - logo_size - margin
   top = margin
   right = w - margin
   bottom = logo_size + margin

   logo = img.crop((left, top, right, bottom))

   # 保存 Logo（需要处理透明背景）
   # 如果背景是纯色，可以转为透明
   logo.save(os.path.join(assets_dir, "logo.png"))
   ```

   **如果自动裁剪失败：**
   - 提醒用户："自动裁剪 Logo 失败，请手动裁剪 Logo 放到 assets/ 文件夹里"
   - 建议工具：美图秀秀、Photoshop、在线工具

3. **记录 Logo 位置规则**：
   - 封面页 Logo 位置：________
   - 内容页 Logo 位置：________
   - 结尾页 Logo 位置：________

**Step 2.4B: 提取背景图片**

**对于实景照片背景的页面：**

1. **识别哪些页面使用实景照片**
2. **提取这些背景图片**：
   - 如果模板是完整的 PPT 页面截图，需要裁剪出背景区域
   - 保存为 `bg-cover.jpg`, `bg-content-1.jpg`, `bg-ending.jpg` 等
3. **记录背景使用规则**：
   - 封面页使用：________
   - 内容页使用：________（哪些用照片，哪些用纯色）
   - 结尾页使用：________

**Step 2.5B: 生成模板分析报告**

**创建 `.slide-design/template-analysis.json`：**

```json
{
  "templateName": "杭州师范大学答辩PPT",
  "logo": {
    "file": "assets/logo.png",
    "coverPosition": "top-center",
    "contentPosition": "top-right",
    "endingPosition": "top-center"
  },
  "backgrounds": {
    "cover": "assets/bg-cover.jpg",
    "content": {
      "photo": ["assets/bg-content-1.jpg", "assets/bg-content-2.jpg"],
      "solid": ["#F5F3EF"]
    },
    "ending": "assets/bg-ending.jpg"
  },
  "overlays": {
    "cover": "rgba(30,39,97,0.75)",
    "contentPhoto": "rgba(245,243,239, 0.92)",
    "ending": "rgba(30,39,97,0.75)"
  },
  "colors": {
    "primary": "#1E2761",
    "secondary": "#E8EEF5",
    "accent": "#4A90D9",
    "background": "#F5F3EF",
    "textOnDark": "#FFFFFF",
    "textOnLight": "#2C2C2C"
  },
  "fonts": {
    "display": {
      "family": "Noto Serif SC",
      "weight": "600"
    },
    "body": {
      "family": "Noto Sans SC",
      "weight": "400"
    },
    "titleToBodyRatio": "1.8"
  },
  "layoutPatterns": {
    "cover": "居中标题 + 信息框",
    "contents": "左侧大标题 + 右侧网格",
    "content": "上标题 + 下内容",
    "ending": "居中感谢语"
  },
  "components": {
    "infoBox": {
      "background": "rgba(255,255,255,0.12)",
      "borderRadius": "6px",
      "border": "1px solid rgba(255,255,255,0.2)",
      "backdropFilter": "blur(8px)"
    },
    "card": {
      "background": "#FFFFFF",
      "borderRadius": "6px",
      "shadow": "0 2px 15px rgba(0,0,0,0.04)",
      "leftBorder": "3px solid var(--color-primary)"
    }
  },
  "decorations": {
    "divider": "none",
    "geometricShapes": "none",
    "icons": "minimal, blue circles"
  },
  "structure": {
    "titleAreaHeight": "15%",
    "contentAreaPadding": "5%",
    "pageNumberPosition": "bottom-right"
  }
}
```

**Step 2.6B: 用户确认**

询问用户（header: "确认"）：
"我已经分析了你的模板，提取了 Logo、背景和配色。风格预览已保存，确认无误吗？"

选项：
- **"确认，继续"** → 进入 Phase 3
- **"调整一下"** → 询问具体调整需求

---

### 路径 C: 上传提炼

**触发：** 用户选择"上传参考素材"或描述了具体风格要求

**Step 2.1C: 收集参考**

询问用户（header: "素材"）：
"请分享你的参考素材（PPT、图片、品牌文档或网站链接），或者描述你想要的风格（颜色、字体、气质）"

**Step 2.2C: 提炼 VI 元素**

**如果用户提供视觉参考（PPT/图片/品牌文档）：**

1. **读取素材**
   - PPT → 用 pptx skill 提取内容
   - 图片 → 用 Read 工具读取
   - 品牌文档 → 用 Read 工具读取

2. **检查 Logo**
   - 是否存在品牌 Logo？
   - Logo 位置：左上角 / 右上角 / 右下角 / 居中
   - 如果有 Logo，记住位置，用于后续所有 slide

3. **提取颜色**
   - Primary: 主色
   - Secondary: 辅助色
   - Accent: 强调色
   - Background: 背景色

4. **提取字体**
   - Display font: 标题用
   - Body font: 内容用

5. **视觉特征**
   - 圆角: 锐利 / 柔和 / 圆润
   - 阴影: 无 / 柔和 / 硬边
   - 渐变: 无 / 微妙 / 大胆

**如果用户提供文字描述：**
- 解析描述中的具体要求
- 根据描述的气质填补空白

**提炼检查清单：**

1. **颜色**
   - Primary: 主色
   - Secondary: 辅助色
   - Accent: 强调色
   - Background: 背景色

2. **字体**
   - Display font: 标题用
   - Body font: 内容用

3. **视觉特征**
   - 圆角: 锐利 / 柔和 / 圆润
   - 阴影: 无 / 柔和 / 硬边
   - 渐变: 无 / 微妙 / 大胆

4. **整体气质**
   - 专业度: 正式 / 中性 / 友好
   - 现代感: 经典 / 现代 / 前卫
   - 情感基调: 冷静 / 温暖 / 活力

**Step 2.3C: 生成风格预览卡片**

创建单卡片 HTML 预览：
- 使用提取的颜色
- 应用字体搭配
- 展示视觉特征
- 显示气质关键词
- **如果有 Logo**：将 Logo 嵌入预览卡片

保存到 `.slide-design/custom-style-preview.html` 并在浏览器中打开。

**Step 2.4C: 用户确认**

询问用户（header: "确认"）：
"这是根据你的品牌提炼的风格，可以吗？"

选项：
- "可以，继续"
- "调整一下"

如果"调整一下"，询问要调整什么，重新生成预览。

**Step 2.5C: 保存风格配置**

确认后保存到 `.slide-design/custom-style.json`：

```json
{
  "styleName": "Custom Brand Style",
  "colors": {
    "primary": "#1E2761",
    "secondary": "#CADCFC",
    "accent": "#D4AF37",
    "background": "#0a0a0a"
  },
  "fonts": {
    "display": "Playfair Display",
    "body": "Lato"
  },
  "traits": {
    "borderRadius": "4px",
    "shadowStyle": "soft",
    "gradientUse": "subtle"
  },
  "vibe": ["professional", "luxury", "trustworthy"],
  "logo": {
    "src": "path/to/logo.png",
    "position": "top-left"
  }
}
```

> **Logo position 可选值：** `top-left`（左上角）、`top-right`（右上角）、`bottom-right`（右下角）、`center`（居中）

**✅ Phase 2 完成，进入 Phase 3: 生成演示**

---
