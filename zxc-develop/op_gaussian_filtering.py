import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 高斯滤波（Gaussian Filtering）
    [原理] 使用高斯核对图像进行卷积，高斯核中心权重大、边缘权重小，平滑同时保留边缘轮廓。
    [业务场景] 去除高频随机噪声（如传感器热噪声、相机量化噪声），常作为边缘检测前的预处理步骤。

    [配置参数]
    - kernel_size (int, 必填): 核大小，须为正奇数，默认 5
    - sigma (float, 可选): 高斯标准差，0 表示由 kernel_size 自动推导，默认 0
    """
    kernel_size = int(options.get("kernel_size", 5))
    sigma = float(options.get("sigma", 0))
    if kernel_size < 1:
        raise ValueError("kernel_size must be >= 1")
    if kernel_size % 2 == 0:
        kernel_size += 1

    return apply_image_op(
        df, target_cols, context,
        lambda img: cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma),
    )
