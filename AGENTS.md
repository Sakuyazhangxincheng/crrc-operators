# crrc-operators — 项目说明文档

> 🖥️ **运行环境**：WSL (Ubuntu)。文档中所有 `~/` 和 `~/.hermes/` 一律指 `/home/sakuya/...`，不是 Windows `$HOME`。
> 本文件供执行型 Agent（Cursor / Codex / Claude Code）读取。Hermes 负责更新。


## 🖥️ 运行环境

> Python 和所有依赖在 WSL Ubuntu 内。详细环境信息见项目根目录的 `ENVIRONMENT.md`。


## 🚨 启动硬检查（新窗口必执行，不可跳过）

按顺序逐项执行，任何一步失败就停止并报告：

```
1. 读取本文件（你正在读）
2. 读取 .hermes/plan/STATUS.md（30 秒了解当前进度）
3. 读取 \\wsl.localhost\Ubuntu\home\sakuya\workspace\.hermes\skills\SKILLS_INDEX.md（了解可用 skill 及正确路径）
4. 根据你的角色，按索引中的路径加载对应 skill：
   - Codex → design-agent（设计时）/ review-agent（审查时）
   - Cursor → dev-agent
   - Claude Code → 按需加载
5. 如果 skill 文件找不到：先声明缺失，不得直接开始任务
```

### 📋 启动回执（每次新窗口首次回复时必须输出）

```
🔍 启动检查
- AGENTS.md：✅ 已读
- STATUS.md：✅ 已读
- 角色 skill：✅ xxx 已加载 / ⚠️ 缺失（降级执行）
- 当前角色：🧠 设计 Agent / ✋ 实现 Agent / 🔬 深入 Agent
- 本轮边界：只设计不实现 / 只实现不设计 / 按需深入
```

### ⚠️ skill 缺失处理协议

如果 SKILLS_INDEX.md 中列出的 skill 文件实际上找不到：

1. **必须**在首次回复中声明「索引指向的 skill X 文件缺失，路径：...」
2. **可以**继续按角色边界工作——Codex 只设计/审查，Cursor 只实现/测试
3. **必须**在 `.hermes/handoff.md` 记录缺失的 skill 路径，Hermes 会处理
4. **不得**以 skill 缺失为借口越过角色边界（Codex 永远不能实现代码，Cursor 永远不能做架构决策）

---
---

## 项目概述

> ### 🤖 Agent 自识别（请先读我！）

> 如果你是 **Codex**：你是 🧠 设计+审查者。启动时加载 `design-agent` skill。审查时加载 `review-agent` skill。你负责架构设计、方案对比、技术选型、代码审查——只动脑不动手。
>
> 如果你是 **Cursor**：你是 ✋ 实现+测试者。启动时加载 `dev-agent` skill。你负责按设计文档写代码、写测试、跑测试——只动手不做架构决策。
>
> 如果你是 **Claude Code**：你是 🔬 深入者。先读 `CLAUDE.md`，按需加载 skill。你负责终端操作、git、CI、深度审查。
>
> 如果你是 **Hermes**：你是 🏛 巡检员。加载 `project-briefing`，然后读 STATUS.md。你只管追踪状态，不分发任务。

**目标**：

**负责人**：sakuya
**🧠 设计 Agent**：Codex（架构设计、方案规划、技术选型）
**✋ 实现 Agent**：Cursor（按设计编写代码、运行测试）
**🔬 深入 Agent**：Claude Code（终端脚本/CI/运维/深度审查）
**协调 Agent**：Hermes（追踪进展、更新本文件）

---

## 与 Hermes 的通信机制

本项目使用 `.hermes/` 目录进行多 Agent 协调：

| 文件 | 谁写 | 谁读 | 用途 |
|------|------|------|------|
| `.hermes/plan/STATUS.md` | 执行 Agent（里程碑完成时）+ Hermes（每日巡检时）+ sakuya | 所有人 | **进度快照**：完成里程碑即更新，每日巡检汇总 |
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
1. read_file \\wsl.localhost\Ubuntu\home\sakuya\workspace\.hermes\skills\SKILLS_INDEX.md   ← 先看索引，找需要的 skill
2. read_file <索引用列出的路径>                              ← 加载 skill 正文
3. 按 skill 中的步骤执行
```

### 本项目的推荐 Skill

| 场景 | Skill | 路径 |
|------|-------|------|
| 汇报项目状态 | project-briefing | `\\wsl.localhost\Ubuntu\home\sakuya\.hermes\skills\project-briefing/SKILL.md` |
| 更新项目文档 | project-audit-agents-update | `\\wsl.localhost\Ubuntu\home\sakuya\.hermes\skills\project-audit-agents-update/SKILL.md` |
| TDD 开发 | test-driven-development | `\\wsl.localhost\Ubuntu\home\sakuya\.hermes\skills\software-development/test-driven-development/SKILL.md` |
| Bug 调试 | systematic-debugging | `\\wsl.localhost\Ubuntu\home\sakuya\.hermes\skills\software-development/systematic-debugging/SKILL.md` |
| Python 调试 | python-debugpy | `\\wsl.localhost\Ubuntu\home\sakuya\.hermes\skills\software-development/python-debugpy/SKILL.md` |

> 完整索引见 `\\wsl.localhost\Ubuntu\home\sakuya\workspace\.hermes\skills\SKILLS_INDEX.md`
