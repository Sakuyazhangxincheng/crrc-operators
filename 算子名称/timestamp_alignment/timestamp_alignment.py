import numpy as np


def timestamp_alignment(input, target_length):
    """
    将一维序列重采样对齐到指定长度。

    参数:
    input (list): 输入的一维信号序列。
    target_length (int): 目标输出长度，必须为大于等于 2 的整数。

    返回:
    output (list): 对齐后的序列，长度为 target_length。
    """
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    target_length = int(target_length)
    if target_length < 2:
        raise ValueError("target_length must be >= 2")

    if signal.size == 1:
        return np.full(target_length, signal[0], dtype=np.float64).tolist()

    x_old = np.linspace(0.0, 1.0, signal.size, dtype=np.float64)
    x_new = np.linspace(0.0, 1.0, target_length, dtype=np.float64)
    return np.interp(x_new, x_old, signal).tolist()
