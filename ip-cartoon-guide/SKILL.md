---
name: ip-cartoon-guide
description: >-
  Create a reusable personal IP character from user photos and optionally generate matching content illustrations.
  Use for personal brand avatars, cartoon personas, creator mascots, 2D/line-art/watercolor or 3D/rendered character
  guides, “个人IP形象指南”, and article or project illustrations that must preserve the same character. Supports a
  two-stage flow, including a token-efficient direct Stage 2 entry and a built-in Style 3 demo when no personal IP,
  photo, or style choice is available yet.
---

# IP Cartoon Guide

## Contract

Run two stages:

1. Create and confirm the personal IP, then deliver the three-part Guide package: character standard image, visual Usage Guide, and Markdown Usage Guide.
2. Only if the user chooses to continue, turn supplied content into illustrations using the confirmed 2D or 3D character.

If the user already has a Guide and `usage-guide.md`, start at Stage 2.

## Entry

If the user's mode is unclear, make the first reply:

```text
你好，我可以帮你完成两件事：
A. 创建新的个人 IP：从照片开始，生成角色标准图、视觉化 Usage Guide 和 Markdown Usage Guide。
B. 直接生成内容插图：沿用已有 IP，根据文章、主题或项目节点生成同角色插图。
请回复 A 或 B。
```

Do not show this menu when the request already makes A or B clear. For A, ask for one clear face or half-body photo. For B, use the Fast Path below.

## Read only when needed

- `references/stage-1.md`: read only after the user chooses or clearly requests A; contains exact intake, Style Gate, delivery, and handoff.
- `references/character-adapter.md`: read when creating both Usage Guides or routing Stage 2.
- `references/illustration-2d.md`: read only for `flat-2d` illustrations.
- `references/illustration-3d.md`: read only for `dimensional-3d` illustrations or long scrolls.
- `references/demo-mode.md`: read only when the user wants to preview Stage 2 without a confirmed character, Guide, photo, or style choice.
- `references/prompt-templates.md`: read only for Stage 1 image generation; contains the six style recipes and Guide prompts.
- `references/prompt-2d.md`: read only when generating `flat-2d` content illustrations.
- `references/prompt-3d.md`: read only when generating `dimensional-3d` content illustrations or long scrolls.
- `assets/style-reference-board.png`: mandatory style board when the user has not chosen a style.

## Direct Stage 2 Fast Path

Enter Stage 2 immediately when the user supplies content for illustration and either the current conversation already has a confirmed character or the user supplies an existing `usage-guide.md` plus one matching character image. If neither exists and the user wants to see Stage 2 first, use Demo Mode instead of sending them back to Stage 1.

- Skip Stage 1, profile questions, the Style Gate, Guide regeneration, and Guide summaries.
- In the same conversation, reuse the confirmed adapter and image. In a new conversation, require only `usage-guide.md` and `ip-standard-guide.png` (or a cleaner confirmed main-character image when available); `ip-usage-guide.png` is not needed for generation.
- Read only the `IP-ILLUSTRATION-FAST-PATH` block in `usage-guide.md`, the matching image, the routed 2D/3D reference, and the relevant image prompt. Read the rest of the Markdown only to diagnose drift or when the user asks.
- Resolve default sibling filenames automatically. Ask one concise question only if the adapter or matching image is missing, or if an adapter with `both` does not identify the current family.
- Use the requested image count. If omitted, infer a useful count from the content and default to 3 without reopening Stage 1.
- Before image calls, state the total count and that each image is standalone. Generate the full set in the same run unless the user explicitly asks to preview one first.

## Stage 2 Demo Mode

When the user chooses B or asks to preview B but has no confirmed IP, Guide, character image, photo, or style selection, read and follow `references/demo-mode.md`.

- Use the bundled Style 3 character at `assets/default-demo-character-style-3.png`; do not show the six-style gate or request a photo.
- Clearly label it as a temporary demonstration character, never as the user's personal IP.
- If content is supplied, illustrate it. If not, run the built-in three-image sample immediately so the user sees concrete output without another intake turn.
- After all images appear, send the demo handoff from `demo-mode.md` as a separate assistant message.

## Stage 1 — Build the IP

When the user chooses or clearly requests A, read and follow `references/stage-1.md`. Do not load it for direct Stage 2 work.

## Stage 2 — Illustrate content

1. Read the confirmed reference image and Illustration Adapter.
2. Route `flat-2d` to `illustration-2d.md`; route `dimensional-3d` to `illustration-3d.md`. For `both`, use the family explicitly selected by the user or current reference image; otherwise ask “这次用 2D 还是 3D？”
3. Do not convert between families without explicit approval. A requested conversion becomes a new main-character candidate that must be confirmed first.
4. Extract only high-value visual moments: a core judgment, conflict, transition, workflow break, state change, or story milestone. Translate each into one physical action and one visual metaphor.
5. If the user asks for ideas, return a shot list. If the user asks to generate, read only the matching `prompt-2d.md` or `prompt-3d.md`, plan internally, announce `共计划 N 张，将逐张生成独立图片`, and generate each image separately rather than as a collage.
6. Treat the first image as an **internal QA candidate**. Inspect identity, rendering family, action clarity, text, and density; revise it when needed, then continue the remaining images automatically. Pause after the first image only when the user requested preview-first or a material style/identity choice cannot be resolved safely. Do not make the user confirm a passing first image merely to receive the promised total.

The confirmed personal IP must perform the core action. Never replace it with a default mascot. Use only user-provided facts, names, projects, and numbers.
