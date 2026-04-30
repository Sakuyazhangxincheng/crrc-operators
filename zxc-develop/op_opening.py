import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 形态学开运算（Morphological Opening）
    [原理] 先腐蚀后膨胀。腐蚀消除细小噪声，膨胀恢复主体形状；整体效果：去噪、断开纤细连接。
    [业务场景] 去除二值图像中的小面积噪声点，同时保留主体目标区域大小基本不变；
               常用于提取干净的缺陷轮廓。

    [配置参数]
    - kernel_size (int, 必填): 矩形结构元素边长，须 >= 1，默认 3
    """
    kernel_size = int(options.get("kernel_size", 3))
    if kernel_size < 1:
        raise ValueError("kernel_size must be >= 1")

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

    return apply_image_op(
        df, target_cols, context,
        lambda img: cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel),
        read_flags=cv2.IMREAD_GRAYSCALE,
    )
