import pandas as pd
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    算子：固定时间窗切片
    配置项 options: {"time_col_index": 0, "freq": "5s"} 
    """
    time_col_idx = options.get("time_col_index", 0)
    freq = options.get("freq", "5s")
    time_col = df.columns[time_col_idx]
    
    df[time_col] = pd.to_datetime(df[time_col])
    periods = df[time_col].dt.to_period(freq)
    df['window_id'] = pd.factorize(periods)[0] + 1
    
    return df, context