# Style Presets Reference

30 种精选视觉风格，按使用场景组织。每种风格都支持：动画、图表、卡片等组件。

**Viewport CSS:** 基础样式见 [viewport-base.css](viewport-base.css)，每次生成时必须完整复制。

---

## 🔮 科技未来 (5)

适用于：技术演讲、产品发布、AI/区块链、开发者大会

### 01. Neon Cyber

**Vibe:** Futuristic, techy, confident, high-impact

**Layout:** Deep dark with neon accents. Glowing elements, grid patterns.

**Typography:**
- Display: `Clash Display` (700/800) — Fontshare
- Body: `Satoshi` (400/500) — Fontshare

**Colors:**
```css
:root {
  --bg-primary: #0a0f1c;
  --bg-secondary: #111827;
  --text-primary: #ffffff;
  --text-secondary: #9ca3af;
  --accent-cyan: #00ffcc;
  --accent-magenta: #ff00aa;
  --accent-glow: rgba(0, 255, 204, 0.3);
}
```

**Signature Elements:**
- Neon glow effects (text-shadow, box-shadow)
- Grid/scanline background patterns
- Gradient mesh overlays
- Monospace accents for data

---

### 02. Terminal Green

**Vibe:** Developer-focused, hacker aesthetic, raw authenticity

**Layout:** GitHub dark style. Monospace throughout. Code-block aesthetics.

**Typography:**
- Display: `JetBrains Mono` (700/800)
- Body: `JetBrains Mono` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --text-primary: #c9d1d9;
  --text-secondary: #8b949e;
  --accent-green: #39d353;
  --accent-yellow: #f0883e;
}
```

**Signature Elements:**
- Terminal prompt styling (">$ ")
- Blinking cursor animation
- Scan lines overlay
- Code syntax highlighting colors

---

### 03. Cyberpunk Glow

**Vibe:** Edgy, rebellious, night-city, high contrast

**Layout:** Dark purple base with electric pink/cyan highlights. Chromatic aberration effects.

**Typography:**
- Display: `Orbitron` (700/900)
- Body: `Rajdhani` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #1a1a2e;
  --text-primary: #ffffff;
  --text-secondary: #a0a0b0;
  --accent-pink: #ff2a6d;
  --accent-cyan: #05d9e8;
  --accent-yellow: #f9f871;
}
```

**Signature Elements:**
- Chromatic aberration (RGB split)
- Glitch text effects
- Diagonal stripes/bars
- Neon sign aesthetics

---

### 04. Holographic

**Vibe:** Futuristic, ethereal, premium tech, AR/VR

**Layout:** Dark with iridescent gradients. Glassmorphism elements.

**Typography:**
- Display: `Space Grotesk` (700)
- Body: `Inter` (400/500) — exception for glassmorphism readability

**Colors:**
```css
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #121218;
  --text-primary: #ffffff;
  --text-secondary: #a0a0b0;
  --holo-1: #7b68ee;
  --holo-2: #00d4ff;
  --holo-3: #ff6b9d;
}
```

**Signature Elements:**
- Iridescent/rainbow gradients
- Glassmorphism cards (backdrop-blur)
- Floating 3D elements
- Soft glow shadows

---

### 05. Data Dashboard

**Vibe:** Analytical, precise, data-driven, professional tech

**Layout:** Dark dashboard aesthetic. Cards with subtle borders. Data visualization focused.

**Typography:**
- Display: `DM Sans` (700)
- Body: `DM Sans` (400/500)
- Mono: `Fira Code` (for numbers)

**Colors:**
```css
:root {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --bg-card: #1e293b;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --accent-blue: #3b82f6;
  --accent-green: #22c55e;
  --accent-amber: #f59e0b;
}
```

**Signature Elements:**
- Card-based layouts with subtle borders
- Status indicators (dots/badges)
- Number highlights with mono font
- Subtle grid backgrounds

---

## 💼 商务专业 (5)

适用于：商业提案、财务报告、投资人路演、企业汇报

