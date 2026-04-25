import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 频带能量 (Band Energy) 计算
    [业务场景] 计算指定频率区间内的信号能量之和，常用于特定故障特征频带（如轴承内外圈故障频率附近）的能量监控。
    
    [配置参数]
        - sampling_rate (float): 采样率(Hz)
        - f_min (float): 关注频带的下限频率
        - f_max (float): 关注频带的上限频率
    """
    fs = options.get("sampling_rate", 1.0)
    f_min = options.get("f_min", 0.0)
    f_max = options.get("f_max", fs / 2.0)
    
    feature_result = {}
    
    for col in target_cols:
        data = df[col].dropna().values
        n = len(data)
        
        if n > 2:
            yf = np.abs(fft(data))
            xf = fftfreq(n, 1 / fs)[:n//2]
            yf_pos = yf[:n//2]
            
            # 创建布尔掩码，筛选出落在 [f_min, f_max] 范围内的频率点
            mask = (xf >= f_min) & (xf <= f_max)
            
            # 能量 = 该频段内各频率点幅值的平方和
            energy = np.sum(np.square(yf_pos[mask]))
            feature_result[f"{col}_BandEnergy"] = float(energy)
        else:
            feature_result[f"{col}_BandEnergy"] = np.nan
            
    return pd.DataFrame([feature_result]), context