直方图均衡化是一种增强图像对比度的技术，它通过调整图像的灰度值分布，使得图像的灰度值在整个灰度级范围内均匀分布。

###
### 实现过程
直方图均衡化的实现过程主要包括以下步骤：

1. **统计灰度级**：统计原图像中每个灰度级出现的次数，得到灰度直方图。
2. **计算累积分布函数**：计算灰度直方图的累积分布函数（CDF），即每个灰度级及其之前所有灰度级出现的总次数占图像总像素数的比例。
3. **映射新灰度级**：根据累积分布函数，将原图像的每个灰度级映射到一个新的灰度级上，使得新图像的灰度直方图接近均匀分布。
4. **生成新图像**：根据映射后的灰度级生成新的图像。

### 应用场景

具体应用场景包括：
- 图像处理和增强
- 数据预处理
- 计算机视觉任务中的图像优化

### 参数

- `signal` (str): 输入的 base64 编码图像字符串

### 返回

- `output` (str): 输出的 base64 编码图像字符串

### 示例

#### 输入图像

![signal](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/equalize_histogram/before.jpg)

#### 输出图像

![output](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/equalize_histogram/after.jpg)