# Urban-Perception-Assessment-Based-on-CNN
基于卷积神经网络的城市感知评估

## 💡 Introductionn

城市感知（Urban perceptions）指的是居民对于城市场所的心理感受，对于城市规划和公共卫生领域有着重要的作用。通常可将对城市场所的心理感受分为beautiful、boring、depressing、lively、safety和wealthy六类。传统上，由于缺乏高通量方法、样本不足，人们对城市感知评估的仍然困难。鉴于这些调查方法成本高、耗时长，因此亟需一个高效率的框架来优化城市感知评估过程。笔者在此提出一个基于卷积神经网络的城市感知分析框架。

## 🎨 在线访问

[基于卷积神经网络的城市感知可视化](http://www.urbancomp.net/2020/01/10/%e5%9f%ba%e4%ba%8e%e5%8d%b7%e7%a7%af%e7%a5%9e%e7%bb%8f%e7%bd%91%e7%bb%9c%e7%9a%84%e5%9f%8e%e5%b8%82%e6%84%9f%e7%9f%a5%e5%8f%af%e8%a7%86%e5%8c%96/)

## ✨ 项目思路

### 数据采集及处理

* 制作App
通过Android手机自带的位置传感器和GPS，获取到当前位置的经度、纬度、高度、速度、方向、测量精度等信息。同时在数据记录方面做了小小的优化，只有当间隔时间1s同时距离超过4米的时候才会进行记录。这样做的目的是为了防止在红绿灯或堵车等情况下同一个地点记录了过多数据的问题。需要注意的是，通过手机自带的GPS传感器记录下的经纬度是WGS84坐标系下的，后面进行可视化的时候需要根据底图进行坐标转换。

![App界面展示](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/App%E7%95%8C%E9%9D%A2%E5%B1%95%E7%A4%BA.jpg)

* 采集数据
在需要采集的地点，只需要点击左上角的Capture按钮，就会开始录制视频，同时将位置信息记录到csv文件中，将视频的开始时间和结束时间记录到txt文件中。数据保存在存储目录下的 `MyCameraApp` 文件夹下。

* 数据处理
在AntV进行可视化时使用的是高德的底图，所以这里需要将采集到的WGS84坐标系下经纬度数据转为火星坐标系下的经纬度数据。

* 图像处理
    1. 根据csv文件中每一条记录所对应的时间，计算出与该时间对应的图像在视频流中的帧数。
    2. 通过OpenCV对相应帧数的图像，进行图像增强，旋转和必要的裁剪，并保存。
    3. 通过Python将csv文件转换为AntV可视化所需的json，csv或GeoJson格式。

关于 App 更多详情可转至 [App](./App/) 目录。

### 网络模型训练

* 搭建网络模型
    * 在 Yao,Y. 等人的研究中，首先使用了全卷积神经网络（FCN）对街景进行语义分割，然后使用随机森林模型拟合人的打分倾向，最终给出推荐分数。
    * 在本神经网络模型中，笔者尝试定义了一个三层双卷积神经网络，输出纬度分别是64、64、128、128、和256、256。在最后的输出层定义了一个全连接神经网络，输出纬度是1。在定义卷积神经网络过程中，按照一个卷积神经网络的标准结构进行定义，使用最大池化（maxpooling）策略进行降维特征提取，使用Dropout防止过拟合，使用BatchNormalization对隐藏层的输出进行归一化。
    * 网络使用rmsprop作为优化器，损失函数设置为均方误差（mse），模型评价标准为平均绝对误差（mae）。
    * 在最后的结果分析中，笔者将自己训练的卷积神经网络对街景图片的打分结果，和 Yao,Y. 在论文中提出的模型的打分结果进行可视化对比，以此来对模型进行大致的评估。

* 训练数据处理
    * 为了增加模型的鲁棒性，同时也为了增加训练数据量，笔者将原图像进行了尺度变换。首先将原图通过OpenCV或PIL进行缩放，然后再恢复成原来尺寸，这样便可以得到一份新的数据样本，同时也增加了训练后模型对不同分辨率图像的适应性。
    * 使用pickle将训练数据、测试数据，及其对应的Label进行打包，方便数据的移动和加载。

* 训练结果
对于六个不同的类别，模型最终训练的结果如下

![beautiful](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/beautiful.png)

![boring](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/boring.png)

![depressing](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/depressing.png)

![lively](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/lively.png)

![safety](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/safety.png)

![wealthy](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/wealthy.png)

## 🍱 可视化展示

![可视化展示](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/可视化展示.png)


## 🛠️ 结果分析
通过和 Yao,Y. 的模型对比分析得知，本框架所采用的卷积神经网络对街景情感的预测会更加准确，差异性会更加的明显。 Yao,Y. 在其论文中提出的通过FCN网络进行语义分割，和随机森林拟合，过重的考虑了地物之间的比重关系，而忽略的地物之间的空间关系。因此，对于不同的街景图片，较难体现出其差异性。这也就是，过于追求神经网络的可解释性，可能的后果就是损失精度。

![YaoY模型对光谷地区的safety打分结果](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/yaoy.jpg)

![我的模型对光谷地区的safety打分结果](https://cdn.jsdelivr.net/gh/ylsislove/Urban-Perception-Assessment-Based-on-CNN/my.png)


## 📜 参考文献
[1] Yao Y, Liang Z, Yuan Z, et al. A human-machine adversarial scoring framework for urban perception assessment using street-view images[J].