import numpy as np
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """算子：3σ过滤（异常值替换为均值）"""
    sigma = float(options.get("sigma", 3.0))
    for col in target_cols:
        series = df[col].dropna().to_numpy(dtype=np.float64)
        if series.size == 0 or np.std(series) == 0:
            continue
        mean, std = np.mean(series), np.std(series)
        mask = df[col].notna() & ((df[col] < mean - sigma * std) | (df[col] > mean + sigma * std))
        df.loc[mask, col] = mean
    return df, context
