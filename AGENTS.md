# crrc-operators — 项目说明文档

> 本文件供 Cursor、Codex、Claude Code 等执行型 Agent 读取。
> Hermes 负责在项目进展时更新本文件。
>
> **⚡ 启动顺序**：请按以下顺序读取，避免全盘扫描：
> 1. **本文件** — 项目架构、约定、技术栈
> 2. **`.hermes/plan/SETUP.md`** — 环境踩坑经验（WSL 配置、命令差异等）
> 3. **`.hermes/plan/STATUS.md`** — 当前进度、阶段、下一步（30 秒了解全貌）
> 4. `.hermes/session-log.md` — 最近工作细节（按需）
>
> **📋 环境信息**：详见 [workspace/ENVIRONMENTS.md](../ENVIRONMENTS.md#4-crrc-operators)
> - Python · `.venv/` ✅ 已就绪（opencv/numpy/pandas）
> - 激活：`.venv/bin/python` 或 `source .venv/bin/activate`
> - 关键依赖：opencv-python, numpy, pandas
>
> **🌐 语言规范**：代码注释、文档、commit message 一律中文。详见 [workspace/AGENTS.md](../AGENTS.md)

---

## 项目概述

中车算子对接项目，以文档和接口对接为主。

**负责人**：sakuya
**协调 Agent**：Hermes

---

## 与 Hermes 的通信机制

本项目使用 `.hermes/` 目录进行多 Agent 协调：

| 文件 | 谁写 | 谁读 | 用途 |
|------|------|------|------|
| `.hermes/plan/STATUS.md` | 任何 Agent | 任何 Agent | **进度快照**（覆盖式）：当前阶段、最近完成、正在进行 |
| `.hermes/plan/board.md` | Dev/Test Agent | Dev/Test Agent | **协调面板**：任务看板 + 测试报告 + 交接留言 |
| `.hermes/plan/daily/YYYY-MM-DD.md` | 任何 Agent | sakuya/Hermes | **每日日志**（追加式）：当天工作内容 |
| `.hermes/session-log.md` | 任何 Agent | Hermes | 每次会话简要摘要 |
| `.hermes/handoff.md` | 任何 Agent | Hermes | 需要 Hermes 处理的事项 |
| `.hermes/bulletin.md` | Hermes | 任何 Agent | 优先级和状态变更广播 |

**Agent 启动顺序**：AGENTS.md → STATUS.md → board.md → 开工
**每日结束**：追加 daily/YYYY-MM-DD.md + session-log.md
**阶段完成**：更新 STATUS.md → 在 board.md 留言给对端 Agent

**请每次会话结束后追加一条 session-log**，格式：
```
## 2026-04-28 15:30 | Cursor
- 改动：文件路径
- 结果：简要结果
- 需要Hermes：无 / 具体事项
```

---

## 📚 Skill 支持（2026-05-17 新增）

本项目 Agent（Cursor/Codex）可以加载 workspace 共享的 skill 库。

### 如何使用

```
1. read_file ~/workspace/.hermes/skills/SKILLS_INDEX.md   ← 先看索引，找需要的 skill
2. read_file <索引用列出的路径>                              ← 加载 skill 正文
3. 按 skill 中的步骤执行
```

### 本项目的推荐 Skill

| 场景 | Skill | 路径 |
|------|-------|------|
| 汇报项目状态 | project-briefing | `~/.hermes/skills/project-briefing/SKILL.md` |
| 更新项目文档 | project-audit-agents-update | `~/.hermes/skills/project-audit-agents-update/SKILL.md` |
| TDD 开发 | test-driven-development | `~/.hermes/skills/software-development/test-driven-development/SKILL.md` |
| Bug 调试 | systematic-debugging | `~/.hermes/skills/software-development/systematic-debugging/SKILL.md` |
| Python 调试 | python-debugpy | `~/.hermes/skills/software-development/python-debugpy/SKILL.md` |

> 完整索引见 `~/workspace/.hermes/skills/SKILLS_INDEX.md`
