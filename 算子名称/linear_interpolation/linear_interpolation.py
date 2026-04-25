import numpy as np


def linear_interpolation(input, output_length):
    """
    对一维信号执行线性插值重采样。

    参数:
    input (list): 输入的一维信号序列。
    output_length (int): 目标输出长度，必须为大于等于 2 的整数。

    返回:
    output (list): 重采样后的序列，长度为 output_length。
    """
    signal = np.array(input, dtype=np.float64)

    if signal.size == 0:
        return []

    output_length = int(output_length)
    if output_length < 2:
        raise ValueError("output_length must be >= 2")

    if signal.size == 1:
        return np.full(output_length, signal[0], dtype=np.float64).tolist()

    x_old = np.linspace(0.0, 1.0, num=signal.shape[0], dtype=np.float64)
    x_new = np.linspace(0.0, 1.0, num=output_length, dtype=np.float64)
    output = np.interp(x_new, x_old, signal)
    return output.tolist()
