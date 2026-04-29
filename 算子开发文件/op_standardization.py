import numpy as np
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """算子：标准化（Z-Score，均值0方差1）"""
    for col in target_cols:
        series = df[col].dropna()
        if series.empty:
            continue
        mean, std = series.mean(), series.std(ddof=0)
        if std == 0:
            df.loc[df[col].notna(), col] = 0.0
        else:
            df[col] = (df[col] - mean) / std
    return df, context