### 06. Corporate Navy

**Vibe:** Trustworthy, established, conservative, premium

**Layout:** Navy blue dominant. Clean white cards. Gold accents.

**Typography:**
- Display: `Playfair Display` (700)
- Body: `Source Sans Pro` (400/600)

**Colors:**
```css
:root {
  --bg-primary: #0a1628;
  --bg-secondary: #1a2d4a;
  --bg-card: #ffffff;
  --text-primary: #0a1628;
  --text-secondary: #4a5568;
  --accent-gold: #c9a227;
  --accent-blue: #2c5282;
}
```

**Signature Elements:**
- Classic serif headlines
- Gold accent lines/borders
- Clean white content cards
- Subtle texture backgrounds

---

### 07. Finance Graph

**Vibe:** Analytical, growth-oriented, data-focused, trustworthy

**Layout:** Light background. Chart-focused. Green for positive, red for negative.

**Typography:**
- Display: `Libre Baskerville` (700)
- Body: `Lato` (400/600)

**Colors:**
```css
:root {
  --bg-primary: #f8f9fa;
  --bg-secondary: #ffffff;
  --text-primary: #1a1a2e;
  --text-secondary: #6b7280;
  --accent-green: #10b981;
  --accent-red: #ef4444;
  --accent-blue: #3b82f6;
}
```

**Signature Elements:**
- Large data visualizations
- Trend indicators (arrows, sparklines)
- Clean table styling
- Subtle shadows for depth

---

### 08. Minimal Pitch

**Vibe:** Startup, clean, focused, investor-ready

**Layout:** Maximum whitespace. One idea per slide. Bold typography.

**Typography:**
- Display: `Inter` (800/900) — exception for startup aesthetic
- Body: `Inter` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --text-primary: #0a0a0a;
  --text-secondary: #6b7280;
  --accent: #0a0a0a;
}
```

**Signature Elements:**
- Ultra-generous whitespace
- Black & white dominant
- Single accent color (optional)
- Large, confident typography

---

### 09. Trust Blue

**Vibe:** Reliable, professional, corporate, safe

**Layout:** Blue dominant. Centered content. Clear hierarchy.

**Typography:**
- Display: `Merriweather` (700/900)
- Body: `Open Sans` (400/600)

**Colors:**
```css
:root {
  --bg-primary: #1e3a5f;
  --bg-secondary: #2c5282;
  --text-primary: #ffffff;
  --text-secondary: #bee3f8;
  --accent: #f6ad55;
}
```

**Signature Elements:**
- Deep blue gradients
- Warm accent for CTAs
- Centered, balanced layouts
- Subtle wave patterns

---

### 10. Executive Dark

**Vibe:** Premium, exclusive, C-suite, sophisticated

**Layout:** Rich dark background. Gold or silver accents. Elegant spacing.

**Typography:**
- Display: `Cormorant Garamond` (600/700)
- Body: `Montserrat` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #1a1a1a;
  --bg-secondary: #2d2d2d;
  --text-primary: #f5f5f5;
  --text-secondary: #a0a0a0;
  --accent-gold: #d4af37;
  --accent-silver: #c0c0c0;
}
```

**Signature Elements:**
- Luxurious dark tones
- Metallic accent colors
- Elegant serif typography
- Generous spacing

---

## 🎨 创意设计 (5)

适用于：设计分享、创意提案、作品集、品牌展示

### 11. Bold Signal

**Vibe:** Confident, bold, modern, high-impact

**Layout:** Colored card on dark gradient. Number top-left, navigation top-right, title bottom-left.

