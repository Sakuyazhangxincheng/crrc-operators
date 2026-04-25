import base64
import copy

import cv2
import numpy as np


def resize_transform(signal, target_height, target_width):
    """
    对输入图像执行缩放变换。

    参数:
    signal (str): 输入的 base64 编码图像字符串。
    target_height (int): 目标高度，必须为大于等于 1 的整数。
    target_width (int): 目标宽度，必须为大于等于 1 的整数。

    返回:
    output (str): 输出的 base64 编码图像字符串。
    """
    signal = copy.deepcopy(signal)
    if not signal:
        return signal

    target_height = int(target_height)
    target_width = int(target_width)
    if target_height < 1 or target_width < 1:
        raise ValueError("target_height and target_width must be >= 1")

    img_data = base64.b64decode(signal)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("无法解码输入图像")

    resized = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_NEAREST)
    _, buffer = cv2.imencode(".jpg", resized)
    output = base64.b64encode(buffer).decode("utf-8")
    return output
