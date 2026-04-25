import numpy as np


def mean_value(input):
    """计算一维信号序列的均值。

    Args:
        input (list): 输入的一维数值序列。

    Returns:
        float: 输入序列均值；空输入时返回 0.0。
    """
    # 统一为 float64，保证统计计算精度一致
    signal = np.array(input, dtype=np.float64)

    # 空输入时返回约定默认值，避免下游流程报错
    if signal.size == 0:
        return 0.0

    # np.mean 返回 numpy 标量，转为原生 float 便于序列化
    return float(np.mean(signal))
