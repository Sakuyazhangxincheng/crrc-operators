import numpy as np
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 滑动平均（Moving Average）平滑滤波
    [数学公式] y[i] = mean(x[i-left : i+right+1])，边界采用 edge padding
    [业务场景] 抑制时序信号中的高频噪声，保留整体趋势；常用于振动、温度、电流等传感器原始数据的预处理。

    [配置参数]
    - window_size (int, 必填): 滑动窗口长度，须 >= 1，默认 5
    """
    window_size = int(options.get("window_size", 5))
    if window_size < 1:
        raise ValueError("window_size must be >= 1")

    for col in target_cols:
        series = df[col].to_numpy(dtype=np.float64)

        if window_size == 1 or len(series) == 0:
            continue

        left = window_size // 2
        right = window_size - 1 - left
        padded = np.pad(series, (left, right), mode="edge")
        kernel = np.ones(window_size, dtype=np.float64) / window_size
        df[col] = np.convolve(padded, kernel, mode="valid")

    return df, context
