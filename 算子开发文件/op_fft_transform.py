import numpy as np
import pandas as pd
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """算子：FFT 变换（时域 → 单边幅值谱）

    输出行数为 n//2+1（频率 bin 数），非目标列被丢弃。
    options:
        sampling_rate (float): 采样率（Hz），默认 1.0，用于生成 freq 列。
    """
    sampling_rate = float(options.get("sampling_rate", 1.0))

    result = {}
    n_out = None

    for col in target_cols:
        signal = df[col].dropna().to_numpy(dtype=np.float64)
        if signal.size == 0:
            continue
        spectrum = np.abs(np.fft.rfft(signal))
        result[col] = spectrum
        if n_out is None:
            n_out = spectrum.size

    if n_out is None:
        return pd.DataFrame(columns=target_cols), context

    # 频率轴：取最长那列对应的采样点数生成
    n_signal = len(df[target_cols[0]].dropna())
    freqs = np.fft.rfftfreq(n_signal, d=1.0 / sampling_rate)
    result_df = pd.DataFrame({"freq": freqs})
    for col, spectrum in result.items():
        result_df[col] = spectrum

    return result_df, context
