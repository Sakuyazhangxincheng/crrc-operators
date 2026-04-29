import numpy as np
import pandas as pd
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """算子：降采样（固定步长抽取）

    options:
        factor (int): 降采样倍率，>= 2。
    """
    factor = int(options.get("factor", 2))
    if factor < 2:
        raise ValueError("factor must be >= 2")
    result_df = df.iloc[::factor].reset_index(drop=True)
    return result_df, context
