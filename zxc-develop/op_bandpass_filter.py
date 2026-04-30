import numpy as np
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 频域带通滤波（Band-pass Filter）
    [原理] 对信号做 rFFT，仅保留 [low_ratio, high_ratio] 频带内的分量，再做 irFFT 还原。
    [业务场景] 提取特定频带的振动分量，例如轴承故障特征频带、电机工频带等。

    [配置参数]
    - low_ratio  (float, 必填): 频带下界归一化比例，须满足 0 < low_ratio < 0.5，默认 0.1
    - high_ratio (float, 必填): 频带上界归一化比例，须满足 low_ratio < high_ratio < 0.5，默认 0.3
      - ratio = freq_hz / (sampling_rate / 2)
      - 例：采样率 1000 Hz，目标 100–300 Hz → low_ratio=0.2, high_ratio=0.6（需不超 0.5）
    """
    low_ratio = float(options.get("low_ratio", 0.1))
    high_ratio = float(options.get("high_ratio", 0.3))

    if not (0 < low_ratio < high_ratio < 0.5):
        raise ValueError("require 0 < low_ratio < high_ratio < 0.5")

    for col in target_cols:
        series = df[col].to_numpy(dtype=np.float64)
        n = len(series)
        if n == 0:
            continue
        if not np.all(np.isfinite(series)):
            raise ValueError(f"列 {col} 包含非有限值（NaN/Inf），请先做缺失值填充")

        spectrum = np.fft.rfft(series)
        freqs = np.fft.rfftfreq(n, d=1.0)
        keep = (freqs >= low_ratio) & (freqs <= high_ratio)
        spectrum[~keep] = 0
        df[col] = np.fft.irfft(spectrum, n=n)

    return df, context
