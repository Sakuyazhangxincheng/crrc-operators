import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 形态学闭运算（Morphological Closing）
    [原理] 先膨胀后腐蚀。膨胀填充前景内部空洞，腐蚀恢复主体形状；整体效果：填孔、连接断裂。
    [业务场景] 填充目标区域内的孔洞（如焊点缺陷内部的空隙），将邻近的小区域合并为整体；
               常用于缺陷检测后的结果修补。

    [配置参数]
    - kernel_size (int, 必填): 矩形结构元素边长，须 >= 1，默认 3
    """
    kernel_size = int(options.get("kernel_size", 3))
    if kernel_size < 1:
        raise ValueError("kernel_size must be >= 1")

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

    return apply_image_op(
        df, target_cols, context,
        lambda img: cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel),
        read_flags=cv2.IMREAD_GRAYSCALE,
    )
