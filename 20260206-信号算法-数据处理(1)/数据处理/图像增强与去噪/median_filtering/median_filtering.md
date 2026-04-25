中值滤波通过将图像中的每个像素值替换为其邻域内像素值的中值来去除噪声，特别适用于去除椒盐噪声。

###
### 技术特点

中值滤波的基本原理是把数字图像或数字序列中一点的值用该点的一个邻域中各点值的中值代替，让周围的像素值接近真实值，从而消除孤立的噪声点。
具体来说，它使用一个奇数点的移动窗口，并将模板中心与图中某个像素位置重合，然后读取模板下各对应的像素灰度值（或信号值），
并将这些值进行从小到大的排序，最后选取排序后位于中间的灰度值（或信号值）作为模板中心位置像素的新值。
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

![signal](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/median_filtering/before.jpg)

#### 输出图像

![output](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/median_filtering/after.jpg)