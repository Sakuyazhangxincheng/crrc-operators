import cv2
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 均值滤波（Mean Filtering / Box Filter）
    [原理] 用邻域内所有像素的算术平均值替代中心像素，等权卷积核，实现最简单的平滑。
    [业务场景] 计算开销最低的平滑方式，适合实时性要求高的场景；缺点是对边缘模糊明显。

    [配置参数]
    - kernel_size (int, 必填): 核大小（边长），须 >= 1，默认 3
    """
    kernel_size = int(options.get("kernel_size", 3))
    if kernel_size < 1:
        raise ValueError("kernel_size must be >= 1")

    return apply_image_op(
        df, target_cols, context,
        lambda img: cv2.blur(img, (kernel_size, kernel_size)),
    )
