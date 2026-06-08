---
name: comic-production
description: "Generate educational comic strips in 混知漫画 (Hunzhi Comics) style using AI image generation and PIL assembly. Produces long-form vertical comics with illustrated panels and text bands. Use when the user wants to create educational comics, 科普漫画, knowledge comics, 混知风格 content, or illustrated explainers on any topic (AI, finance, history, science, etc.)."
---

# Comic Production Pipeline (混知风格科普漫画)

Generate educational comic strips: AI generates each panel independently → PIL assembles into a long-form vertical comic with text bands.

## Pipeline Overview

```
1. Plan panels  →  2. Generate images  →  3. Assemble comic  →  4. (Optional) Make video
```

## Step 1: Plan Panels

Define 6-10 panels for the topic. Each panel needs:

```python
PANELS = [
    {"title": "以物易物", "description": "简短描述文字……", "scene_prompt": "English scene description for ImageGen..."},
    # ... more panels
]
```

**Panel count guide:**
- Simple topic: 6 panels
- Standard topic: 8 panels (recommended)
- Deep dive: 10 panels

**Title guidelines:** 2-4 Chinese characters, concise stage/phase name.

**Writing guidelines (STORYTELLING STYLE — critical for 混知 feel!):**

Each panel uses `lines` array (recommended) for multi-line story text.

**混知写作五原则：**
1. 用类比和比喻，不用教科书定义
2. 像在给朋友讲故事，不像在上课
3. 创造小场景："假设全村100人，每人发100块……"
4. 用幽默、反问、戏剧性对比
5. 最后一句 = 金句/punchline，让人记住

**Good example:**
```json
{
  "title": "什么是通胀",
  "lines": [
    "假设全村100人，每人发100块",
    "可村里只有一头牛……你猜牛能卖多少钱？",
    "钱多了，东西没多 = 通胀"
  ]
}
```

**Bad example (AVOID):**
```json
{"title": "什么是通胀", "description": "货币供应量超过商品供应量导致物价上涨"}
```

## Step 2: Generate Panel Images

Use `ImageGen` tool for each panel with these parameters:

- **Size:** `1024x768` (landscape, 4:3)
- **Style prompt template:**

```
A single-panel Chinese educational comic in the style of 混知漫画 (Hunzhi Comics).
Scene: [SCENE DESCRIPTION HERE].
[CHARACTER_A]'s speech bubble: "[中文对话A]".
[CHARACTER_B]'s speech bubble: "[中文对话B]".
Simple cartoon style with bold black outlines, flat bright colors, minimal background.
Exaggerated humorous facial expressions, big heads and small bodies.
Chinese speech bubbles with dialogue are essential.
Self-contained single scene, clean composition.
```

**Critical rules:**
- **Always include Chinese speech bubbles** in the prompt — characters should have dialogue to make scenes lively
- Speech bubble text should be conversational, funny, in-character
- Generate panels in parallel batches of 4 for speed
- Each panel must be a complete, self-contained scene
- AI-generated images may contain "Qoder AI 生成" watermark in bottom-right — this is auto-removed by the assembly script

**Speech bubble example prompts:**
```
Shopkeeper's speech bubble: "东西涨价了呗！"
Customer's speech bubble: "我的钱怎么不够花了？"
Official's speech bubble: "缺钱？印就完事了！"
Economist's speech bubble: "你印的不是钱，是未来的物价啊！"
```

## Step 3: Assemble Comic

Run the assembly script: `python3 scripts/assemble.py`

The script takes a JSON config and produces a long-form vertical image:

```bash
python3 scripts/assemble.py \
  --title "什么是货币？" \
  --subtitle "从以物易物到数字货币" \
  --panels panels.json \
  --output comic.png
```

### panels.json format

```json
[
  {
    "image": "/path/to/panel_1.png",
    "title": "以物易物",
    "lines": [
      "我想拿鸡换你的鞋，可你想要粮食",
      "双方都得需要对方的东西，这买卖才能成",
      "需求必须双向匹配——太难了吧！"
    ]
  }
]
```

### Assembly layout

```
┌─────────────────────────────┐
│        Title Area           │
├─────────────────────────────┤
│                             │
│     Panel 1 Image           │  ← AI watermark auto-removed
│                             │
├─────────────────────────────┤
│ ① 标题                      │  ← Dark text band (dynamic height)
│ 故事线1……                   │
│ 故事线2……                   │
│ 金句/punchline……            │
├─────────────────────────────┤
│                             │
│     Panel 2 Image           │
│                             │
├─────────────────────────────┤
│ ② 标题                      │
│ 故事线1……                   │
│          ...                │
└─────────────────────────────┘
  (no footer watermark)
```

**Key design principles:**
- Images are NEVER cropped — text is on separate bands below
- AI watermark ("Qoder AI 生成") auto-removed from each panel's bottom-right corner
- Text band height is dynamic (auto-expands for multi-line `lines` content)
- Numbered yellow badge for each panel
- No footer attribution — clean output
- Width: 1080px (mobile-friendly)

### Assembly config parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--width` | 1080 | Output image width |
| `--padding` | 40 | Horizontal margin (px) |
| `--text-band-h` | 95 | Text band height (px) |
| `--title-h` | 180 | Title area height (px) |
| `--gap` | 10 | Gap between elements (px) |
| `--output-jpg` | flag | Also export JPG version |

## Step 4: Optional Video

To convert the comic into a short video, use the `educational-video-production` skill. The comic panels become visual frames with Ken Burns effects, TTS narration, and subtitles.

## Color Scheme

| Element | Color | Hex |
|---------|-------|-----|
| Background | Light gray | `(245, 245, 245)` |
| Text band | Dark navy | `(35, 40, 55)` |
| Title text | Red | `(230, 60, 60)` |
| Panel title | Yellow | `(250, 200, 30)` |
| Description | Light gray | `(200, 200, 200)` |
| Number badge | Yellow bg + dark text | - |

## Dependencies

```bash
pip install Pillow
```

macOS fonts: `STHeiti Medium.ttc` (bold), `STHeiti Light.ttc` (regular).

## Example Workflow

User: "帮我做一个关于通货膨胀的科普漫画"

1. Plan 8 panels with storytelling `lines` (3 lines each: scene → conflict → punchline)
2. Generate 8 images via ImageGen (2 batches of 4), each prompt includes Chinese speech bubbles
3. Create panels.json with `lines` arrays (storytelling text)
4. Run `scripts/assemble.py` — auto-removes AI watermarks, dynamic text bands, no footer
5. Resize to 720px wide for WeChat sharing
6. Send to user

## Troubleshooting

- **Panels look inconsistent in style:** Re-generate with more specific style keywords. Add "same art style as previous panels" to prompt.
- **Text too long for band:** Keep descriptions under 40 Chinese characters.
- **Image too tall for sharing:** The script auto-exports a JPG version. For WeChat, resize to 720px wide.
