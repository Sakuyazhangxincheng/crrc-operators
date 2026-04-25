`低通滤波`算子用于在频域保留低频分量、抑制高频分量，常用于去除高频噪声和短时抖动。

###
### 应用场景

具体应用场景包括：

-   **噪声抑制**:
    -   去除传感器信号中的高频随机噪声。
-   **趋势提取**:
    -   保留慢变化趋势，削弱快速波动。
-   **预处理环节**:
    -   在特征提取前提升信号平稳性。

### 描述

`lowpass_filter` 在频域执行滤波：

1.  对输入信号执行 `rfft` 得到单边频谱。
2.  根据截止频率阈值将高频频点置零。
3.  通过 `irfft` 变换回时域得到滤波后信号。

**截止频率定义**:

- `cutoff_ratio` 取值范围为 `(0, 0.5)`。
- 实际截止频率：`cutoff_hz = cutoff_ratio * nyquist`。
- `nyquist = 0.5 / sampling_interval`，其中 `sampling_interval` 在代码中默认 `1.0`。

**边界行为**:

- 输入为空时返回空列表。
- `cutoff_ratio` 非法（`<=0`、`>=0.5`、`NaN/Inf`）抛出异常。
- `sampling_interval` 非法（`<=0`、`NaN/Inf`）抛出异常（内部默认值通常无需用户配置）。

### 参数说明
#### 输入参数

- `signal` (list): 输入的一维时域信号。
- `cutoff_ratio` (float): 归一化截止频率比例，必须在 `(0, 0.5)`。

#### 输出结果

- `output` (list): 低通滤波后的时域信号，长度与输入一致。

### 示例
#### 输入数据

```python
signal = [0, 1, 0, -1] * 8
cutoff_ratio = 0.2
```

#### 输出数据

```python
output = lowpass_filter(signal, cutoff_ratio)
# 返回低频保留后的序列
```
