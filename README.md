# Jianing Skills

Jianing 的公开 Skill 合集仓库。每个一级目录都是可独立安装、独立触发的 Skill；合集仓库只负责统一发现、安装和版本管理，不把所有能力塞进一个巨型 `SKILL.md`。

由加宁（[@Jianing1117](https://github.com/Jianing1117)）设计和维护，支持 Codex、Claude Code 及其他能读取 `SKILL.md` 的 Agent 环境。

## Skill 目录

### 内容创作流程

| Skill | 用途 |
|---|---|
| [awesome-creator](awesome-creator/) | 主入口，判断当前创作阶段并路由 |
| [awesome-creator-positioning](awesome-creator-positioning/) | 从零确定内容定位 |
| [awesome-creator-title](awesome-creator-title/) | 标题优化与候选生成 |
| [awesome-creator-hook](awesome-creator-hook/) | 设计前 3 秒内容开头（不是系统生命周期 Hook） |
| [awesome-creator-content](awesome-creator-content/) | 正文结构诊断与互动设计 |
| [awesome-creator-cover](awesome-creator-cover/) | 白板风格封面设计，内置可编辑 Excalidraw 生成脚本 |

**创作流程**：定位 → 标题 → 开头 → 正文设计 → 封面

### 视觉、演示与发布

| Skill | 用途 |
|---|---|
| [ip-cartoon-guide](ip-cartoon-guide/) | 从照片建立可复用个人 IP，并延伸到同角色内容插图 |
| [super-slides](super-slides/) | 生成 HTML 互动演示稿，可选导出 PDF/PPT 或部署 |
| [wechat-formatter](wechat-formatter/) | 微信公众号排版与封面生成 |

### 自我认知

| Skill | 用途 |
|---|---|
| [mindmirror](mindmirror/) | 基于明确授权的真实语料，进行证据导向的自我画像、数字分身与人生路径推演 |

`mindmirror` 会处理高度个人化材料，必须先确认阅读范围与是否落盘；凭证、证件、银行资料和私钥等永不读取。

## 安装

先克隆合集：

```bash
git clone https://github.com/Jianing1117/jianing-skills.git
cd jianing-skills
```

然后只复制需要的 Skill 目录。例如安装 `mindmirror`：

```bash
# Codex
cp -R mindmirror "${CODEX_HOME:-$HOME/.codex}/skills/"

# Claude Code
cp -R mindmirror "$HOME/.claude/skills/"
```

要安装其他 Skill，把命令中的 `mindmirror` 换成对应目录名即可。安装后刷新或重启 Agent 客户端。

## 依赖与边界

- `mindmirror`：纯 Markdown，无代码依赖。
- `ip-cartoon-guide`：需要 Agent 具备图像生成/编辑能力。
- `awesome-creator-cover`：内置脚本需 Python 3；输出为 `.excalidraw`。
- `super-slides`：生成 HTML 无强制依赖；PDF 导出和在线部署需 Node.js 及相应 CLI，PPTX 抽取助手另需 `python-pptx`。只有在用户明确选择部署后才发布到外部服务。
- `wechat-formatter`：封面生成需 `playwright` 和 `Pillow`。

## 迁移来源

2026-08-06 将以下独立仓库的主 Skill 包并入本合集。单文件兼容副本、测试报告和仓库级安装文档不重复并入。

| Skill | 原始仓库 | 迁移基线 |
|---|---|---|
| mindmirror | [Jianing1117/mindmirror](https://github.com/Jianing1117/mindmirror) | [`56fc5e3`](https://github.com/Jianing1117/mindmirror/commit/56fc5e3e7fa2fa5f31d7afad8b67acf59de87e71) |
| ip-cartoon-guide | [Jianing1117/ip-cartoon-guide](https://github.com/Jianing1117/ip-cartoon-guide) | [`8bc97fc`](https://github.com/Jianing1117/ip-cartoon-guide/commit/8bc97fc4671c5398968b5702ea8ee74ece67f997) |
| super-slides | [Jianing1117/super-slides](https://github.com/Jianing1117/super-slides) | [`1e1dc44`](https://github.com/Jianing1117/super-slides/commit/1e1dc443c6c7e39acfcc1da8a255e6ed52049e8e) |

## 设计理念

`awesome-creator` 系列的方法论详见 [philosophy.md](awesome-creator/references/philosophy.md)。核心是：**好内容是人与人之间的连接，不是对算法的讨好。**

## 许可说明

各 Skill 保留自身的许可或第三方声明，例如 `mindmirror/LICENSE` 与 `ip-cartoon-guide/NOTICE.md`。本合集目前没有统一的根许可证，不应将某个子 Skill 的许可自动视为整个仓库的许可。

## 版本记录

- **2026-08** — 并入 `mindmirror`、`ip-cartoon-guide` 和 `super-slides`；将 `awesome-creator-cover` 改为无外部 Skill 依赖的可编辑封面生成器
- **2026-08** — 合并冗余封面子路由；移除已有公开文档和脚本中的个人本地路径
- **2026-05** — 初始版本：`awesome-creator` 系列与 `wechat-formatter`
