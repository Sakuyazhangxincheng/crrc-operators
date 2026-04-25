from scipy import signal
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    算子：去趋势
    配置项 options: {"type": "linear"} 或 {"type": "constant"}
    """
    detrend_type = options.get("type", "linear")
    
    for col in target_cols:
        mask = df[col].notna()
        if mask.sum() > 1:
            df.loc[mask, col] = signal.detrend(df.loc[mask, col], type=detrend_type)
    return df, context