import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 直方图均衡化（Histogram Equalization）
    [原理] 对灰度图像重新分配像素亮度，使直方图趋近均匀分布，从而自动提升对比度。
    [业务场景] 增强工业图像的细节可见度，尤其适合整体过暗或过亮的图像；
               常用于缺陷检测前的预处理，使目标区域与背景的对比度更清晰。

    [配置参数] 无，算法无可调参数
    """
    return apply_image_op(
        df, target_cols, context,
        cv2.equalizeHist,
        read_flags=cv2.IMREAD_GRAYSCALE,
    )
