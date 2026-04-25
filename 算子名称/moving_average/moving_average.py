import numpy as np


def moving_average(input, window_size):
    """对一维信号执行滑动平均平滑。

    Args:
        input (list): 输入的一维信号序列。
        window_size (int): 滑动窗口长度，必须大于等于 1。

    Returns:
        list: 平滑后的信号序列，长度与输入一致。
    """
    # 统一数据类型，避免整数输入导致精度损失
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    window_size = int(window_size)
    if window_size < 1:
        raise ValueError("window_size must be >= 1")
    if window_size == 1:
        return signal.tolist()

    # 边界采用 edge padding，保证输出长度与输入一致
    left = window_size // 2
    right = window_size - 1 - left
    padded = np.pad(signal, (left, right), mode="edge")

    # 等权滑动平均核
    kernel = np.ones(window_size, dtype=np.float64) / window_size
    output = np.convolve(padded, kernel, mode="valid")
    return output.tolist()
