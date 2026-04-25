import numpy as np


def power_spectral_density(input):
    """估计一维信号的单边功率谱密度（周期图法）。

    Args:
        input (list): 输入的一维时域信号。

    Returns:
        list: 单边功率谱密度序列。
    """
    # 统一数据类型，保证频谱计算稳定
    signal = np.array(input, dtype=np.float64)
    n = signal.size
    if n == 0:
        return []

    # 去均值可减弱直流偏置对谱估计的影响
    signal = signal - np.mean(signal)

    # 单边 FFT
    spectrum = np.fft.rfft(signal)

    # 周期图法 PSD：|X(k)|^2 / N
    psd = (np.abs(spectrum) ** 2) / n

    # 对单边谱进行能量修正：除直流和奈奎斯特点外乘 2
    if n > 1:
        if n % 2 == 0:
            psd[1:-1] *= 2.0
        else:
            psd[1:] *= 2.0

    return psd.tolist()
