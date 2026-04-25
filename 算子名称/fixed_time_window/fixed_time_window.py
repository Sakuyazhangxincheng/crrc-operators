import numpy as np


def fixed_time_window(input, window_size):
    """
    按固定窗口长度对一维序列切片。

    参数:
    input (list): 输入的一维信号序列。
    window_size (int): 窗口长度，必须为大于等于 1 的整数。

    返回:
    output (list): 按窗口切分后的二维列表。
    """
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    window_size = int(window_size)
    if window_size < 1:
        raise ValueError("window_size must be >= 1")

    windows = []
    for i in range(0, signal.size, window_size):
        windows.append(signal[i:i + window_size].tolist())
    return windows
