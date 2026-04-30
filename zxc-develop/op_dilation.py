import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 形态学膨胀（Dilation）
    [原理] 用结构元素在图像上滑动，只要结构元素与前景像素有交集，中心像素即变为前景；
           效果：填充前景内部空洞、扩张边界、连接临近区域。
    [业务场景] 填充缺陷区域中的孔洞，将断裂的目标连接为整体；与腐蚀配合实现闭运算。

    [配置参数]
    - kernel_size (int, 必填): 矩形结构元素边长，须 >= 1，默认 3
    - iterations (int, 可选): 膨胀迭代次数，默认 1
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
        lambda img: cv2.dilate(img, kernel, iterations=iterations),
        read_flags=cv2.IMREAD_GRAYSCALE,
    )
