import numpy as np


def sliding_window(input, window_size, step):
    """
    按窗口长度和步长对一维序列执行滑动切片。

    参数:
    input (list): 输入的一维信号序列。
    window_size (int): 窗口长度，必须为大于等于 1 的整数。
    step (int): 滑动步长，必须为大于等于 1 的整数。

    返回:
    output (list): 滑动切分后的二维列表。
    """
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    window_size = int(window_size)
    step = int(step)
    if window_size < 1 or step < 1:
        raise ValueError("window_size and step must be >= 1")

    if signal.size < window_size:
        return [signal.tolist()]

    windows = []
    for i in range(0, signal.size - window_size + 1, step):
        windows.append(signal[i:i + window_size].tolist())
    return windows
