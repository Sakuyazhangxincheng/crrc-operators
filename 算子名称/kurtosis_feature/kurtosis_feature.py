import numpy as np


def kurtosis_feature(input):
    """
    计算一维信号的超额峭度。

    参数:
    input (list): 输入的一维信号序列。

    返回:
    output (float): 输入序列的超额峭度。
    """
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return 0.0

    mean_value = np.mean(signal)
    std_value = np.std(signal)
    if std_value == 0:
        return 0.0

    normalized_fourth_moment = np.mean(((signal - mean_value) / std_value) ** 4)
    return float(normalized_fourth_moment - 3.0)
