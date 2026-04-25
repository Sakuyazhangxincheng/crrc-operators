import pandas as pd
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    算子：滑动窗口
    配置项 options: {"window_size": 100, "step_size": 50}
    """
    window_size = options.get("window_size", 100)
    step_size = options.get("step_size", 50)
    
    total_rows = len(df)
    windowed_frames = []
    
    window_id = 1
    for start_idx in range(0, total_rows - window_size + 1, step_size):
        current_window = df.iloc[start_idx : start_idx + window_size].copy()
        current_window['window_id'] = window_id  
        windowed_frames.append(current_window)
        window_id += 1
        
    if not windowed_frames:
        return pd.DataFrame(columns=df.columns), context
        
    result_df = pd.concat(windowed_frames, ignore_index=True)
    return result_df, context