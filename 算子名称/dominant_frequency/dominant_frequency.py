import numpy as np


def dominant_frequency(input, sampling_rate):
    """
    估计一维信号幅值谱中的主频。

    参数:
    input (list): 输入的一维信号序列。
    sampling_rate (float): 采样率，必须大于 0。

    返回:
    output (float): 信号的主频。
    """
    signal = np.array(input, dtype=np.float64)
    sample_count = signal.size
    if sample_count == 0:
        return 0.0

    sampling_rate = float(sampling_rate)
    if not np.isfinite(sampling_rate) or sampling_rate <= 0:
        raise ValueError("sampling_rate must be > 0")

    magnitude = np.abs(np.fft.rfft(signal))
    frequencies = np.fft.rfftfreq(sample_count, d=1.0 / sampling_rate)

    if magnitude.size > 0:
        magnitude[0] = 0.0

    dominant_index = int(np.argmax(magnitude))
    return float(frequencies[dominant_index])
