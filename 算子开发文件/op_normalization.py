import numpy as np
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """算子：归一化（Min-Max，映射到 [0, 1]）"""
    for col in target_cols:
        series = df[col].dropna()
        if series.empty:
            continue
        min_v, max_v = series.min(), series.max()
        if max_v == min_v:
            df.loc[df[col].notna(), col] = 0.0
        else:
            df[col] = (df[col] - min_v) / (max_v - min_v)
    return df, context
