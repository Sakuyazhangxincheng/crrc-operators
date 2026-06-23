# CLAUDE.md — crrc-operators

> 完整上下文见 `AGENTS.md`。本文件由 claude-md-management 自动维护。

## 启动顺序
1. `AGENTS.md` — 架构/技术栈/约定
2. `.hermes/plan/STATUS.md` — 当前进度
3. `.hermes/session-log.md` — 最近工作

## 快速激活
```bash
source .venv/bin/activate   # opencv/numpy/pandas
```

## 关键命令
```bash
cd zxc-develop && python -m pytest tests/ -v
```

## 项目约定
- 中车信号/图像处理算子 Python 实现
- 16 算子模块 + 28 参考规格
- 文档和接口对接为主
