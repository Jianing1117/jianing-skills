# Jianing Skills

一套用于 [Claude Code](https://claude.ai/code) 的内容创作 Skill 合集，涵盖抖音/小红书内容创作全流程，以及微信公众号发布工具。

由加宁（[@Jianing1117](https://github.com/Jianing1117)）设计和维护，基于真实创作经验提炼的方法论。

---

## 包含的 Skill

### awesome-creator 系列 — 抖音/小红书内容创作全流程

按创作流程顺序使用，每个模块可独立触发，也可由主入口路由调用。

| Skill | 解决的问题 |
|-------|-----------|
| [awesome-creator](awesome-creator/) | 主入口，判断当前阶段并路由到对应模块 |
| [awesome-creator-positioning](awesome-creator-positioning/) | 从零确定内容定位——我是谁、做什么、给谁看 |
| [awesome-creator-title](awesome-creator-title/) | 标题优化，覆盖 9 种触发模式，生成 27+ 个候选 |
| [awesome-creator-hook](awesome-creator-hook/) | 前 3 秒开头设计，3 种方法生成 10-15 条候选 |
| [awesome-creator-content](awesome-creator-content/) | 正文结构诊断 + 五种互动钩子设计（完播/点赞/收藏/转发/评论） |
| [awesome-creator-cover](awesome-creator-cover/) | 封面设计入口，根据内容类型路由到对应风格 |
| [awesome-creator-cover-whiteboard](awesome-creator-cover-whiteboard/) | 白板风格封面，输出 `.excalidraw` 文件 |

**创作流程**：定位 → 标题 → 开头 → 正文设计 → 封面

---

### 独立工具

| Skill | 用途 |
|-------|------|
| [wechat-formatter](wechat-formatter/) | 微信公众号排版（Markdown → 内联 HTML）+ 封面图生成（900×383px PNG） |

---

## 安装方法

将需要的 skill 目录复制到你的 Claude Code skills 文件夹：

```bash
# 克隆仓库
git clone https://github.com/Jianing1117/jianing-skills.git

# 复制到 Claude Code 用户级 skills 目录
cp -r jianing-skills/awesome-creator* ~/.claude/skills/
cp -r jianing-skills/wechat-formatter ~/.claude/skills/

# 清理
rm -rf jianing-skills
```

安装后重启 Claude Code 即可使用。

> 如果你想把 skills 目录直接作为 git 仓库管理（如本仓库的方式），可以直接在 `~/.claude/skills/` 下 `git init` 并添加这些文件，使用 `.gitignore` 控制提交范围。

---

## 使用方式

### 从头开始做内容

```
/awesome-creator
```

或者直接描述你的情况，Claude 会路由到对应模块：
- "我想在小红书做内容，不知道做什么方向" → 定位模块
- "帮我优化这个标题" → 标题模块
- "这个开头怎么改能让人看完" → 开头模块
- "帮我把这篇脚本加上互动钩子" → 正文设计模块

### 发微信公众号

```
/wechat-formatter
```

把 Markdown 文章粘贴进来，自动生成：
- 可一键复制到公众号编辑器的内联 HTML
- 配套封面图（900×383px，符合微信标准比例）

---

## 设计理念

详见 [awesome-creator/references/philosophy.md](awesome-creator/references/philosophy.md)

核心一句话：**好内容是人与人之间的连接，不是对算法的讨好。**

这套工具不帮你"生成内容"——它帮你把自己的想法变成有效表达。你是主体，AI 是工具。

---

## 依赖说明

`wechat-formatter` 的封面生成需要额外安装：

```bash
pip3 install playwright pillow
python3 -m playwright install chromium
```

其他 skill 无外部依赖。

---

## 版本记录

- **2026-05** — 初始版本：awesome-creator 完整系列 + wechat-formatter
