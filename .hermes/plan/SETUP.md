# 环境配置经验库 — crrc-operators

> Agent 在此记录 WSL 环境下配置和运行本项目的经验教训。
> **后来者启动后请先读本文件**，避免重复踩坑。

---

## 运行环境

```bash
# 激活虚拟环境
source .venv/bin/activate

# 关键依赖
# opencv-python, numpy, pandas
```

---

## Agent 踩坑记录

> 每当你遇到环境问题并成功解决，请在此追加。

<!-- 暂无记录，等你来写 -->

---

## 常用命令

```bash
cd zxc-develop

# 平台测试（批量验证）
python run_platform_test.py

# 单元测试
python -m pytest tests/ -v
```
