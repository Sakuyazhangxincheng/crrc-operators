import numpy as np


def fft_transform(input):
    """对一维信号执行 FFT，并返回单边幅值谱。

    Args:
        input (list): 输入的一维时域信号。

    Returns:
        list: 单边幅值谱（长度为 n//2 + 1）。
    """
    # 统一输入数据类型，避免整数/混合类型导致频谱计算精度不一致
    signal = np.array(input, dtype=np.float64)

    # 空输入时直接返回空列表，避免下游流程报错
    if signal.size == 0:
        return []

    # 使用实数 FFT（rfft）得到单边频谱，适合实值信号
    spectrum = np.fft.rfft(signal)

    # 输出幅值谱（复数频谱取模）
    return np.abs(spectrum).tolist()
