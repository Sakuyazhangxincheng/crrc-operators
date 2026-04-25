import pandas as pd
import numpy as np
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 峰值因子 (Crest Factor) 特征提取
    [数学公式] C = 信号最大绝对值 / 信号RMS值
    [业务场景] 用于判断波形中是否存在离散的极端峰值，常用于衡量冲击强度。
    
    [配置参数] 无特殊配置项
    """
    feature_result = {}
    
    for col in target_cols:
        series = df[col].dropna()
        if len(series) > 0:
            # 1. 提取绝对峰值
            peak = np.max(np.abs(series))
            # 2. 计算 RMS
            rms = np.sqrt(np.mean(np.square(series)))
            
            # 3. 避免除以零导致系统崩溃 (如遇全0直流信号)
            if rms > 1e-12:
                feature_result[f"{col}_CrestFactor"] = float(peak / rms)
            else:
                feature_result[f"{col}_CrestFactor"] = 0.0
                context.setdefault('warnings', []).append(f"列 {col} RMS趋于0，峰值因子置为0")
        else:
            feature_result[f"{col}_CrestFactor"] = np.nan
            
    return pd.DataFrame([feature_result]), context