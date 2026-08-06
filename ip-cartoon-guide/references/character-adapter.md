# Character Adapter

Use this file only to create `ip-usage-guide.png`, write `usage-guide.md`, or route Stage 2. The Markdown adapter is the detailed source of truth; the visual Guide presents the same rules in a concise human-readable form.

## Families

| Family | Use for |
| --- | --- |
| `flat-2d` | Styles 1, 2, 4, 5: rough line, flat cartoon, clean line art, watercolor |
| `dimensional-3d` | Styles 3 and 6: soft-cute 3D, or mature professional light-realistic 3D |
| `both` | Two separately confirmed 2D and 3D characters |

Style 3 is rounder and softer; Style 6 is more mature, professional, and restrained. Both route to 3D real-object scenes. Judge custom styles from the confirmed image: drawn shading stays 2D; physical volume, material, and contact light mean 3D.

## Fast Path placement

Put the adapter near the top of `usage-guide.md` between these exact markers so Stage 2 can extract only this block:

```text
<!-- IP-ILLUSTRATION-FAST-PATH:START -->
...adapter YAML only...
<!-- IP-ILLUSTRATION-FAST-PATH:END -->
```

Keep the marked block concise: one routed reference asset, compressed identity/render anchors, palette, preserve, and avoid. Do not repeat prose or full prompts inside it.

## Required adapter

Write concrete values and omit unused render fields.

```yaml
illustration_adapter:
  style_family: flat-2d | dimensional-3d | both
  default_variant: approved variant
  reference_assets:
    flat_2d: path or null
    dimensional_3d: path or null
  identity:
    hair: stable silhouette and color
    face: stable face, eyes, expression, age impression
    skin: skin direction
    outfit: standard outfit
    accessories: signature accessories
    temperament: core temperament
  palette: primary, secondary, accents, background
  render:
    flat_2d: line, fill, shading
    dimensional_3d: material, light, proportions
  preserve: [non-negotiable anchors]
  avoid: [identity and style drift]
```

## Routing rules

- Attach the matching reference image when generating; text alone is insufficient for identity.
- For a portable three-file delivery, point the Fast Path to `ip-standard-guide.png`. Prefer a separate clean confirmed main-character image only when it is also available to the next model.
- For `both`, route from the user's current choice or reference image. Ask once if neither identifies the family.
- Never inflate 2D into 3D or flatten 3D into 2D silently.
- Reject output when the family is correct but the person, hair, outfit, or accessories drift.
