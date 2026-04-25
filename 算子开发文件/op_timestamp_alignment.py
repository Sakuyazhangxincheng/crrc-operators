import pandas as pd
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    算子：时间戳对齐
    配置项 options: {"time_col_index": 0, "freq": "100ms"}
    """
    time_col_idx = options.get("time_col_index", 0)
    freq = options.get("freq", "100ms")
    time_col = df.columns[time_col_idx]
    
    df[time_col] = pd.to_datetime(df[time_col])
    df = df.set_index(time_col)
    
    df_aligned = df.resample(freq).asfreq()
    df_aligned = df_aligned.reset_index()
    
    return df_aligned, context