import numpy as np


def crest_factor(input):
    """
    计算一维信号的峰值因子。

    参数:
    input (list): 输入的一维信号序列。

    返回:
    output (float): 输入序列的峰值因子。
    """
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return 0.0

    peak_value = np.max(np.abs(signal))
    rms_value = np.sqrt(np.mean(signal ** 2))
    if rms_value == 0:
        return 0.0

    return float(peak_value / rms_value)
