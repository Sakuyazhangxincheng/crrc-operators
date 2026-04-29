import cv2
import numpy as np
from core_wrapper import operator_wrapper
from image_utils import apply_image_op


@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] Gamma 亮度矫正（Gamma Correction）
    [原理] 对灰度图像每个像素执行幂函数变换：output = (input/255)^(1/gamma) × 255。
           gamma > 1 使图像整体变亮（指数 < 1，暗区被拉伸）；gamma < 1 使图像整体变暗（指数 > 1，暗区被压缩）。
    [业务场景] 校正工业相机采集图像的曝光偏差（过暗/过亮），提升后续特征提取质量。

    [配置参数]
    - gamma (float, 必填): 伽马值，须 > 0，默认 1.0（原图）
    """
    gamma = float(options.get("gamma", 1.0))
    if gamma <= 0:
        raise ValueError("gamma must be > 0")

    inv_gamma = 1.0 / gamma
    lut = np.array(
        [((i / 255.0) ** inv_gamma) * 255 for i in range(256)],
        dtype=np.uint8,
    )

    def _apply(img):
        return cv2.LUT(img, lut)

    return apply_image_op(
        df, target_cols, context,
        _apply,
        read_flags=cv2.IMREAD_GRAYSCALE,
    )
