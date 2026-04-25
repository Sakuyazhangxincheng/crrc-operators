高斯滤波使用高斯核对图像进行平滑处理，通常比均值滤波效果更好，能够更有效地去除高斯噪声。
###
### 原理简介

高斯滤波（Gaussian Filtering）是一种平滑图像的滤波方法，主要用于图像处理中的噪声去除和细节模糊。它是通过一个权重为高斯函数的卷积核对图像进行卷积操作来实现的。这里是一些关于高斯滤波的关键点：

1. **高斯函数**：高斯滤波使用高斯函数（Gaussian Function）作为权重分布，它是一个钟形曲线，用于为邻域像素赋予不同的权重。
2. **卷积核**：通常高斯滤波使用一个大小为 \( (2k+1) \times (2k+1) \) 的卷积核，其中 \( k \) 是标准差。较大的标准差值将产生更模糊的图像。
3. **边缘处理**：高斯滤波会平滑图像细节，包括噪声和边缘。这在降噪处理中非常有用，但需要注意可能会导致边缘信息的丢失。

以下是一个高斯滤波的公式表示：

$$ G(x, y) = \frac{1}{2\pi\sigma^2} \exp\left(-\frac{x^2 + y^2}{2\sigma^2}\right) $$

其中 \( (x, y) \) 是卷积核中心，\( \sigma \) 是标准差。这个公式定义了卷积核中每个像素的权重分布。

### 应用场景

具体应用场景包括：
- 图像处理和增强
- 数据预处理
- 计算机视觉任务中的图像优化

### 参数

- `signal` (str): 输入的 base64 编码图像字符串
- `kernel_size` (int): 滤波核大小

### 返回

- `output` (str): 包含处理后的 base64 编码图像字符串

### 示例

#### 输入图像

![signal](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/gaussian_filtering/before.jpg)

#### 输出图像

![output](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/gaussian_filtering/after.jpg)