import numpy as np
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    算子：汉宁窗
    """
    for col in target_cols:
        N = len(df[col].dropna())
        if N > 0:
            window = np.hanning(N)
            mask = df[col].notna()
            df.loc[mask, col] = df.loc[mask, col] * window
    return df, context