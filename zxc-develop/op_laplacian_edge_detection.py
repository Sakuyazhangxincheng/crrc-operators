import cv2
import numpy as np
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 拉普拉斯边缘检测（Laplacian Edge Detection）
    [原理] 对灰度图像计算二阶导数（拉普拉斯算子），在亮度变化剧烈处产生响应；
           对噪声敏感，建议预先使用高斯滤波降噪。
    [业务场景] 检测图像中的细小边缘和纹理变化，与 Canny 互补；
               适合对各方向边缘无偏向性的检测场景。

    [配置参数]
    - ksize (int, 可选): 拉普拉斯核大小，须为正奇数，默认 3
      （ksize=1 使用标准 3×3 拉普拉斯核）
    """
    ksize = int(options.get("ksize", 3))
    if ksize < 1:
        raise ValueError("ksize must be >= 1")
    if ksize % 2 == 0:
        ksize += 1

    def _apply(img):
        lap = cv2.Laplacian(img, cv2.CV_64F, ksize=ksize)
        return np.uint8(np.clip(np.abs(lap), 0, 255))

    return apply_image_op(
        df, target_cols, context,
        _apply,
        read_flags=cv2.IMREAD_GRAYSCALE,
    )
