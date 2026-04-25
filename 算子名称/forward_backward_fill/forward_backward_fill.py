import numpy as np


def forward_backward_fill(input):
    """
    对一维序列中的缺失值进行前向填充，再执行后向填充。

    参数:
    input (list): 输入的一维信号序列，其中缺失值可为 None 或 NaN。

    返回:
    output (list): 填充后的序列。
    """
    arr = np.array([np.nan if (x is None) else x for x in input], dtype=np.float64)
    if arr.size == 0:
        return []

    for i in range(1, arr.size):
        if np.isnan(arr[i]) and not np.isnan(arr[i - 1]):
            arr[i] = arr[i - 1]

    for i in range(arr.size - 2, -1, -1):
        if np.isnan(arr[i]) and not np.isnan(arr[i + 1]):
            arr[i] = arr[i + 1]

    arr = np.nan_to_num(arr, nan=0.0)
    return arr.tolist()
