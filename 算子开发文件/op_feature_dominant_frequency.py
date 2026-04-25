import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 主频 (Dominant Frequency) 提取
    [业务场景] 将时域信号转入频域，寻找能量最集中（幅值最高）的频率成分，用于转速核对或共振分析。
    
    [配置参数]
        - sampling_rate (float): 数据采集频率(Hz)，如果未配置则默认为 1.0Hz
    """
    fs = options.get("sampling_rate", 1.0)
    feature_result = {}
    
    for col in target_cols:
        data = df[col].dropna().values
        n = len(data)
        
        # 必须满足奈奎斯特采样定律的最基本要求（点数>2）
        if n > 2:
            # 1. 进行快速傅里叶变换并求幅值
            yf = np.abs(fft(data))
            # 2. 生成对应的物理频率轴
            xf = fftfreq(n, 1 / fs)
            
            # 3. 截取正频率半轴 (由于实数域信号频谱对称)
            half_n = n // 2
            xf_pos = xf[:half_n]
            yf_pos = yf[:half_n]
            
            # 4. 寻找最大幅值索引。为消除基线漂移影响，通常排除索引 0 (直流分量 0Hz)
            if len(yf_pos) > 1:
                idx_max = np.argmax(yf_pos[1:]) + 1
                feature_result[f"{col}_DomFreq"] = float(xf_pos[idx_max])
            else:
                feature_result[f"{col}_DomFreq"] = 0.0
        else:
            feature_result[f"{col}_DomFreq"] = np.nan
            
    return pd.DataFrame([feature_result]), context