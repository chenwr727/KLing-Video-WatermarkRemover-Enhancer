import argparse
import os
import shutil

from modules.enhance import enhance_frames
from modules.erase import remove_watermark
from utils.logging_utils import update_status
from utils.video_utils import (
    create_video,
    detect_fps,
    extract_frames,
    get_temp_directory_path,
    get_temp_frame_paths,
)


def process_video(
    input_path: str,
    output_path: str,
    remove_watermark_flag: bool,
    enhance_video_flag: bool,
):
    update_status(f"Start! {input_path}")
    file_name, _ = os.path.splitext(input_path)
    fps = detect_fps(input_path)

    update_status(f"Source: extracting frames with {fps} FPS...")
    extract_frames(input_path, fps)
    temp_directory_path = get_temp_directory_path(input_path)
    frame_paths = get_temp_frame_paths(temp_directory_path)

    if remove_watermark_flag:
        update_status("Erase: removing watermark...")
        remove_watermark(frame_paths)

    if enhance_video_flag:
        update_status("Enhance: video enhancement...")
        enhance_frames(frame_paths)

    update_status("Create video")
    create_video(input_path, output_path, fps)

    if os.path.exists(file_name):
        shutil.rmtree(file_name)
        update_status("Temporary request directory {} deleted".format(file_name))

    update_status(f"Done! {input_path}")


def process_input(
    input_path: str, remove_watermark_flag: bool, enhance_video_flag: bool
):
    if not remove_watermark_flag and not enhance_video_flag:
        print("No operation selected.")
        return
    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith((".mp4", ".avi", ".mkv")):
                input_file = os.path.join(input_path, filename)
                output_file = os.path.join(input_path, f"enhanced_{filename}")
                process_video(
                    input_file, output_file, remove_watermark_flag, enhance_video_flag
                )
    elif os.path.isfile(input_path):
        output_path = os.path.splitext(input_path)[0] + "_enhanced.mp4"
        process_video(
            input_path, output_path, remove_watermark_flag, enhance_video_flag
        )
    else:
        print(f"Invalid input path: {input_path}")


def main():
    parser = argparse.ArgumentParser(
        description="KLing-Video-WatermarkRemover-Enhancer"
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Input video file or directory"
    )
    parser.add_argument(
        "--remove-watermark", action="store_true", help="Enable watermark removal"
    )
    parser.add_argument(
        "--enhance-video", action="store_true", help="Enable video enhancement"
    )

    args = parser.parse_args()

    process_input(args.input, args.remove_watermark, args.enhance_video)


if __name__ == "__main__":
    main()
