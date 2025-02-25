[简体中文](README_CN.md) | English

# 🎥 KLing-Video-WatermarkRemover-Enhancer

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/chenwr727/KLing-Video-WatermarkRemover-Enhancer?style=social)](https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/chenwr727/KLing-Video-WatermarkRemover-Enhancer?style=social)](https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer/network/members)
[![GitHub issues](https://img.shields.io/github/issues/chenwr727/KLing-Video-WatermarkRemover-Enhancer)](https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer/issues)

One-click watermark removal for KLing videos - Make your videos more professional! 🚀

![Demo](demo.webp)

</div>

## ✨ Key Features

🎯 **Perfect Watermark Removal**
- Smart detection and precise removal of KLing watermarks
- Lossless quality with smooth, natural edges
- Batch processing support for maximum efficiency

🎨 **AI Video Enhancement**
- Super-resolution technology powered by Real-ESRGAN
- Smart optimization of brightness, contrast, and clarity
- Special facial detail enhancement for better-looking characters

⚡ **Efficient & Convenient**
- Simple command-line operation
- Support for batch video processing
- Customizable processing parameters

## 🔧 Installation

Follow these steps to install **KLing-Video-WatermarkRemover-Enhancer**:

```bash
git clone --recursive https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer.git
conda create -n kling python=3.10
conda activate kling
pip install -r requirements.txt
```

## 🛠️ Configuration

The `config.yaml` file defines parameters for watermark removal and video enhancement.

### `Watermark Removal`
Parameters for watermark removal:

- `position: [556, 1233, 701, 1267]`
  - Defines the watermark area coordinates
  - Format: `(x1, y1, x2, y2)`, representing top-left `(556, 1233)` and bottom-right `(701, 1267)` coordinates
  - Used to determine the watermark region during processing

- `ckpt_p: "./weights/sttn.pth"`
  - Path to the watermark removal model weights
  - [sttn.pth](https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view?usp=sharing) is based on STTN (Spatio-Temporal Trajectory Network)

- `mask_expand: 30`
  - Pixel expansion of the watermark area
  - Ensures clean removal without artifacts

- `neighbor_stride: 10`
  - Stride size for temporal neighborhood computation
  - Controls sampling frequency of neighboring frames

### `Video Enhancement`
Parameters for video enhancement:

- **`RealESRGAN_model_path: "./weights/RealESRGAN_x2plus.pth"`**
  - Path to Real-ESRGAN model weights for video quality enhancement
  - More models available in Real-ESRGAN/inference_realesrgan.py
  - [RealESRGAN_x2plus.pth](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth)

- **`GFPGANer_model_path: "./weights/GFPGANv1.4.pth"`**
  - Path to GFPGAN model weights for facial enhancement
  - More models available in Real-ESRGAN/cog_predict.py
  - [GFPGANv1.4.pth](https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth)

## 🚀 Quick Start

Start enhancing your videos with just one command:

```bash
python main.py --input your_video.mp4 --remove-watermark --enhance-video
```

### 🎮 Common Usage Examples

```bash
# Remove watermark only
python main.py --input video.mp4 --remove-watermark

# Enhance video only
python main.py --input video.mp4 --enhance-video

# Process all videos in a folder
python main.py --input videos_folder --remove-watermark --enhance-video
```

## 📁 Project Structure

```
KLing-Video-WatermarkRemover-Enhancer/
├── 📄 main.py          # Main program entry
├── 📁 modules/         # Core function modules
├── 📁 utils/          # Utility functions
└── 📄 config.yaml     # Configuration file
```

## 🤝 References

- [STTN](https://github.com/researchmm/STTN) - Powerful video inpainting technology
- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - State-of-the-art video super-resolution solution

## 🌟 Support

If this project helps you, please consider giving it a star ⭐️
