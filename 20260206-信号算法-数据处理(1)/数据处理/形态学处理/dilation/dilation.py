import cv2
import numpy as np
import base64
import copy


def dilation(signal, kernel_size, iterations):
    """
    对输入的图像的灰度图进行膨胀操作。

    参数:
    signal  (str): 输入的 base64 编码图像字符串
    kernel_size (int): 核大小
    iterations  (int): 迭代次数

    返回:
    output (str): 输出的 base64 编码图像字符串
    """

    signal = copy.deepcopy(signal)
    if not signal:
        return signal
    
    # 将base64字符串解码成图像
    img_data = base64.b64decode(signal)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    # 创建结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

    # 应用膨胀操作
    dilated = cv2.dilate(img, kernel, iterations=iterations)

    # 将处理后的图像编码成base64字符串
    _, buffer = cv2.imencode('.jpg', dilated)
    output = base64.b64encode(buffer).decode('utf-8')

    return output
