伽马校正用于校正图像的亮度，通过非线性变换调整图像的灰度值。
###
### 原理与数学模型
伽马矫正的原理基于人眼对亮度的非线性感知。通过调整像素值的幂函数来改变图像的亮度分布，其数学模型可以表示为：O=I^(1/γ)，其中O是输出像素值，I是输入像素值，γ是Gamma值（伽马值）。

当γ大于1时，图像将变得更加暗。

当γ小于1时，图像将变得更加亮。

### 应用场景

具体应用场景包括：
- 图像处理和增强
- 数据预处理
- 计算机视觉任务中的图像优化

### 参数

- `signal` (str): 输入的 base64 编码图像字符串
- `gamma` (float): 输入的伽马值

### 返回

- `output` (str): 包含处理后的 base64 编码图像字符串

### 示例

#### 输入图像

![signal](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/gamma_correction/before.jpg)

#### 输出图像

![output](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/gamma_correction/after.jpg)