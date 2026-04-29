import numpy as np
import pandas as pd
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """算子：功率谱密度（周期图法，时域 → 单边 PSD）

    输出行数为 n//2+1，非目标列被丢弃。
    options:
        sampling_rate (float): 采样率（Hz），默认 1.0，用于生成 freq 列。
    """
    sampling_rate = float(options.get("sampling_rate", 1.0))

    result = {}
    n_signal = None

    for col in target_cols:
        signal = df[col].dropna().to_numpy(dtype=np.float64)
        if signal.size == 0:
            continue
        n = signal.size
        signal = signal - np.mean(signal)
        spectrum = np.fft.rfft(signal)
        psd = (np.abs(spectrum) ** 2) / n
        if n > 1:
            psd[1:-1 if n % 2 == 0 else None] *= 2.0
        result[col] = psd
        if n_signal is None:
            n_signal = n

    if n_signal is None:
        return pd.DataFrame(columns=target_cols), context

    freqs = np.fft.rfftfreq(n_signal, d=1.0 / sampling_rate)
    result_df = pd.DataFrame({"freq": freqs})
    for col, psd in result.items():
        result_df[col] = psd

    return result_df, context
