import pandas as pd
import base64
import cv2
import numpy as np
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 图像几何变换：图像缩放 (Resize)
    [配置参数]
        - width (int): 目标图像宽度，默认 224
        - height (int): 目标图像高度，默认 224
    [业务场景] 将不同尺寸的高清工业相机原图，缩放至统一分辨率，用于输入深度学习模型（如 ResNet/YOLO 常用的 224x224 等尺寸）。
    """
    # 获取目标宽高参数
    w = options.get("width", 224)
    h = options.get("height", 224)
    
    for col in target_cols:
        for i in df.index:
            b64_str = df.at[i, col]
            
            if pd.isna(b64_str) or not isinstance(b64_str, str):
                continue
                
            try:
                img_data = base64.b64decode(b64_str)
                nparr = np.frombuffer(img_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if img is not None:
                    # 获取原图尺寸用于判断缩放策略
                    orig_h, orig_w = img.shape[:2]
                    
                    # 核心算子：尺寸变换
                    # 工业界最佳实践：缩小图像使用 INTER_AREA 以抗混叠；放大图像使用 INTER_LINEAR 或 INTER_CUBIC
                    interpolation = cv2.INTER_AREA if (w * h < orig_w * orig_h) else cv2.INTER_LINEAR
                    resized = cv2.resize(img, (w, h), interpolation=interpolation)
                    
                    # 压缩回写
                    _, buffer = cv2.imencode('.jpg', resized)
                    df.at[i, col] = base64.b64encode(buffer).decode('utf-8')
                else:
                    context.setdefault('warnings', []).append(f"行 {i} 图像解码为空")
                    
            except Exception as e:
                context.setdefault('errors', []).append(f"行 {i} 缩放异常: {str(e)}")
                continue
                
    return df, context