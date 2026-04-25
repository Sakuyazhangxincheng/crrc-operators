import pandas as pd
import base64
import cv2
import numpy as np
from core_wrapper import operator_wrapper

@operator_wrapper
def process(df, target_cols, options, context):
    """
    [算子说明] 图像转换：RGB/BGR 转灰度图
    [输入要求] 目标列的单元格中必须存放图像的 Base64 编码字符串。
    [业务场景] 去除色彩信息，保留亮度梯度的结构信息，极大地降低计算量，用于边缘检测或基础机器视觉预处理。
    """
    for col in target_cols:
        for i in df.index:
            b64_str = df.at[i, col]
            
            # 校验数据类型与非空
            if pd.isna(b64_str) or not isinstance(b64_str, str):
                continue
                
            try:
                # 1. Base64 解码并转化为内存字节数组
                img_data = base64.b64decode(b64_str)
                nparr = np.frombuffer(img_data, np.uint8)
                
                # 2. OpenCV 内存解码为图像矩阵 (BGR格式)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if img is not None:
                    # 3. 核心算子：转换为单通道灰度图
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    
                    # 4. 将灰度矩阵重新压缩编码为 jpg 格式的 Base64
                    _, buffer = cv2.imencode('.jpg', gray)
                    new_b64_str = base64.b64encode(buffer).decode('utf-8')
                    
                    # 5. 回写到数据框中
                    df.at[i, col] = new_b64_str
                else:
                    context.setdefault('warnings', []).append(f"行 {i} 图像解码失败")
                    
            except Exception as e:
                # 隔离单行异常，防止整个批次任务崩溃
                context.setdefault('errors', []).append(f"行 {i} 发生异常: {str(e)}")
                continue
                
    return df, context