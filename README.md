# Comic Production Pipeline

Generate educational comic strips in the style of **Hunzhi Comics (混知漫画)** using AI image generation + PIL assembly. Produces long-form vertical comics with illustrated panels and storytelling text bands.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)

## What It Does

This tool implements a 4-step pipeline for creating Chinese educational comics (科普漫画):

```
1. Plan panels  →  2. Generate images (AI)  →  3. Assemble comic (PIL)  →  4. (Optional) Make video
```

Each panel is generated independently by an AI image generator, then assembled into a polished long-form vertical comic using the included Python script.

## Features

- **Hunzhi-style storytelling** — Each panel uses 3-line story text (scene → conflict → punchline)
- **Auto watermark removal** — Strips AI-generated watermarks from panel images
- **Dynamic text bands** — Text band height auto-adjusts based on content length
- **Mobile-friendly output** — 1080px wide, optimized for WeChat/social sharing
- **No image cropping** — Full panel images with text on separate bands below

## Layout

```
┌─────────────────────────────┐
│        Title Area           │
├─────────────────────────────┤
│                             │
│     Panel 1 Image           │  ← AI-generated, watermark auto-removed
│                             │
├─────────────────────────────┤
│ ① Panel Title (yellow)      │  ← Dark text band (dynamic height)
│ Story line 1...             │
│ Story line 2...             │
│ Punchline...                │
├─────────────────────────────┤
│                             │
│     Panel 2 Image           │
│                             │
├─────────────────────────────┤
│ ② Panel Title               │
│ Story lines...              │
└─────────────────────────────┘
```

## Installation

```bash
pip install Pillow
```

**Font requirements:** The script looks for CJK fonts in this order:
1. `STHeiti Medium.ttc` / `STHeiti Light.ttc` (macOS default)
2. `PingFang.ttc`
3. `Songti.ttc`
4. `Hiragino Sans GB.ttc`

On Linux/Windows, install any CJK font and update the `find_font()` function.

## Quick Start

### 1. Prepare Panel Images

Generate panel images using any AI image generator (DALL-E, Midjourney, Stable Diffusion, etc.) with this prompt template:

```
A single-panel Chinese educational comic in the style of Hunzhi Comics.
Scene: [YOUR SCENE DESCRIPTION].
Character A's speech bubble: "中文对话A".
Character B's speech bubble: "中文对话B".
Simple cartoon style with bold black outlines, flat bright colors, minimal background.
Exaggerated humorous facial expressions, big heads and small bodies.
Chinese speech bubbles with dialogue are essential.
```

**Recommended size:** 1024x768 (landscape, 4:3)

### 2. Create panels.json

```json
[
  {
    "image": "panels/panel_1.png",
    "title": "以物易物",
    "lines": [
      "我想拿鸡换你的鞋，可你想要粮食",
      "双方都得需要对方的东西，这买卖才能成",
      "需求必须双向匹配——太难了吧！"
    ]
  },
  {
    "image": "panels/panel_2.png",
    "title": "一般等价物",
    "lines": [
      "后来大家发现，盐谁都想要",
      "于是盐变成了'万能货币'",
      "这就是'一般等价物'的由来"
    ]
  }
]
```

Each panel uses:
- `image`: Path to the generated panel image
- `title`: 2-4 Chinese characters, concise stage/phase name
- `lines`: Array of story text (recommended 3 lines: scene → conflict → punchline)

### 3. Assemble the Comic

```bash
python3 scripts/assemble.py \
  --title "什么是货币？" \
  --subtitle "从以物易物到数字货币" \
  --panels panels.json \
  --output comic.png \
  --output-jpg
```

**Options:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--width` | 1080 | Output image width (px) |
| `--padding` | 40 | Horizontal margin (px) |
| `--text-band-h` | 95 | Minimum text band height (px) |
| `--title-h` | 180 | Title area height (px) |
| `--gap` | 10 | Gap between elements (px) |
| `--output-jpg` | flag | Also export JPG version |

## Writing Guidelines (混知写作五原则)

The key to great educational comics is **storytelling**, not textbook definitions:

1. **Use analogies and metaphors** — Don't quote textbook definitions
2. **Tell it like a story to a friend** — Not like a lecture
3. **Create mini-scenes** — "Imagine a village of 100 people, each given 100 yuan..."
4. **Use humor, rhetorical questions, dramatic contrast**
5. **Last line = golden quote/punchline** — Make it memorable

### Good Example

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

### Bad Example (Avoid)

```json
{
  "title": "什么是通胀",
  "description": "货币供应量超过商品供应量导致物价上涨"
}
```

## Color Scheme

| Element | Color | Hex |
|---------|-------|-----|
| Background | Light gray | `(245, 245, 245)` |
| Text band | Dark navy | `(35, 40, 55)` |
| Title text | Red | `(230, 60, 60)` |
| Panel title | Yellow | `(250, 200, 30)` |
| Description | Light gray | `(200, 200, 200)` |
| Number badge | Yellow bg + dark text | — |

## Programmatic Usage

You can also use the assembly function in your own Python code:

```python
from scripts.assemble import assemble

assemble(
    panels_data=[
        {"image": "panel_1.png", "title": "第一步", "lines": ["...", "...", "..."]},
        {"image": "panel_2.png", "title": "第二步", "lines": ["...", "...", "..."]},
    ],
    title="我的科普漫画",
    subtitle="一个有趣的故事",
    output_path="my_comic.png",
)
```

## Panel Count Guide

| Topic Depth | Panels |
|-------------|--------|
| Simple topic | 6 |
| Standard topic | 8 (recommended) |
| Deep dive | 10 |

## Use with AI Agents

This tool was originally designed as a **Skill** for AI coding agents (Claude Code, QoderWork, etc.). The `SKILL.md` file contains the full agent instructions. You can install it as a skill in any compatible AI agent framework.

## Troubleshooting

- **Panels look inconsistent in style:** Re-generate with more specific style keywords. Add "same art style as previous panels" to prompt.
- **Text too long for band:** Keep lines under 40 Chinese characters each.
- **CJK fonts not rendering:** Install a CJK font and update `find_font()` in `assemble.py`.
- **Image too tall for sharing:** Use `--width 720` for WeChat-friendly output.

## License

MIT License. See [LICENSE](LICENSE) for details.
