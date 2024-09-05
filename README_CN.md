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
git clone https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer.git
cd KLing-Video-WatermarkRemover-Enhancer
pip install -r requirements.txt
```

## 使用方法

使用 **KLing-Video-WatermarkRemover-Enhancer** 去除水印并增强视频，只需运行以下命令：

```bash
python main.py --input path/to/video.mp4 --output path/to/output.mp4
```

### 参数说明

- `--input`：输入视频的路径或文件夹路径。
- `--output`：处理后视频的保存路径。
- `--remove-watermark`：启用水印去除功能（默认启用）。
- `--enhance-video`：启用视频增强功能（默认启用）。

## 示例

```bash
python main.py --input example.mp4 --output enhanced_example.mp4
```

## 项目结构

- **main.py**：主程序入口，负责管理整个处理流程。
- **modules/**：包含各个功能模块（OCR、擦除字幕、翻译、嵌入字幕）。
- **utils/**：包含通用工具，如日志记录、视频处理工具等。
- **config.yaml**：配置文件，用于设置语言、视频格式等参数。

## 参考
- 视频擦除：https://github.com/researchmm/STTN
- 视频修复：https://github.com/xinntao/Real-ESRGAN
