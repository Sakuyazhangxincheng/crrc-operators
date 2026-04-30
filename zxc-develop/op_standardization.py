import numpy as np
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 标准化（Z-Score Standardization）
    [数学公式] y = (x - mean) / std，使输出均值为 0、标准差为 1
    [业务场景] 消除不同量纲/尺度信号间的差异，使各特征对模型贡献均等；
               常作为机器学习模型的前置预处理步骤。

    [配置参数] 无特殊参数
    """
    for col in target_cols:
        series = df[col].dropna()
        if series.empty:
            continue
        mean = series.mean()
        std = series.std(ddof=0)
        if std == 0:
            df.loc[df[col].notna(), col] = 0.0
        else:
            df[col] = (df[col] - mean) / std
    return df, context
