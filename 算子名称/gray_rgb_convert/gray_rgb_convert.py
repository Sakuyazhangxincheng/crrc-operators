import base64
import copy

import cv2
import numpy as np


def gray_rgb_convert(signal, mode):
    """
    执行灰度图像与 RGB 图像之间的双向转换。

    参数:
    signal (str): 输入的 base64 编码图像字符串。
    mode (str): 转换模式，可选值为 rgb2gray 或 gray2rgb。

    返回:
    output (str): 输出的 base64 编码图像字符串。
    """
    signal = copy.deepcopy(signal)
    if not signal:
        return signal

    mode = str(mode).lower()
    if mode not in ("rgb2gray", "gray2rgb"):
        raise ValueError("mode must be 'rgb2gray' or 'gray2rgb'")

    img_data = base64.b64decode(signal)
    np_arr = np.frombuffer(img_data, np.uint8)

    if mode == "rgb2gray":
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("无法解码输入图像")
        converted = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("无法解码输入图像")
        converted = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    _, buffer = cv2.imencode(".jpg", converted)
    output = base64.b64encode(buffer).decode("utf-8")
    return output