**Typography:**
- Display: `Archivo Black` (900)
- Body: `Space Grotesk` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #1a1a1a;
  --bg-gradient: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
  --card-bg: #FF5722;
  --text-primary: #ffffff;
  --text-on-card: #1a1a1a;
}
```

**Signature Elements:**
- Bold colored card as focal point
- Large section numbers (01, 02, etc.)
- Navigation breadcrumbs
- Grid-based layout

---

### 12. Creative Voltage

**Vibe:** Bold, creative, energetic, retro-modern

**Layout:** Split panels—electric blue left, dark right. Script accents.

**Typography:**
- Display: `Syne` (700/800)
- Mono: `Space Mono` (400/700)

**Colors:**
```css
:root {
  --bg-primary: #0066ff;
  --bg-dark: #1a1a2e;
  --accent-neon: #d4ff00;
  --text-light: #ffffff;
}
```

**Signature Elements:**
- Electric blue + neon yellow contrast
- Halftone texture patterns
- Neon badges/callouts
- Script typography for creative flair

---

### 13. Artistic Splash

**Vibe:** Expressive, colorful, artistic, playful

**Layout:** White base with abstract color blobs. Asymmetric layouts.

**Typography:**
- Display: `Dela Gothic One` (400)
- Body: `Nunito` (400/600)

**Colors:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8f8f8;
  --text-primary: #1a1a1a;
  --text-secondary: #666666;
  --splash-1: #ff6b6b;
  --splash-2: #4ecdc4;
  --splash-3: #ffe66d;
}
```

**Signature Elements:**
- Abstract color blobs/shapes
- Playful asymmetric layouts
- Hand-drawn style elements
- Vibrant color palette

---

### 14. Brutalist

**Vibe:** Raw, unconventional, bold, anti-design

**Layout:** Harsh contrasts. Raw edges. System fonts. Unconventional spacing.

**Typography:**
- Display: `Courier New` (bold) or `Arial Black`
- Body: `Courier New` (regular)

**Colors:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f0f0f0;
  --text-primary: #000000;
  --text-secondary: #666666;
  --accent: #ff0000;
  --border: #000000;
}
```

**Signature Elements:**
- Thick black borders
- Raw/system typography
- Intentionally "ugly" spacing
- High contrast, no gradients

---

### 15. Gradient Flow

**Vibe:** Modern, smooth, dynamic, digital-native

**Layout:** Flowing gradient backgrounds. Glassmorphism cards. Smooth curves.

**Typography:**
- Display: `Outfit` (700/800)
- Body: `Outfit` (400/500)

**Colors:**
```css
:root {
  --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --text-primary: #ffffff;
  --text-secondary: rgba(255,255,255,0.8);
  --glass-bg: rgba(255,255,255,0.1);
}
```

**Signature Elements:**
- Flowing gradient backgrounds
- Glassmorphism overlays
- Soft, rounded corners
- Smooth animations

---

## 📖 优雅文艺 (6)

适用于：文化分享、读书会、品牌故事、杂志风格

### 16. Dark Botanical

**Vibe:** Elegant, sophisticated, artistic, premium

**Layout:** Centered content on dark. Abstract soft shapes in corner.

**Typography:**
- Display: `Cormorant` (400/600) — elegant serif
- Body: `IBM Plex Sans` (300/400)

**Colors:**
```css
:root {
  --bg-primary: #0f0f0f;
  --text-primary: #e8e4df;
  --text-secondary: #9a9590;
  --accent-warm: #d4a574;
  --accent-pink: #e8b4b8;
  --accent-gold: #c9b896;
}
```

**Signature Elements:**
- Abstract soft gradient circles (blurred, overlapping)
- Warm color accents (pink, gold, terracotta)
- Thin vertical accent lines
- Italic signature typography

---

### 17. Paper & Ink

**Vibe:** Editorial, literary, thoughtful, timeless

**Layout:** Warm cream background. Classic typography. Red accents.

**Typography:**
- Display: `Cormorant Garamond` (600/700)
- Body: `Source Serif 4` (400/500)

**Colors:**
```css
:root {
  --bg-cream: #faf9f7;
  --bg-paper: #ffffff;
  --text-primary: #1a1a1a;
  --text-secondary: #555555;
  --accent-crimson: #c41e3a;
  --accent-gold: #b8860b;
}
```

**Signature Elements:**
- Drop caps for opening paragraphs
- Pull quotes with accent borders
- Elegant horizontal rules
- Classic editorial spacing

---

### 18. Vintage Editorial

**Vibe:** Witty, confident, editorial, personality-driven

**Layout:** Centered content on cream. Abstract geometric shapes as accent.

**Typography:**
- Display: `Fraunces` (700/900) — distinctive serif
- Body: `Work Sans` (400/500)

**Colors:**
```css
:root {
  --bg-cream: #f5f3ee;
  --text-primary: #1a1a1a;
  --text-secondary: #555555;
  --accent-warm: #e8d4c0;
  --accent-rust: #b87333;
}
```

**Signature Elements:**
- Abstract geometric shapes (circle outline + line + dot)
- Bold bordered CTA boxes
- Witty, conversational copy style
- Magazine-style layouts

---

### 19. Editorial Serif

**Vibe:** Classic, authoritative, newspaper, intellectual

**Layout:** Column-based layouts. Strong typography hierarchy. Black & white dominant.

**Typography:**
- Display: `Playfair Display` (700/900)
- Body: `Georgia` (400/400)

**Colors:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #000000;
  --text-secondary: #444444;
  --accent: #cc0000;
}
```

