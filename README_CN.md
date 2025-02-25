简体中文 | [English](README.md)

# 🎥 KLing-Video-WatermarkRemover-Enhancer

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/chenwr727/KLing-Video-WatermarkRemover-Enhancer?style=social)](https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/chenwr727/KLing-Video-WatermarkRemover-Enhancer?style=social)](https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer/network/members)
[![GitHub issues](https://img.shields.io/github/issues/chenwr727/KLing-Video-WatermarkRemover-Enhancer)](https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer/issues)

一键去除可灵视频水印，让你的视频更专业！🚀

![Demo](demo.webp)

</div>

## ✨ 亮点功能

🎯 **完美去水印**
- 智能检测并精准移除可灵水印
- 无损画质，边缘平滑自然
- 支持批量处理，效率拉满

🎨 **AI 画质增强**
- 基于 Real-ESRGAN 的超分辨率技术
- 智能优化亮度、对比度和清晰度
- 面部细节特殊优化，让人物更出彩

⚡ **高效便捷**
- 简单的命令行操作
- 支持批量处理多个视频
- 可自定义处理参数

## 🔧 安装

按照以下步骤安装 **KLing-Video-WatermarkRemover-Enhancer**：

```bash
git clone --recursive https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer.git
conda create -n kling python=3.10
conda activate kling
pip install -r requirements.txt
```

## 🛠️ 参数配置

配置文件 `config.yaml` 中定义了水印去除和视频增强参数。

### `去水印`
此部分配置水印去除的参数：

- `position: [556, 1233, 701, 1267]`
  - 这是去水印的区域位置，通常是定义一个矩形区域的左上角和右下角的坐标。
  - 具体含义是 `(x1, y1, x2, y2)`，分别代表水印的左上角坐标 `(556, 1233)` 和右下角坐标 `(701, 1267)`。
  - 在处理视频时，可以根据这些坐标确定水印区域。

- `ckpt_p: "./weights/sttn.pth"`
  - 这是水印去除模型的权重文件路径。
  - [sttn.pth](https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view?usp=sharing) 是基于时空轨迹网络（STTN，Spatio-Temporal Trajectory Network）的模型文件，通常用于去除动态视频中的物体或水印。

- `mask_expand: 30`
  - 这是水印区域扩展的像素数。
  - 在去水印的过程中，通常需要对水印区域进行适当扩展，以确保去除的水印边缘不会留下残影或瑕疵。

- `neighbor_stride: 10`
  - 表示在去除水印时，时空轨迹网络计算邻域的步长大小。
  - 此值控制在处理视频帧时，对邻近帧的信息进行采样的频率或步长。较大的步长可能会减少计算量，但也可能降低去水印效果。

### `视频增强`
此部分配置视频增强参数：

- **`RealESRGAN_model_path: "./weights/RealESRGAN_x2plus.pth"`**
  - 这是 Real-ESRGAN 模型权重的路径，用于增强视频的分辨率和质量。
  - 可以在 Real-ESRGAN/inference_realesrgan.py 获取更多的模型。
  - [RealESRGAN_x2plus.pth](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth)

- **`GFPGANer_model_path: "./weights/GFPGANv1.4.pth"`**
  - 这是 GFPGAN 模型权重的路径，用于在视频中进行面部增强，提高面部特征的清晰度和细节。
  - 可以在 Real-ESRGAN/cog_predict.py 获取更多的模型。
  - [GFPGANv1.4.pth](https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth)

## 🚀 快速开始

只需一行命令，即可开启视频优化之旅：

```bash
python main.py --input your_video.mp4 --remove-watermark --enhance-video
```

### 🎮 常用命令示例

```bash
# 仅去除水印
python main.py --input video.mp4 --remove-watermark

# 仅增强视频质量
python main.py --input video.mp4 --enhance-video

# 批量处理文件夹中的所有视频
python main.py --input videos_folder --remove-watermark --enhance-video
```

## 📁 项目结构

```
KLing-Video-WatermarkRemover-Enhancer/
├── 📄 main.py          # 主程序入口
├── 📁 modules/         # 核心功能模块
├── 📁 utils/          # 工具函数
└── 📄 config.yaml     # 配置文件
```

## 🤝 参考项目

- [STTN](https://github.com/researchmm/STTN) - 强大的视频擦除技术
- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - 顶尖的视频超分辨率方案

## 🌟 支持项目

如果这个项目对你有帮助，欢迎点个 Star ⭐️
