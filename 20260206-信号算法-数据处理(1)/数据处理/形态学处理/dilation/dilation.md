膨胀操作是一种形态学图像处理技术，通过应用结构元素来扩展图像中的高亮区域。
###
### 数学原理

膨胀操作是数学形态学中的一种基本操作，用于扩展图像中的高亮区域。给定输入图像 $I$ 和结构元素 $B$，膨胀操作定义为：
$I \oplus B = \{ z \mid (B)_z \cap I \neq \emptyset \}$

其中，$I$ 是输入图像，$B$ 是结构元素，$z$ 是图像中的一个像素点，$(B)_z$ 表示结构元素 $B$ 平移到 $z$ 位置后的结果。膨胀操作的结果是所有使得结构元素与输入图像有非空交集的像素点的集合。

### 应用场景

具体应用场景包括：
- 边缘检测：用于增强图像中的边缘和轮廓，便于进一步的图像分析和处理。
- 图像处理和增强：通过扩展图像中的高亮区域，填补间隙和小孔，提高图像的可视化效果。
- 医学图像分析：在CT、MRI等医学图像中，膨胀操作可以帮助分割和识别器官、组织和病变区域。
- 计算机视觉任务：在目标检测、图像分割和特征提取等任务中作为预处理步骤，增强感兴趣区域。
- 机器人视觉：帮助机器人识别环境中的物体和障碍物，实现路径规划和导航。

### 参数

- `signal`  (str): 输入的 base64 编码图像字符串
- `kernel_size` (int): 核大小，决定膨胀操作的强度
- `iterations`  (int): 迭代次数，决定膨胀操作的次数

### 返回

- `output` (str): 包含处理后的 base64 编码图像字符串

### 示例

#### 输入图像

![signal](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/dilation/before.jpg)

#### 输出图像

![output](https://minio.kaiyuantech.net/huiyan-platform/module-library/module/dilation/after.jpg)