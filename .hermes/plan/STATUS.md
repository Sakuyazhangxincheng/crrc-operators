# Project Status — crrc-operators

> **最后更新**：2026-05-07 | **更新者**：Hermes（每日巡检自动刷新）
>
> Agent 启动后请按顺序读取：
> 1. `AGENTS.md` — 项目架构和约定
> 2. **本文件** — 当前进度 ← 你在这里
> 3. `.hermes/session-log.md` — 最近工作细节（按需）

---

## 1. 当前阶段

**Phase: 算子实现与测试**

中车信号/图像处理算子 Python 实现。16 个算子模块 + 28 个参考规格，35 个测试用例。

---

## 2. 最近完成（本周）

- ✅ op_standardization 标准化算子实现 (4/30)
- ✅ 平台测试运行器（run_platform_test.py，批量验证 (4/30)
- ✅ 25 个新增信号/图像处理算子 (4/29)
- ✅ 测试套件重构（test_new_operators.py，35 用例）(4/29)

---

## 3. 正在进行

- 无活跃会话（最后一次提交 4/30，距今天 10 天）

---

## 4. 阻塞项

无

---

## 5. 下一步

1. 运行平台测试验证所有算子
2. 对照 28 个参考规格检查覆盖率
3. 补充缺失算子的实现

---

## 6. 验证命令

```bash
source .venv/bin/activate
cd zxc-develop
python run_platform_test.py      # 批量平台验证
python -m pytest tests/ -v        # 单元测试
```

---

## 7. 关键文件速查

| 文件/目录 | 用途 |
|-----------|------|
| `zxc-develop/` | **主力开发目录**：16 算子 + 测试 |
| `zxc-develop/run_platform_test.py` | 平台测试运行器 |
| `zxc-develop/tests/test_new_operators.py` | 35 个测试用例 |
| `算子名称/` | 28 个算子规格（.py + .json + .md） |
| `算子开发文件/` | 原始实现（参考，gitignored） |
