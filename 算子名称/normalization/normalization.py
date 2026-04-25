import numpy as np


def normalization(input):
    """对一维数值序列执行 Min-Max 归一化到 [0, 1] 区间。

    Args:
        input (list): 输入的一维数值序列。

    Returns:
        list: 归一化后的序列。
    """
    # 统一为 float64，保证数值计算稳定
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    min_v = np.min(signal)
    max_v = np.max(signal)

    # 常量序列无法执行标准 Min-Max 归一化，按约定返回全零序列
    if max_v == min_v:
        return np.zeros_like(signal).tolist()

    output = (signal - min_v) / (max_v - min_v)
    return output.tolist()
