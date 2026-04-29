import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 中值滤波（Median Filtering）
    [原理] 用邻域像素的中位数替代中心像素值，对椒盐噪声有极强的鲁棒性。
    [业务场景] 去除椒盐噪声（随机白/黑像素点），在保留边缘的同时消除脉冲噪声；
               常用于工业相机采集图像的预处理。

    [配置参数]
    - kernel_size (int, 必填): 核大小，须为正奇数（>=3），默认 5
    """
    kernel_size = int(options.get("kernel_size", 5))
    if kernel_size < 3:
        raise ValueError("kernel_size must be >= 3")
    if kernel_size % 2 == 0:
        kernel_size += 1

    return apply_image_op(
        df, target_cols, context,
        lambda img: cv2.medianBlur(img, kernel_size),
    )