**Signature Elements:**
- Multi-column layouts
- Strong typographic hierarchy
- Red accent for emphasis
- Newspaper-inspired design

---

### 20. Literary

**Vibe:** Bookish, contemplative, sophisticated, quiet

**Layout:** Generous margins. Book-page aesthetic. Subtle textures.

**Typography:**
- Display: `Libre Baskerville` (700)
- Body: `Lora` (400/400)

**Colors:**
```css
:root {
  --bg-primary: #fdfbf7;
  --bg-secondary: #f5f1e8;
  --text-primary: #2c2c2c;
  --text-secondary: #5c5c5c;
  --accent: #8b4513;
}
```

**Signature Elements:**
- Book-page margins
- Subtle paper texture
- Chapter-style headings
- Quiet, refined palette

---

### 21. Japanese Zen

**Vibe:** Minimal, peaceful, balanced, contemplative

**Layout:** Extreme whitespace. Asymmetric balance. Natural tones.

**Typography:**
- Display: `Noto Serif JP` (600/700)
- Body: `Noto Sans JP` (400/400)

**Colors:**
```css
:root {
  --bg-primary: #f7f5f0;
  --bg-secondary: #ebe8e0;
  --text-primary: #2c2c2c;
  --text-secondary: #6b6b6b;
  --accent: #8b0000;
  --accent-gold: #b8860b;
}
```

**Signature Elements:**
- Extreme whitespace
- Asymmetric composition
- Natural, earthy tones
- Subtle texture (washi paper feel)

---

## 🌿 温暖友好 (4)

适用于：教育讲座、社区分享、新手培训、团队内部

### 22. Notebook Tabs

**Vibe:** Editorial, organized, elegant, tactile

**Layout:** Cream paper card on dark background. Colorful tabs on right edge.

**Typography:**
- Display: `Bodoni Moda` (400/700) — classic editorial
- Body: `DM Sans` (400/500)

**Colors:**
```css
:root {
  --bg-outer: #2d2d2d;
  --bg-page: #f8f6f1;
  --text-primary: #1a1a1a;
  --tab-1: #98d4bb; /* Mint */
  --tab-2: #c7b8ea; /* Lavender */
  --tab-3: #f4b8c5; /* Pink */
  --tab-4: #a8d8ea; /* Sky */
  --tab-5: #ffe6a7; /* Cream */
}
```

**Signature Elements:**
- Paper container with subtle shadow
- Colorful section tabs on right edge (vertical text)
- Binder hole decorations on left
- Tab text scales with viewport

---

### 23. Pastel Geometry

**Vibe:** Friendly, organized, modern, approachable

**Layout:** White card on pastel background. Vertical pills on right edge.

