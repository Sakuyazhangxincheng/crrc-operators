`带通滤波`算子在频域保留目标频带成分并抑制带外成分，适用于一维时序信号预处理。

###
### 应用场景

- 机械振动信号去除低频漂移与高频噪声
- 生理信号提取目标频段成分
- 声学/电流信号特定频带分析前预处理

### 描述

`bandpass_filter` 采用 FFT 频域截取方式实现带通滤波。

1. 将输入信号转换为 `float64`。
2. 计算单边频谱与归一化频率轴（`0 ~ 0.5`）。
3. 仅保留 `[low_ratio, high_ratio]` 频带内的频谱分量，其余置零。
4. 通过逆 FFT 重建时域信号，输出与输入等长。

说明：
- 该实现为理想“砖墙”频域滤波，边界可能出现振铃效应（Gibbs 现象）。
- `low_ratio` 与 `high_ratio` 为归一化频率比值，`0.5` 对应奈奎斯特频率。

### 参数说明
#### 输入参数

- `input` (list): 输入一维信号。
- `low_ratio` (float): 低截止比值，要求 `0 < low_ratio < 0.5`。
- `high_ratio` (float): 高截止比值，要求 `low_ratio < high_ratio < 0.5`。

#### 输出结果

- `output` (list): 带通滤波后的信号序列，长度与输入一致。

### 示例
#### 输入数据

```python
signal = [0, 1, 0, -1] * 8
low_ratio = 0.1
high_ratio = 0.3
```

#### 输出数据

```python
output = bandpass_filter(signal, low_ratio, high_ratio)
# 返回带通后的序列
```
