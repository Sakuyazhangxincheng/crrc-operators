import pandas as pd
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    算子：前向/后向填充
    配置项 options: {"method": "ffill"} 或 {"method": "bfill"}
    """
    method = options.get("method", "ffill") 
    if method == "ffill":
        df[target_cols] = df[target_cols].ffill()
    elif method == "bfill":
        df[target_cols] = df[target_cols].bfill()
    else:
        raise ValueError("不支持的填充方法，请指定 'ffill' 或 'bfill'")
    return df, context