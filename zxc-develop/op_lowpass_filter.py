import numpy as np
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 频域低通滤波（Low-pass Filter）
    [原理] 对信号做 rFFT，将高于截止频率的频率分量置零，再做 irFFT 还原时域信号。
    [业务场景] 去除高频干扰、抑制量化噪声，保留低频趋势分量；适用于振动、温度等缓变传感器信号。

    [配置参数]
    - cutoff_ratio (float, 必填): 归一化截止频率比例，须在 (0, 0.5) 范围内，默认 0.2
      - cutoff_ratio = cutoff_hz / (sampling_rate / 2)
      - 例：采样率 100 Hz、截止 10 Hz → cutoff_ratio = 10 / 50 = 0.2
    - sampling_interval (float, 可选): 采样间隔（秒），默认 1.0
    """
    cutoff_ratio = float(options.get("cutoff_ratio", 0.2))
    sampling_interval = float(options.get("sampling_interval", 1.0))

    if not (0 < cutoff_ratio < 0.5):
        raise ValueError("cutoff_ratio must be in (0, 0.5)")
    if sampling_interval <= 0:
        raise ValueError("sampling_interval must be > 0")

    for col in target_cols:
        series = df[col].to_numpy(dtype=np.float64)
        n = len(series)
        if n == 0:
            continue

        spectrum = np.fft.rfft(series)
        freqs = np.fft.rfftfreq(n, d=sampling_interval)
        nyquist = 0.5 / sampling_interval
        cutoff_hz = cutoff_ratio * nyquist
        spectrum[freqs > cutoff_hz] = 0
        df[col] = np.fft.irfft(spectrum, n=n)

    return df, context
