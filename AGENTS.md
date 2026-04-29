# crrc-operators — 项目说明文档

> 本文件供 Cursor、Codex、Claude Code 等执行型 Agent 读取。
> Hermes 负责在项目进展时更新本文件。

---

## 项目概述

中车算子对接项目，以文档和接口对接为主。

**负责人**：sakuya
**协调 Agent**：Hermes

---

## 与 Hermes 的通信机制

本项目使用 `.hermes/` 目录与 workspace 总协调 Agent（Hermes）通信：

| 文件 | 谁写 | 谁读 | 用途 |
|------|------|------|------|
| `.hermes/session-log.md` | **你（Cursor/Codex/Claude Code）** | Hermes | 每次会话后追加：做了什么、结果、需要什么 |
| `.hermes/handoff.md` | **你** | Hermes | 需要 Hermes 处理的事项（写完后 Hermes 会清空） |
| `.hermes/bulletin.md` | Hermes | **你** | Hermes 广播的优先级和状态变更 |

**请每次会话结束后追加一条 session-log**，格式：
```
## 2026-04-28 15:30 | Cursor
- 改动：文件路径
- 结果：简要结果
- 需要Hermes：无 / 具体事项
```
