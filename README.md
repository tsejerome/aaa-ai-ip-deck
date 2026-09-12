# AAA 個人品牌 AI 講座 — web slide deck

Open `deck.html` directly in a browser. Images and animations are self-contained.

The original 36-slide design (now 35 after removing the Step 2 Research slide), content, illustrations, poster, colors, layouts,
and controls are preserved. Motion enhancements animate the existing visuals:
- Staggered slide entrances that replay when revisiting slides.
- Gentle image and icon entrances, including the original cover poster.
- Growth-chart curves drawing in sequence and mind-map branches drawing outward.
- Staggered cards, calendar cells, format tiles, and chapter numbers.
- Reduced-motion support; offscreen animations are cancelled.

Selected 3D enhancements (original content retained):
- Slide 1: original poster styled as a raised card, automatically floating and tilting in a continuous 10-second loop while visible.
- Slide 11: rotating fine gold-wire donut.
- Slide 16: floating 6×5 gold-wire lattice matching the donut.
- Slide 18: gold contour outlines, flowing connections, and perspective movement on the original mind map and format cards.
- Slide 25: dimensional camera with a modeled lens.
- Slide 27: larger folded paper plane with distinct wings and fold lines, viewed from above for a recognizable silhouette.

The four canvas scenes use inline 3D geometry and perspective projection,
respond to the pointer, pause offscreen, and respect reduced motion.

Use arrows / Page Up / Page Down / Space to navigate, Home / End to jump,
and click existing image previews to enlarge. Escape closes image previews.

Files:
- `deck_template.html`: editable source (CSS, slides, JavaScript, image tokens).
- `assets/`: image assets; token mapping lives in `assemble.py`.
- `assemble.py`: embeds the assets and writes `deck.html`.
- `original/`: untouched original HTML and source template.
- `source/`: original presentation and supporting materials.

Build: `python3 assemble.py`.

Validation: script syntax, original markup/content/visual preservation,
original CSS preservation, resolved asset tokens, and 3D geometry checked.
Confirmed that all original text, images and 36 slides are retained. Browser visual
verification remains pending because the required gstack `/browse` skill was
not available locally.
