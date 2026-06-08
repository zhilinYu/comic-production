<p align="center">
  <a href="README.md">English</a> | <strong>中文</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/zhilinYu/comic-production" alt="License">
  <img src="https://img.shields.io/badge/python-3.8+-green" alt="Python">
  <img src="https://img.shields.io/badge/skill-AI%20Agent-blue" alt="Skill">
</p>

# 科普漫画生产流水线

> 用 AI 生图 + PIL 拼装，生成**混知漫画风格**的科普长图漫画——带故事线文字条的竖版长图，适合微信朋友圈、公众号分享。

## 示例作品

<p float="left" align="center">
  <img src="examples/example_money.jpg" width="30%" alt="什么是货币">
  <img src="examples/example_inflation.jpg" width="30%" alt="什么是通胀">
  <img src="examples/example_kline.jpg" width="30%" alt="什么是K线">
</p>

<p align="center"><em>左：什么是货币 &nbsp;|&nbsp; 中：什么是通胀 &nbsp;|&nbsp; 右：什么是K线</em></p>

## 快速开始

```bash
# 安装为 AI 智能体 Skill（Claude Code / QoderWork / Cursor）
cp -r . ~/.qoderwork/skills/comic-production   # QoderWork
cp -r . .claude/skills/comic-production         # Claude Code（项目级）

# 或者只安装 Python 依赖
pip install Pillow
```

然后对你的 AI 助手说：

> "帮我做一个关于通货膨胀的科普漫画"

## 这是什么？

这个项目既是一个**独立的 Python 工具**，也是一个 **AI 智能体 Skill**，用于制作中文科普漫画。它实现了 4 步流水线：

```
1. 规划面板  →  2. AI 生成图片  →  3. PIL 拼装漫画  →  4.（可选）制作视频
```

每一格漫画由 AI 图像生成器（DALL-E、Midjourney 等）独立生成，然后通过内置的 PIL 脚本拼装成精美的竖版长图漫画。输出针对手机端分享优化（微信、社交媒体）。

**核心特性：**

- 自动去除 AI 生成图片的水印
- 动态文字条——根据内容长度自动扩展高度
- 混知风格故事线（场景 → 冲突 → 金句）
- 1080px 宽度，手机端友好
- 图片不裁剪——文字放在独立的深色文字条上

## 安装

### 作为 AI 智能体 Skill

| 平台 | 安装方式 |
|------|---------|
| **QoderWork** | `cp -r . ~/.qoderwork/skills/comic-production` |
| **Claude Code**（全局） | `cp -r . ~/.claude/skills/comic-production` |
| **Claude Code**（项目级） | `cp -r . .claude/skills/comic-production` |
| **Cursor** | 把 `SKILL.md` 复制到 `.cursor/rules/comic-production.mdc` |

### 作为独立 Python 工具

```bash
pip install Pillow
python3 scripts/assemble.py --help
```

**字体要求：** 脚本在 macOS 上自动检测中文字体（华文黑体、苹方、宋体、冬青黑体）。Linux/Windows 用户需安装任意中文字体并修改 `assemble.py` 中的 `find_font()` 函数。

## 使用方式

### 配合 AI 智能体

安装为 Skill 后，当你要求制作科普漫画时，智能体会自动激活此技能。试试：

```
"帮我做一个关于量子力学的科普漫画"
"用混知风格画一个讲股票K线的漫画"
"做一个区块链科普漫画，8格，发到微信群里"
```

### 独立使用（手动流水线）

**第一步：** 用任意 AI 图像生成器生成面板图片，使用以下提示词模板：

```
A single-panel Chinese educational comic in the style of Hunzhi Comics.
Scene: [你的场景描述]。
Character A's speech bubble: "中文对话".
Simple cartoon style with bold black outlines, flat bright colors, minimal background.
Exaggerated humorous facial expressions, big heads and small bodies.
```

推荐尺寸：1024×768（横版，4:3）。

