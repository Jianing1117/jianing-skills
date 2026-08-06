# Stage 1 — Build and deliver the IP

Read this file only after the user chooses or clearly requests A.

## Intake and Style Gate

1. Get one clear face or half-body photo; extra angles and outfit references improve consistency. Use photos only for the current task and never package them into the Skill.
2. Collect only missing poster copy in one compact request. Show examples: `IP名称（例：小林慢慢来 / 阿青的AI日记）`, `一句话定位（例：AI领域陪伴式女性博主 / 温和专业的知识型创作者）`, `3–5个关键词（例：温柔、知性、灵动、专业、可信）`, `3–5个使用场景（例：教学、分享、阅读、内容创作、学习记录）`, `标志性道具（例：书、笔记本、茶杯、电脑、平板）`, and `可选口号（例：慢慢来更幸福；可以留空）`.
3. Let the user write “跳过”. Continue without another turn and clearly label editable recommendations: positioning `温和专业的知识型创作者`, keywords `亲和、清晰、可信`, use cases `头像、内容分享、学习记录`, props `书或笔记本、电脑或平板、杯子`; keep the name neutral and slogan empty. Never present defaults as facts or infer sensitive attributes.
4. Before generating, display `../assets/style-reference-board.png` and list: `1 粗线手绘（2D）`, `2 可爱卡通（2D）`, `3 3D软萌（3D）`, `4 清透线稿（2D）`, `5 水彩手绘（2D）`, `6 职场轻熟（3D）`. Ask for one number and wait. For both families, ask for one from `(1/2/4/5)` and one from `(3/6)`. If the board cannot display, list all six in text and still wait. Skip only when the user already chose a style.

## Candidate and delivery

1. Extract identity anchors: hair silhouette, face, skin direction, standard outfit, accessories, temperament. Extract render anchors: line/fill/watercolor for 2D; material/light/proportions for 3D.
2. Read `prompt-templates.md`, use its selected style recipe, and prepare one candidate per chosen family. Finish all other work first, then make this the last text immediately before the image call: `正在生成主形象候选。请等待图片出现后再回复（出图后系统不会自动追加文字）：回复“确认”进入三件套，或回复“修改：……”指出像不像、发型、肤色、服装、配饰、成熟度或整体风格中的关键问题。` Accept confirmation only after the candidate appears; fix important mismatches first.
3. After confirmation, read `character-adapter.md`, prepare the Markdown and prompts, then deliver all three required files:
   - `ip-standard-guide.png`: portrait editorial poster with one hero, front/side views, expressions, actions, scenes, and palette. Use separate `-2d` and `-3d` files when both are confirmed.
   - `ip-usage-guide.png`: matching portrait brand-manual poster with a large portrait, palette, temperament keywords, props, application thumbnails, style traits, and one short usage note.
   - `usage-guide.md`: AI-readable source of truth with the compact marked Fast Path Adapter first, followed by identity/render rules, full prompts, drift controls, and asset paths.

Make the two PNGs a coordinated warm editorial set. Keep identity, palette, typography, and rendering consistent. Reject mismatched faces, hairstyle/outfit/accessory drift, family mixing, invented facts, or logos. Optional application sheets are not required.

## Handoff

Never end Stage 1 silently. After all final images appear, send this as a separate assistant message unless both stages were already requested:

```text
IP Cartoon Guide 三件套已完成。你可以：
A. 到这里结束，直接使用角色标准图、视觉化 Usage Guide 和 Markdown Usage Guide。
B. 继续做内容插图，把文章、主题或项目节点发给我。
如需调整，请回复“修改：……”。
```

Keep the handoff outside every image and outside `usage-guide.md`; it is conversation guidance. Do not treat a pre-image notice as a substitute. Before the image calls, briefly tell the user to wait until both PNGs appear. Only accept A/B after all images appear. If B, ask only for missing content and optional image count.
