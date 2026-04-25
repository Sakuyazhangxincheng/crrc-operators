# 算子开发文件说明

本目录用于时序数据算子开发，包含数据清洗、窗口处理、特征提取和图像预处理算子。  
所有算子都通过 `core_wrapper.py` 提供统一输入输出接口，便于在流程编排系统中调用。

## 目录结构

- `core_wrapper.py`：统一包装器（参数解析、CSV 编解码、上下文管理）
- `op_*.py`：具体算子实现
- `requirements.txt`：Python 依赖
- `environment.yml`：Conda 环境文件
- `tests/test_operators.py`：自动化测试
- `算子对照表.xlsx`：算子标准命名对照

## 环境准备

```bash
conda env create -f environment.yml
conda activate op-dev
```

## 统一调用接口

包装后算子入口：

```python
process(taskId, projectId, csv_data=None, columns=None, options_str="{}", path=None)
```

参数说明：

- `taskId`：任务 ID
- `projectId`：项目 ID
- `csv_data`：Base64 编码的 CSV 内容（与 `path` 二选一）
- `path`：CSV 文件路径（与 `csv_data` 二选一）
- `columns`：待处理列下标列表（如 `[1, 2]`）
- `options_str`：JSON 字符串配置

返回值：

- `output`：处理后的 Base64 CSV
- `options`：回传的 options JSON 字符串

### 通用 options

- `encoding`：默认 `utf-8`
- `delimiter`：默认 `,`
- `has_header`：默认 `true`

## 算子文件名（按《算子对照表》修正）

以下为**对照表算子名称 -> 当前文件名**：

### 数据治理

- 线性插值 -> `op_linear_interpolate.py`
- 前向/后向填充 -> `op_fill_missing.py`
- 去趋势 -> `op_detrend.py`
- 汉宁窗 -> `op_hanning_window.py`

### 窗口与时间

- 固定时间窗 -> `op_fixed_time_window.py`
- 滑动窗口 -> `op_sliding_window.py`
- 时间戳对齐 -> `op_timestamp_alignment.py`

### 特征计算

- RMS -> `op_feature_rms.py`
- 峭度 -> `op_feature_kurtosis.py`
- 峰值因子 -> `op_feature_crest_factor.py`
- 主频 -> `op_feature_dominant_frequency.py`
- 频带能量 -> `op_feature_band_energy.py`

### 图像处理

- 灰度图像与RGB互转 -> `op_image_gray_convert.py`
- 缩放 -> `op_image_resize.py`

## 使用示例

下面示例以 `op_detrend.py` 为例，演示如何调用包装后的 `process`：

```python
import base64
import json
import pandas as pd
from op_detrend import process

df = pd.DataFrame({
    "ts": ["2026-03-25 10:00:00", "2026-03-25 10:00:01", "2026-03-25 10:00:02"],
    "value": [1.0, 2.0, 3.0]
})

csv_b64 = base64.b64encode(df.to_csv(index=False).encode("utf-8")).decode("utf-8")
result = process(
    taskId="task-001",
    projectId="project-001",
    csv_data=csv_b64,
    columns=[1],  # 处理 value 列
    options_str=json.dumps({"type": "linear"})
)

output_csv = base64.b64decode(result["output"]).decode("utf-8")
print(output_csv)
```

## 测试

```bash
pytest -q
```

当前测试覆盖全部算子，并额外校验包装器的：

- `has_header` 支持
- `path` 输入支持
- context 注入字段（`taskId` / `projectId` / `options`）
