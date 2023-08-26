**<h1 style="text-align: center;">Label_Change_Tool</h1>**

<div style="display: flex; justify-content: center;">

  <span style="margin: 0 8px;">
    <a href="https://github.com/GeekFong/Label_Change_Tool">
      <img src="https://badgen.net/badge/Label_Change_Tool/v1.0/green" alt="Label_Change_Tool">
    </a>
  </span>

  <span style="margin: 0 1px;">
    <a href="https://github.com/RichardLitt/standard-readme">
      <img src="https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square" alt="standard-readme">
    </a>
  </span>

  <span style="margin: 0 8px;">
    <a href="https://www.python.org/">
      <img src="https://badgen.net/badge/python/3.8/blue" alt="python">
    </a>
  </span>

  <span style="margin: 0 8px;">
    <a href="http://www.jinglingbiaozhu.com/">
      <img src="https://badgen.net/badge/精灵标注/标注工具/blue" alt="python">
    </a>
  </span>


  <span style="margin: 0 8px;">
    <a href="https://github.com/ultralytics/yolov5">
      <img src="https://badgen.net/badge/yolo/v5.5/blue" alt="python">
    </a>
  </span>

</div>

## **内容列表**
- [**内容列表**](#内容列表)
- [**简介**](#简介)
- [**Label\_Change\_Tool使用说明**](#label_change_tool使用说明)
- [**问题**](#问题)
- [**联系方式**](#联系方式)
- [**赞助和广告**](#赞助和广告)


## **简介**
这款工具的初衷源于使用yolo进行识别时的一些问题。在完成初始模型的训练后，实际运行环境中常常出现误识别的情况。为了解决这个问题，我开始收集这些被误识别的图片。接下来，我使用初始模型重新识别这些图片，生成了包含误识别信息的txt标注文件。但是标注精灵需要的是xml格式的标注文件，所以需要进行转换，以便在标注精灵中重新标注那些出现误识别的地方。

这个过程的目标是减少重新标注的时间，因为传统的方法非常耗时。另外，为了进一步提升模型的准确性，我需要将这些重新标注的数据转换成yolo所需的txt标注格式，并用它们重新训练模型。然而，这些转换步骤非常繁琐，容易出错。

因此，我决定开发了这款转换工具，并分享给有着类似需求的人,帮助那些面临相同挑战的人节省时间和精力。



## **Label_Change_Tool使用说明**
Label_Change_Tool这个工具主要支持一下几种标注格式的相互转换：

-  yolo的txt格式
-  Pascal VOC的xml格式转换
-  [标注精灵](http://www.jinglingbiaozhu.com/)的xml格式转换（这是我经常使用的标注工具）

![软件截图](/doc/image/1.png)
整个界面主要由以下几部分组成:
1. 进度条：实时显示转换的进度
2. 标签名：标注时自己定义的标签名字,用逗号分隔如（骑车,飞机,人）
3. 左边是需要转换的标签文件（选择标签文件的路径和对应的图片，点击按钮即可选择路径）
4. 右边是需要转换后的标签类型（填写转换后输出的地址，点击按钮即可选择路径）
5. 校验按钮作用（判断需要转换的标签和图片数量是否一直，不一致会移动的wrong_file,并且检测图片类型是否为jpg）
6. 点击转换按钮后即可进行转换





## **问题**
1. 如果在使用过程中遇到什么问题，可以先查看Logger文件夹中的log.txt。
2. 如还是解决不了可以提交[issue](https://github.com/GeekFong/Label_Change_Tool/issues),并提交log信息
3. 最终还是解决不了可以通过下面方式联系我。




## **联系方式**
- qq: 502969366
- 我的博客: http://www.geekfong.cn/
- tg: https://t.me/f0x15
- 关注 **微信公众号**


![](./doc/image/1.jpg)


## **赞助和广告**

- 创造不易, 关注点赞支持一波
- [5元chatgpt账号](https://xiaomaipu.geekfong.cn/)

