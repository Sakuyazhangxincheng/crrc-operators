import cv2
import numpy as np
import base64
import copy


def mean_filtering(signal, kernel_size):
    """
    对输入的图像进行均值滤波处理。

    参数:
    signal (str): 输入的 base64 编码图像字符串
    kernel_size (int): 核大小

    返回:
    output (str): 包含均衡化处理后的 base64 编码图像字符串
    """

    signal = copy.deepcopy(signal)
    if not signal:
        return signal
    
    # 将base64字符串解码成图像
    img_data = base64.b64decode(signal)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 应用均值滤波
    equ = cv2.blur(img, (kernel_size, kernel_size))

    # 将处理后的图像编码成base64字符串
    _, buffer = cv2.imencode('.jpg', equ)
    output = base64.b64encode(buffer).decode('utf-8')

    return output
