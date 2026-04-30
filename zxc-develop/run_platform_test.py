"""
本地平台流程模拟脚本
====================
完整模拟 dataset.crrchy.com 上的执行过程：
  读取 CSV → Base64 编码 → 调用算子 process() → Base64 解码 → 展示结果

用法：
    cd /home/sakuya/workspace/crrc-operators/zxc-develop
    python run_platform_test.py
"""

import base64
import io
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# ── 配置区（修改这里来测试不同算子）──────────────────────────────────────
OPERATOR_MODULE = "op_standardization"   # 算子文件名（不含 .py）
CSV_PATH        = ROOT / "test_data" / "test_standardization.csv"
COLUMNS         = [1]                    # 处理第几列（0-based），此处处理 vibration
OPTIONS         = {}                     # 算子参数，标准化无需参数
# ─────────────────────────────────────────────────────────────────────────


def encode_csv(path: Path) -> str:
    """读取 CSV 文件并 Base64 编码，模拟平台的输入。"""
    raw = path.read_bytes()
    return base64.b64encode(raw).decode("utf-8")


def decode_csv(b64: str) -> pd.DataFrame:
    """Base64 解码并解析为 DataFrame，模拟平台的输出解析。"""
    csv_str = base64.b64decode(b64).decode("utf-8")
    return pd.read_csv(io.StringIO(csv_str))


def run():
    print("=" * 60)
    print(f"算子：{OPERATOR_MODULE}")
    print(f"数据：{CSV_PATH.name}")
    print(f"目标列索引：{COLUMNS}")
    print(f"参数：{OPTIONS}")
    print("=" * 60)

    # ── Step 1：加载原始数据 ──────────────────────────────────────────
    df_input = pd.read_csv(CSV_PATH)
    print("\n【输入数据】")
    print(df_input.to_string(index=True))

    # ── Step 2：编码（模拟平台传参） ──────────────────────────────────
    csv_b64 = encode_csv(CSV_PATH)

    # ── Step 3：动态加载算子并调用 ────────────────────────────────────
    import importlib
    op = importlib.import_module(OPERATOR_MODULE)

    result = op.process(
        taskId="local-test-001",
        projectId="local-project",
        csv_data=csv_b64,
        columns=COLUMNS,
        options_str=json.dumps(OPTIONS),
    )

    # ── Step 4：解码输出（模拟平台接收结果） ──────────────────────────
    df_output = decode_csv(result["output"])

    print("\n【输出数据】")
    print(df_output.to_string(index=True))

    # ── Step 5：自动验证 ──────────────────────────────────────────────
    print("\n【验证结果】")
    processed_col = df_input.columns[COLUMNS[0]]

    mean_out = df_output[processed_col].mean()
    std_out  = df_output[processed_col].std(ddof=0)

    print(f"  处理列：{processed_col}")
    print(f"  输出均值：{mean_out:.6f}  （期望 ≈ 0）")
    print(f"  输出标准差：{std_out:.6f}  （期望 ≈ 1）")

    mean_ok = abs(mean_out) < 1e-10
    std_ok  = abs(std_out - 1.0) < 1e-10

    # 检查未处理列是否保持不变
    unchanged_cols = [c for i, c in enumerate(df_input.columns) if i not in COLUMNS]
    cols_unchanged = all(
        df_input[c].equals(df_output[c]) for c in unchanged_cols
    )

    print(f"  未处理列不变：{cols_unchanged}  （期望 True）")
    print(f"  行数不变：{len(df_input) == len(df_output)}  （期望 True）")

    all_pass = mean_ok and std_ok and cols_unchanged and (len(df_input) == len(df_output))

    print()
    if all_pass:
        print("✅  全部验证通过 —— 算子行为正确，可上平台测试")
    else:
        print("❌  验证失败，请检查以下项：")
        if not mean_ok:
            print(f"    - 均值不为 0：{mean_out:.6f}")
        if not std_ok:
            print(f"    - 标准差不为 1：{std_out:.6f}")
        if not cols_unchanged:
            print(f"    - 未处理列发生了变化")
        if len(df_input) != len(df_output):
            print(f"    - 行数变化：{len(df_input)} → {len(df_output)}")

    print("=" * 60)


if __name__ == "__main__":
    run()
