import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 形态学腐蚀（Erosion）
    [原理] 用结构元素在图像上滑动，只有当结构元素完全覆盖前景像素时，中心像素才保留为前景；
           效果：消除细小噪声、收缩前景边界、断开纤细连接。
    [业务场景] 去除二值图像中的孤立噪声点，使缺陷区域边界更清晰；
               常与膨胀配合使用（开运算/闭运算）。

    [配置参数]
    - kernel_size (int, 必填): 矩形结构元素边长，须 >= 1，默认 3
    - iterations (int, 可选): 腐蚀迭代次数，默认 1
    """
    kernel_size = int(options.get("kernel_size", 3))
    iterations = int(options.get("iterations", 1))
    if kernel_size < 1:
        raise ValueError("kernel_size must be >= 1")
    if iterations < 1:
        raise ValueError("iterations must be >= 1")

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

    return apply_image_op(
        df, target_cols, context,
        lambda img: cv2.erode(img, kernel, iterations=iterations),
        read_flags=cv2.IMREAD_GRAYSCALE,
    )
