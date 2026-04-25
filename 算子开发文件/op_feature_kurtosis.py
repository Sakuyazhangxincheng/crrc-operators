import pandas as pd
import numpy as np
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 峭度 (Kurtosis) 特征提取
    [统计意义] 描述数据分布陡峭程度及尾部粗细的四阶中心矩。
    [业务场景] 对早期冲击类故障（如齿轮断齿、轴承外圈点蚀）极其敏感。正常信号峭度约等于3。
    
    [配置参数] 无特殊配置项
    """
    feature_result = {}
    
    for col in target_cols:
        # Pandas 的 kurt() 默认计算 Fisher 峭度（超额峭度），即标准峭度减去 3
        # 结果 > 0 表示存在较多极端冲击脉冲
        series = df[col].dropna()
        if len(series) > 3:  # 计算峭度通常需要至少4个数据点
            val = series.kurt()
            feature_result[f"{col}_Kurtosis"] = float(val)
        else:
            feature_result[f"{col}_Kurtosis"] = np.nan
            context.setdefault('warnings', []).append(f"列 {col} 数据点不足，无法计算峭度")
        
    return pd.DataFrame([feature_result]), context