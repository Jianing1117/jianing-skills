# Stage 2 Demo Mode

Read this file only when the user wants to preview B but has no confirmed personal IP, Guide, matching character image, photo, or style selection.

## Start without blocking

Use `../assets/default-demo-character-style-3.png` as the reference. Skip Stage 1, profile questions, photo intake, and the six-style gate. Say:

```text
可以，先进入 B 的默认体验模式。我会临时使用内置的第 3 种「3D软萌」示范角色；默认生成 3 张独立插图。这只是功能预览，不会替代你的个人 IP。
```

If the user supplied content, use it and infer up to three high-value scenes. If they supplied a count, honor it. If they supplied no content and only asked to see the effect, do not ask another question; generate the sample set below.

## Demo adapter

```yaml
illustration_adapter:
  style_family: dimensional-3d
  default_variant: style-3-soft-cute-demo
  reference_assets:
    dimensional_3d: ../assets/default-demo-character-style-3.png
  identity:
    hair: long softly layered black hair with a gentle side-center part
    face: rounded stylized adult face, large gentle dark-brown eyes, small friendly smile
    skin: warm fair matte skin direction
    outfit: ivory mock-neck short-sleeve top and white high-waist trousers
    accessories: pearl stud earrings and one white jade bangle
    temperament: gentle, intelligent, lively, approachable
  palette: ivory, warm beige, dark brown-black, sparse soft blue or rose accents, pure white background
  render:
    dimensional_3d: soft clay-like matte materials, larger rounded head, compact adult proportions, diffused warm studio light
  preserve: [same face, black hair silhouette, ivory-and-white outfit, pearl studs, white jade bangle, matte soft-cute 3D material]
  avoid: [photorealism, flat 2D, glossy plastic, child proportions, identity drift, red bracelet, invented user identity or biography]
```

Attach the bundled image and use `illustration-3d.md` plus the real-object prompt in `prompt-3d.md`. The character must act inside the scene.

## Built-in sample set

Use the neutral theme `学习 AI 的三步节奏：筛选信息、动手练习、复盘积累` and generate three standalone 16:9 images:

1. **筛选信息** — One overflowing tray of AI cards. The character physically sorts them into three slots labeled `重要`, `稍后`, `忽略`.
2. **动手练习** — One workbench with a small laptop, notebook, and a bridge made from practice blocks. The character places the last block; labels: `先做`, `再懂`, `迭代`.
3. **复盘积累** — One book-step path leading to a small glowing archive box. The character carries a note into the box; labels: `记录`, `复盘`, `积累`.

Keep every scene on seamless `#FFFFFF`, with restrained objects, clear physical contact, shared light and perspective, and no claim that the sample topic describes the user.

## Handoff after images

Never end the demo silently. After all demo images appear, send this as a separate assistant message, never inside an image:

```text
这是 B 的默认示范效果，使用的是内置第 3 种「3D软萌」角色。接下来你可以：
A. 上传照片，创建并替换成你自己的个人 IP。
B. 继续使用示范角色，把你的文章、主题或项目节点发给我。
C. 上传已有的 usage-guide.md 和角色图，改用你已有的 IP。
```
