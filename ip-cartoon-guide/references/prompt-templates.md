# Image Prompt Templates

Read only when generating images. Replace every `{variable}` with confirmed content. Always attach the matching character reference image.

## Six style recipes

Use the selected recipe verbatim as the base of `{exact_2d_or_3d_render_description}`, then add only confirmed user-specific anchors.

1. **粗线手绘 / flat-2d**: `Bold uneven hand-drawn black contours, visible line wobble, simple friendly facial features, mostly flat white fills, two or three sparse bright accents, little or no shading, playful notebook energy.`
2. **可爱卡通 / flat-2d**: `Clean rounded 2D cartoon linework, compact friendly proportions, flat pastel fills, small soft drawn shadows, bright readable expression, polished but not vector-corporate and not 3D.`
3. **3D软萌 / dimensional-3d**: `Soft-cute stylized 3D character with a larger rounded head, big gentle eyes, compact body, soft clay-like matte materials, pastel accents, diffused studio light, warm toy-like charm without glossy plastic.`
4. **清透线稿 / flat-2d**: `Fine clean graphite-and-ink line art, airy adult proportions, mostly white negative space, delicate facial detail, very light blue or pink annotations, minimal transparent wash, no solid 3D volume.`
5. **水彩手绘 / flat-2d**: `Hand-painted watercolor illustration with translucent layered washes, soft pigment blooms, gentle paper-edge variation inside the artwork, refined line accents, light adult proportions, and no 3D material or studio rendering.`
6. **职场轻熟 / dimensional-3d**: `Mature professional semi-realistic 3D character with natural adult eyes and proportions, restrained facial stylization, softly detailed hair, matte skin and fabric, subtle material realism, and warm editorial studio lighting; sophisticated, approachable, not chibi and not photoreal.`

## Stage 1 main-character candidate

```text
Create one polished personal-IP main-character candidate based on the same person in {photo_references}. Use the photos only as identity references, not as a background or layout to copy.

CONFIRMED IDENTITY
Preserve: hair {hair}; face and age impression {face}; skin {skin}; standard outfit {outfit}; signature accessories {accessories}; temperament {temperament}.

SELECTED STYLE
Style number and name: {selected_style_number_and_name}.
Rendering rules: {exact_2d_or_3d_render_description from the selected recipe above}.
Do not mix this style with any of the other five menu styles.

Menu family mapping: Styles 1, 2, 4, and 5 are flat 2D. Style 3 is soft-cute dimensional 3D. Style 6 is mature professional dimensional 3D with restrained realism. Styles 3 and 6 both route to 3D real-object scenes.

COMPOSITION
One character only, near-full-body or three-quarter body, clean uncluttered background, complete silhouette, one natural friendly action, personal-brand ready. Keep the face recognizable and the proportions attractive, mature, and consistent with the selected style.

AVOID
Identity drift, different hairstyle, outfit drift, accessory drift, age drift, generic stock-avatar face, copied famous character, extra people, malformed hands, extra fingers, real logo, watermark, dense text, poster layout, or any unselected rendering family.
```

## Stage 1 character standard poster

```text
Create `ip-standard-guide.png` as one polished portrait personal-IP character poster using the confirmed character in {reference_asset}.

IDENTITY LOCK
Preserve exactly: hair {hair}; face and adult age impression {face}; skin {skin}; standard outfit {outfit}; signature accessories {accessories}; temperament {temperament}. Use only {style_family_and_variant} with {render_rules} and {palette}.

VISUAL DIRECTION
Use a warm ivory paper background, soft beige glow, refined hand-made editorial spacing, thin understated dividers, small friendly line icons, and a premium personal-brand mood. The poster should feel like a curated character-design page, not a sterile software grid.

PORTRAIT LAYOUT
- Large title at upper left and one short positioning line.
- One dominant full-body hero character.
- Small front and side views near the hero.
- Two or three expression/action busts.
- Four compact lifestyle or work scenes where the same character performs useful actions.
- One small palette strip and a short signature footer.
Use varied scale and organic editorial rhythm while preserving clear hierarchy and whitespace.

TEXT
Render only the exact short labels supplied in {standard_guide_labels}. Do not invent facts or add paragraphs. If text reliability is weak, keep only the title and section labels; put all detail in `usage-guide.md`.

AVOID
Identity drift, family mixing, repeated mismatched faces, accessory-side errors, long text, tiny type, cold dashboard cards, dense technical infographic, random letters, logo, watermark, unrelated decoration, or copied outfits and props from layout references.
```

## Stage 1 visual Usage Guide poster

```text
Create `ip-usage-guide.png` as one polished portrait personal-IP color-and-theme reference poster using the confirmed character in {reference_asset}. This is the human-readable companion to `usage-guide.md`, not a replacement.

IDENTITY LOCK
Preserve exactly: hair {hair}; face and adult age impression {face}; skin {skin}; standard outfit {outfit}; signature accessories {accessories}; temperament {temperament}. Use only {style_family_and_variant} with {render_rules} and {palette}.

VISUAL DIRECTION
Match the standard poster as a coordinated two-page set: warm ivory paper, soft beige glow, rounded pale cards, gentle shadows, restrained icons, clean Chinese editorial typography, and generous whitespace. Keep it warm and personal, not clinical.

PORTRAIT LAYOUT
- Large title and one short positioning line at the top.
- One large waist-up approved portrait as the visual anchor.
- A vertical palette with color names or hex values.
- Three or four temperament keyword chips with small icons.
- A row of recommended props or objects.
- Five compact application thumbnails using the same character.
- Four concise style-trait cards.
- One short usage note across the bottom.
The page should be visually rich but easy to scan, with the character remaining dominant.

TEXT
Render only the exact short labels supplied in {usage_guide_labels}. Do not put the Stage 2 A/B handoff or other conversation guidance inside the image. Do not invent personal facts. Do not use long prompt text inside the image; `usage-guide.md` remains the AI-readable source of truth.

AVOID
Do/Don't audit layout, red-cross gallery, identity drift, family mixing, hairstyle or outfit changes, accessory-side errors, age drift, long paragraphs, tiny unreadable text, random letters, logo, watermark, cold dashboard styling, or unrelated decorative scenes.
```
