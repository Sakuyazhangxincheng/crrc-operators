import numpy as np


def hanning_window(input):
    """
    对一维信号施加汉宁窗。

    参数:
    input (list): 输入的一维信号序列。

    返回:
    output (list): 施加汉宁窗后的序列。
    """
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    window = np.hanning(signal.size)
    return (signal * window).tolist()
