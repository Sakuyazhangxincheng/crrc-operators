import pandas as pd
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    算子：线性插值
    """
    # limit_direction='both' 确保开头和结尾的 NaN 也能被填充
    df[target_cols] = df[target_cols].interpolate(method='linear', limit_direction='both')
    return df, context