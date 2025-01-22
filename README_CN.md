简体中文 | [English](README.md)

# KLing-Video-WatermarkRemover-Enhancer

## 项目简介

**KLing-Video-WatermarkRemover-Enhancer** 是一个开源工具，专为处理由可灵（KLing）生成的视频而设计。该工具集成了水印去除和视频增强功能，使视频更加清晰、专业，适用于个人视频优化以及批量视频处理场景。

![Demo](demo.webp)

## 功能特性

- **水印去除**：自动检测并移除可灵生成视频中的水印，保证视频的纯净度。
- **视频增强**：通过高级算法增强视频的清晰度、亮度和对比度，提升观看体验。
- **批量处理**：支持一次处理多个视频文件，高效管理大量视频。

## 安装

按照以下步骤安装 **KLing-Video-WatermarkRemover-Enhancer**：

```bash
git clone --recursive https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer.git
cd KLing-Video-WatermarkRemover-Enhancer
pip install -r requirements.txt
```

## 参数配置

配置文件 `config.yaml` 中定义了水印去除和视频增强参数。

### `watermark`
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

### `enhance`
此部分配置视频增强参数：

- **`RealESRGAN_model_path: "./weights/RealESRGAN_x2plus.pth"`**
  - 这是 Real-ESRGAN 模型权重的路径，用于增强视频的分辨率和质量。
  - 可以在 Real-ESRGAN/inference_realesrgan.py 获取更多的模型。
  - [RealESRGAN_x2plus.pth](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth)

- **`GFPGANer_model_path: "./weights/GFPGANv1.4.pth"`**
  - 这是 GFPGAN 模型权重的路径，用于在视频中进行面部增强，提高面部特征的清晰度和细节。
  - 可以在 Real-ESRGAN/cog_predict.py 获取更多的模型。
  - [GFPGANv1.4.pth](https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth)

## 使用方法

使用 **KLing-Video-WatermarkRemover-Enhancer** 去除水印并增强视频，只需运行以下命令：

```bash
python main.py --input path/to/video.mp4 --remove-watermark --enhance-video
```

### 参数说明

- `--input`：输入视频的路径或文件夹路径。
- `--remove-watermark`：如果指定此参数，则启用水印去除功能。
- `--enhance-video`：如果指定此参数，则启用视频增强功能。

## 示例

```bash
python main.py --input example.mp4 --remove-watermark --enhance-video
```

## 项目结构

- **main.py**：主程序入口，负责管理整个处理流程。
- **modules/**：包含各个功能模块（擦除水印、视频增强等）。
- **utils/**：包含通用工具，如日志记录、视频处理工具等。
- **config.yaml**：配置文件，用于设置水印等参数。

## 参考
- 视频擦除：https://github.com/researchmm/STTN
- 视频修复：https://github.com/xinntao/Real-ESRGAN
