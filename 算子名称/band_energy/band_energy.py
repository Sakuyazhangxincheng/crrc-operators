import numpy as np


def band_energy(input, low_ratio, high_ratio):
    """
    计算一维信号在指定归一化频带内的频谱能量。

    参数:
    input (list): 输入的一维信号序列。
    low_ratio (float): 频带下界，要求 0 <= low_ratio < 0.5。
    high_ratio (float): 频带上界，要求 low_ratio < high_ratio <= 0.5。

    返回:
    output (float): 指定频带内的频谱能量。
    """
    signal = np.asarray(input, dtype=np.float64)
    sample_count = signal.size
    if sample_count == 0:
        return 0.0

    low_ratio = float(low_ratio)
    high_ratio = float(high_ratio)
    if not (0 <= low_ratio < high_ratio <= 0.5):
        raise ValueError("require 0 <= low_ratio < high_ratio <= 0.5")
    if not np.all(np.isfinite(signal)):
        raise ValueError("input contains non-finite values")

    spectrum = np.fft.rfft(signal)
    frequencies = np.fft.rfftfreq(sample_count, d=1.0)
    band_mask = (frequencies >= low_ratio) & (frequencies <= high_ratio)
    if not np.any(band_mask):
        return 0.0

    energy = np.sum(np.abs(spectrum[band_mask]) ** 2) / sample_count
    return float(energy)
