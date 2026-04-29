import numpy as np
import pandas as pd
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """算子：均值特征提取"""
    feature_result = {}
    for col in target_cols:
        series = df[col].dropna()
        if len(series) > 0:
            feature_result[f"{col}_Mean"] = float(np.mean(series))
        else:
            feature_result[f"{col}_Mean"] = np.nan
            context.setdefault("warnings", []).append(f"列 {col} 无有效数据，跳过均值计算")
    return pd.DataFrame([feature_result]), context
