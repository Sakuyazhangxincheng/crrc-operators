import pandas as pd
import numpy as np
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 均方根值 (Root Mean Square) 特征提取
    [数学公式] RMS = sqrt( (x1^2 + x2^2 + ... + xn^2) / n )
    [业务场景] 衡量时序信号的有效能量大小，常用于评价电机旋转机械的整体振动烈度。
    
    [配置参数] 无特殊配置项
    """
    feature_result = {}
    
    for col in target_cols:
        # 1. 清洗数据：剔除 NaN 值，确保纯数值计算
        series = df[col].dropna()
        
        # 2. 防御性校验：检查有效数据长度
        if len(series) > 0:
            # 计算平方均值的平方根
            rms_val = np.sqrt(np.mean(np.square(series)))
            feature_result[f"{col}_RMS"] = float(rms_val)
        else:
            # 数据全空时填充 NaN，供下游异常检测模块识别
            feature_result[f"{col}_RMS"] = np.nan
            context.setdefault('warnings', []).append(f"列 {col} 无有效数据，跳过 RMS 计算")
            
    # 特征提取类算子输出为单行结果表
    return pd.DataFrame([feature_result]), context