import ctypes
import numpy as np
import os

def detrend(input, n):

    input = np.array([input], dtype=np.float64)

    # 加载动态库
    detrend_lib = ctypes.CDLL(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'libdetrend.so')

    # 定义函数的参数类型和返回类型
    detrend_lib.detrend_wrapper.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, flags='C'),  # input_array
        ctypes.c_int,  # rows
        ctypes.c_int,  # cols
        ctypes.c_int,  # n
        np.ctypeslib.ndpointer(dtype=np.float64, ndim=2, flags='C')   # output_array
    ]
    detrend_lib.detrend_wrapper.restype = None

    # 准备输出数组
    output_array = np.zeros_like(input, dtype=np.float64)

    # 调用 detrend_wrapper 函数
    detrend_lib.detrend_wrapper(
        input, 
        input.shape[0], 
        input.shape[1], 
        n, 
        output_array
    )

    return output_array.tolist()[0]