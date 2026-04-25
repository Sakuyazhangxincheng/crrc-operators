import cv2
import numpy as np
import base64
import copy


def gamma_correction(signal, gamma):
    """
    对输入的图像的灰度图进行伽马矫正处理。

    参数:
    signal (str): 输入的 base64 编码图像字符串
    gamma (float): 伽马值

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

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    img = cv2.LUT(img, table)

    # 将处理后的图像编码成base64字符串
    _, buffer = cv2.imencode('.jpg', img)
    output = base64.b64encode(buffer).decode('utf-8')

    return output
