"""
图像算子公共工具：Base64 ↔ OpenCV ndarray 转换，以及批量行处理框架。

所有图像类算子都通过 apply_image_op() 统一调用，避免重复编解码样板代码。
"""
import base64

import cv2
import numpy as np
import pandas as pd


def decode_b64_image(b64_str: str, flags: int = cv2.IMREAD_COLOR) -> np.ndarray:
    """将 Base64 编码的图像字符串解码为 OpenCV ndarray。"""
    img_data = base64.b64decode(b64_str)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, flags)
    if img is None:
        raise ValueError("图像解码失败（imdecode 返回 None，请检查 Base64 数据是否为有效图像）")
    return img


def encode_image_b64(img: np.ndarray, fmt: str = ".jpg") -> str:
    """将 OpenCV ndarray 编码为 Base64 字符串。"""
    ok, buffer = cv2.imencode(fmt, img)
    if not ok:
        raise ValueError(f"图像编码失败（格式 {fmt}）")
    return base64.b64encode(buffer).decode("utf-8")


def apply_image_op(df, target_cols, context, op_fn, read_flags: int = cv2.IMREAD_COLOR):
    """
    对 DataFrame 中目标列的每个 Base64 图像单元格执行 op_fn。

    Args:
        df: 输入 DataFrame
        target_cols: 需要处理的列名列表
        context: 算子上下文（用于记录警告/错误）
        op_fn: 接收 np.ndarray 并返回 np.ndarray 的图像处理函数
        read_flags: cv2.imread 读取模式，默认 cv2.IMREAD_COLOR（BGR 彩色）

    Returns:
        (df, context)
    """
    for col in target_cols:
        for i in df.index:
            b64_str = df.at[i, col]
            if pd.isna(b64_str) or not isinstance(b64_str, str):
                continue
            try:
                img = decode_b64_image(b64_str, flags=read_flags)
                result_img = op_fn(img)
                df.at[i, col] = encode_image_b64(result_img)
            except Exception as e:
                context.setdefault("errors", []).append(
                    f"列 {col} 行 {i} 处理失败: {e}"
                )
    return df, context
