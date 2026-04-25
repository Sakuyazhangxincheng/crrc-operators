import numpy as np


def standardization(input):
    """对一维数值序列执行 Z-Score 标准化。

    标准化公式：
        z = (x - mean) / std

    Args:
        input (list): 输入的一维数值序列。

    Returns:
        list: 标准化后的序列。
    """
    # 统一为 float64，保证统计计算稳定
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    mean = np.mean(signal)
    std = np.std(signal)

    # 常量序列标准差为 0，按约定返回全零序列
    if std == 0:
        return np.zeros_like(signal).tolist()

    output = (signal - mean) / std
    return output.tolist()