**Typography:**
- Display: `Plus Jakarta Sans` (700/800)
- Body: `Plus Jakarta Sans` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #c8d9e6;
  --card-bg: #faf9f7;
  --pill-pink: #f0b4d4;
  --pill-mint: #a8d4c4;
  --pill-sage: #5a7c6a;
  --pill-lavender: #9b8dc4;
  --pill-violet: #7c6aad;
}
```

**Signature Elements:**
- Rounded card with soft shadow
- Vertical pills on right edge with varying heights
- Consistent pill width
- Friendly, rounded aesthetic

---

### 24. Split Pastel

**Vibe:** Playful, modern, friendly, creative

**Layout:** Two-color vertical split (peach left, lavender right).

**Typography:**
- Display: `Outfit` (700/800)
- Body: `Outfit` (400/500)

**Colors:**
```css
:root {
  --bg-peach: #f5e6dc;
  --bg-lavender: #e4dff0;
  --text-dark: #1a1a1a;
  --badge-mint: #c8f0d8;
  --badge-yellow: #f0f0c8;
  --badge-pink: #f0d4e0;
}
```

**Signature Elements:**
- Split background colors
- Playful badge pills with icons
- Grid pattern overlay on right panel
- Rounded CTA buttons

---

### 25. Friendly Rounded

**Vibe:** Approachable, soft, warm, community-focused

**Layout:** Soft rounded cards. Warm color palette. Friendly illustrations (abstract shapes only).

**Typography:**
- Display: `Nunito` (700/800)
- Body: `Nunito` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #fff9f5;
  --bg-secondary: #fff0e6;
  --text-primary: #3d3d3d;
  --text-secondary: #6b6b6b;
  --accent-orange: #ff8c42;
  --accent-yellow: #ffd166;
  --accent-teal: #06d6a0;
}
```

**Signature Elements:**
- Extra rounded corners (16px+)
- Warm, inviting colors
- Soft shadows
- Abstract blob shapes

---

## ⬜ 极简聚焦 (5)

适用于：TED 演讲、大会开场、金句展示、关键信息

### 26. Swiss Modern

**Vibe:** Clean, precise, Bauhaus-inspired, timeless

**Layout:** Visible grid. Asymmetric layouts. Geometric shapes.

**Typography:**
- Display: `Archivo` (800/900)
- Body: `Nunito` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #000000;
  --text-secondary: #666666;
  --accent-red: #ff3300;
}
```

**Signature Elements:**
- Visible grid lines (optional)
- Asymmetric composition
- Geometric accent shapes
- Bold typographic hierarchy

---

### 27. Monochrome

**Vibe:** Pure, focused, dramatic, essential

**Layout:** Black and white only. Maximum contrast. Minimal elements.

**Typography:**
- Display: `Helvetica Neue` (800/900)
- Body: `Helvetica Neue` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #000000;
  --text-primary: #000000;
  --text-secondary: #333333;
  --text-on-dark: #ffffff;
}
```

**Signature Elements:**
- Strict black & white palette
- High contrast photography
- Minimal decorative elements
- Bold, confident typography

---

### 28. Ultra Minimal

**Vibe:** Quiet, refined, spacious, premium minimal

**Layout:** Extreme whitespace. Single focal point per slide.

**Typography:**
- Display: `Inter` (300/400) — exception for minimal aesthetic
- Body: `Inter` (300/400)

**Colors:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #fafafa;
  --text-primary: #1a1a1a;
  --text-secondary: #888888;
  --accent: #1a1a1a;
}
```

**Signature Elements:**
- Extreme whitespace (60%+ empty)
- Light weight typography
- Subtle gray accents
- Single focal point

---

### 29. Big Type

**Vibe:** Bold, confident, statement-making, impactful

**Layout:** Typography as hero. Massive headlines. Minimal supporting content.

**Typography:**
- Display: `Inter` (900) or `Arial Black`
- Body: `Inter` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #000000;
  --text-secondary: #666666;
  --accent: #000000;
}
```

**Signature Elements:**
- Massive display type (120px+)
- Type as visual element
- Minimal supporting graphics
- High contrast

---

### 30. Focus Point