**第二步：** 创建 `panels.json`：

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
  }
]
```

**第三步：** 拼装：

```bash
python3 scripts/assemble.py \
  --title "什么是货币？" \
  --subtitle "从以物易物到数字货币" \
  --panels panels.json \
  --output comic.png \
  --output-jpg
```

### 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--width` | 1080 | 输出宽度（像素） |
| `--padding` | 40 | 左右边距（像素） |
| `--text-band-h` | 95 | 文字条最小高度（像素） |
| `--title-h` | 180 | 标题区高度（像素） |
| `--gap` | 10 | 元素间距（像素） |
| `--output-jpg` | 关闭 | 同时导出 JPG 版本 |

## Skill 工作原理

Skill 是一个包含 `SKILL.md` 文件的文件夹，用来指导 AI 编码智能体执行特定任务：

```
comic-production/
├── SKILL.md              # 智能体指令（YAML 前言 + Markdown 正文）
├── scripts/
│   └── assemble.py       # PIL 漫画拼装脚本
├── examples/             # 示例输出
├── README.md
└── LICENSE
```

`SKILL.md` 的前言（frontmatter）告诉智能体何时激活此技能：

```yaml
---
name: comic-production
description: "Generate educational comic strips in 混知漫画 style...
  Use when the user wants to create educational comics, 科普漫画,
  knowledge comics, or illustrated explainers."
---
```

## 项目结构

```
comic-production/
├── SKILL.md                 # AI 智能体技能定义
├── scripts/
│   └── assemble.py          # 基于 PIL 的漫画拼装（249 行）
├── examples/
│   ├── example_money.jpg    # 什么是货币
│   ├── example_inflation.jpg# 什么是通胀
│   └── example_kline.jpg    # 什么是K线
├── README.md                # English documentation
├── README.zh-CN.md          # 中文文档
├── LICENSE                  # MIT
└── .gitignore
```

## 混知写作五原则

科普漫画的灵魂是**讲故事**，而不是搬教科书：

1. **用类比和比喻**——不用教科书定义
2. **像给朋友讲故事**——不像在上课
3. **创造小场景**——"假设全村100人，每人发100块……"
4. **用幽默、反问、戏剧性对比**
5. **最后一句 = 金句/punchline**——让人记住

**好的写法：**

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

**不好的写法（避免）：**

```json
{"title": "什么是通胀", "description": "货币供应量超过商品供应量导致物价上涨"}
```

## 设计规范

### 版面布局

```
┌─────────────────────────────┐
│          标题区              │
├─────────────────────────────┤
│     第1格漫画图片            │  ← AI 生成，自动去水印
├─────────────────────────────┤
│ ① 面板标题（黄色）           │  ← 深色文字条（高度自适应）
│ 故事线1……                   │
│ 故事线2……                   │
│ 金句/punchline……            │
├─────────────────────────────┤
│     第2格漫画图片            │
├─────────────────────────────┤
│ ② 面板标题                   │
│ 故事线……                    │
└─────────────────────────────┘
```

### 配色方案

| 元素 | 色值 | 预览 |
|------|------|------|
| 背景 | `#F5F5F5` | 🟫 |
| 文字条 | `#232837` | ⬛ |
| 标题文字 | `#E63C3C` | 🟥 |
| 面板标题 | `#FAC81E` | 🟨 |
| 正文文字 | `#C8C8C8` | 🔘 |

### 面板数量参考

| 主题深度 | 面板数 |
|---------|--------|
| 简单主题 | 6 格 |
| 标准主题 | 8 格（推荐） |
| 深度解析 | 10 格 |

## 参与贡献

欢迎贡献！你可以：

- 添加更多中文字体支持（Linux/Windows）
- 改进水印去除算法
- 添加新的布局模板（横版、九宫格等）
- 翻译故事线写作指南到其他语言

## 开源协议

[MIT](LICENSE) —— 个人和商业使用免费。
