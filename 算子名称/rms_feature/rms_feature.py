import numpy as np


def rms_feature(input):
    """
    计算一维信号的均方根值。

    参数:
    input (list): 输入的一维信号序列。

    返回:
    output (float): 输入序列的均方根值。
    """
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return 0.0

    return float(np.sqrt(np.mean(signal ** 2)))
