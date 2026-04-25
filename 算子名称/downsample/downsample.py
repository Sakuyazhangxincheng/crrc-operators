import numpy as np


def downsample(input, factor):
    """按固定步长对一维信号进行降采样。

    Args:
        input (list): 输入的一维信号。
        factor (int): 降采样倍率，必须大于等于 2。

    Returns:
        list: 降采样后的序列。
    """
    # 转换为 float64，保证数值计算和下游处理一致
    signal = np.array(input, dtype=np.float64)

    # 空输入直接返回空列表
    if signal.size == 0:
        return []

    factor = int(factor)
    if factor < 2:
        raise ValueError("factor must be >= 2")

    # 每隔 factor 个点保留一个采样点
    return signal[::factor].tolist()
