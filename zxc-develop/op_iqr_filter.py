import numpy as np
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] IQR 四分位距异常值过滤（IQR Filter）
    [原理] 计算 Q1/Q3 与 IQR = Q3-Q1，将超出 [Q1 - k*IQR, Q3 + k*IQR] 范围的值替换为中位数。
    [业务场景] 鲁棒性优于 3σ 的异常值剔除方法，对偏态分布、非正态信号效果更好；
               常用于温度、压力、流量等传感器数据的粗差剔除。

    [配置参数]
    - k (float, 必填): IQR 放大系数，通常取 1.5（轻度过滤）或 3.0（仅剔除极端异常），默认 1.5
    """
    k = float(options.get("k", 1.5))
    if not np.isfinite(k) or k < 0:
        raise ValueError("k must be a finite non-negative number")

    for col in target_cols:
        series = df[col].dropna()
        if series.empty:
            continue

        vals = series.to_numpy(dtype=np.float64)
        q1 = np.percentile(vals, 25)
        q3 = np.percentile(vals, 75)
        iqr = q3 - q1
        median = np.median(vals)

        if iqr == 0:
            continue

        lower = q1 - k * iqr
        upper = q3 + k * iqr
        mask = (df[col] < lower) | (df[col] > upper)
        df.loc[mask, col] = median

    return df, context
