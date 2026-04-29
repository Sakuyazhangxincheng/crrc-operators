import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] Canny 边缘检测（Canny Edge Detection）
    [原理] 多阶段算法：高斯平滑 → Sobel 梯度 → 非极大值抑制 → 双阈值滞后连接，
           产生单像素宽、连续性好的边缘图。
    [业务场景] 提取工业图像中零件轮廓、焊缝边缘等精细边缘信息；
               与形态学算子配合使用可进一步提取目标区域。

    [配置参数]
    - threshold1 (float, 必填): 滞后下阈值，默认 100
    - threshold2 (float, 必填): 滞后上阈值，默认 200
      （建议 threshold2 = 2~3 × threshold1）
    """
    threshold1 = float(options.get("threshold1", 100))
    threshold2 = float(options.get("threshold2", 200))
    if threshold1 < 0 or threshold2 < 0:
        raise ValueError("threshold1 and threshold2 must be >= 0")
    if threshold1 >= threshold2:
        raise ValueError("threshold1 must be < threshold2")

    return apply_image_op(
        df, target_cols, context,
        lambda img: cv2.Canny(img, threshold1, threshold2),
        read_flags=cv2.IMREAD_GRAYSCALE,
    )