**Vibe:** Intentional, directed, clear, purposeful

**Layout:** Single element in focus. Directional cues. Minimal distractions.

**Typography:**
- Display: `DM Serif Display` (400)
- Body: `DM Sans` (400/500)

**Colors:**
```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #1a1a1a;
  --text-primary: #ffffff;
  --text-secondary: #888888;
  --accent: #ffffff;
}
```

**Signature Elements:**
- Single focal point per slide
- Directional arrows/lines
- Spotlight effect
- Dark background for focus

---

## Font Pairing Quick Reference

| # | Style Name | Display Font | Body Font | Source |
|---|------------|--------------|-----------|--------|
| 01 | Neon Cyber | Clash Display | Satoshi | Fontshare |
| 02 | Terminal Green | JetBrains Mono | JetBrains Mono | JetBrains |
| 03 | Cyberpunk Glow | Orbitron | Rajdhani | Google |
| 04 | Holographic | Space Grotesk | Inter | Google |
| 05 | Data Dashboard | DM Sans | DM Sans | Google |
| 06 | Corporate Navy | Playfair Display | Source Sans Pro | Google |
| 07 | Finance Graph | Libre Baskerville | Lato | Google |
| 08 | Minimal Pitch | Inter | Inter | Google |
| 09 | Trust Blue | Merriweather | Open Sans | Google |
| 10 | Executive Dark | Cormorant Garamond | Montserrat | Google |
| 11 | Bold Signal | Archivo Black | Space Grotesk | Google |
| 12 | Creative Voltage | Syne | Space Mono | Google |
| 13 | Artistic Splash | Dela Gothic One | Nunito | Google |
| 14 | Brutalist | Courier New | Courier New | System |
| 15 | Gradient Flow | Outfit | Outfit | Google |
| 16 | Dark Botanical | Cormorant | IBM Plex Sans | Google |
| 17 | Paper & Ink | Cormorant Garamond | Source Serif 4 | Google |
| 18 | Vintage Editorial | Fraunces | Work Sans | Google |
| 19 | Editorial Serif | Playfair Display | Georgia | Google |
| 20 | Literary | Libre Baskerville | Lora | Google |
| 21 | Japanese Zen | Noto Serif JP | Noto Sans JP | Google |
| 22 | Notebook Tabs | Bodoni Moda | DM Sans | Google |
| 23 | Pastel Geometry | Plus Jakarta Sans | Plus Jakarta Sans | Google |
| 24 | Split Pastel | Outfit | Outfit | Google |
| 25 | Friendly Rounded | Nunito | Nunito | Google |
| 26 | Swiss Modern | Archivo | Nunito | Google |
| 27 | Monochrome | Helvetica Neue | Helvetica Neue | System |
| 28 | Ultra Minimal | Inter | Inter | Google |
| 29 | Big Type | Inter | Inter | Google |
| 30 | Focus Point | DM Serif Display | DM Sans | Google |

---

## DO NOT USE (Generic AI Patterns)

**Fonts:** Roboto, Arial (except Brutalist), system fonts as primary display

**Colors:** `#6366f1` (generic indigo), purple gradients on white, generic blue (#007bff)

**Layouts:** Everything centered, generic hero sections, identical card grids

**Decorations:** Realistic illustrations, gratuitous glassmorphism, drop shadows without purpose

---

## CSS Gotchas

### Negating CSS Functions

**WRONG — silently ignored by browsers (no console error):**
```css
right: -clamp(28px, 3.5vw, 44px);   /* Browser ignores this */
margin-left: -min(10vw, 100px);      /* Browser ignores this */
```

**CORRECT — wrap in `calc()`:**
```css
right: calc(-1 * clamp(28px, 3.5vw, 44px));  /* Works */
margin-left: calc(-1 * min(10vw, 100px));     /* Works */
```

CSS does not allow a leading `-` before function names. The browser silently discards the entire declaration — no error, the element just appears in the wrong position. **Always use `calc(-1 * ...)` to negate CSS function values.**
