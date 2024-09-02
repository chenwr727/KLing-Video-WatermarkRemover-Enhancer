import glob
import os
import subprocess
from typing import List

TEMP_VIDEO_FILE = "tmp.mp4"
TEMP_FRAME_FORMAT = "png"


def run_ffmpeg(args: List[str]) -> bool:
    commands = ["ffmpeg", "-hide_banner", "-loglevel", "error"]
    commands.extend(args)
    try:
        subprocess.check_output(commands, stderr=subprocess.STDOUT)
        return True
    except Exception as e:
        print(str(e))
        pass
    return False


def detect_fps(target_path: str) -> float:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=r_frame_rate",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        target_path,
    ]
    output = subprocess.check_output(command).decode().strip().split("/")
    try:
        numerator, denominator = map(int, output)
        return numerator / denominator
    except Exception:
        pass
    return 30


def extract_frames(
    target_path: str, fps: float = 30, temp_frame_quality: int = 1
) -> bool:
    temp_directory_path = get_temp_directory_path(target_path)
    commands = [
        "-hwaccel",
        "auto",
        "-i",
        target_path,
        "-q:v",
        str(temp_frame_quality),
        "-pix_fmt",
        "rgb24",
        "-vf",
        "fps=" + str(fps),
        os.path.join(temp_directory_path, "%04d." + TEMP_FRAME_FORMAT),
    ]
    return run_ffmpeg(commands)


def create_video(
    target_path: str,
    output_path: str,
    fps: float = 30,
    output_video_encoder: str = "libx264",
) -> bool:
    temp_directory_path = get_temp_directory_path(target_path)

    commands = [
        "-hwaccel", "auto",
        "-r", str(fps),
        "-i", os.path.join(temp_directory_path, "%04d." + TEMP_FRAME_FORMAT),
        "-c:v", output_video_encoder,
        "-pix_fmt", "yuv420p",
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-y", output_path
    ]

    return run_ffmpeg(commands)


def get_temp_frame_paths(
    temp_directory_path: str, temp_frame_format: str = TEMP_FRAME_FORMAT
) -> List[str]:
    temp_frame_paths = glob.glob(
        (os.path.join(glob.escape(temp_directory_path), "*." + temp_frame_format))
    )
    temp_frame_paths.sort()
    return temp_frame_paths


def get_temp_directory_path(target_path: str) -> str:
    target_name, _ = os.path.splitext(os.path.basename(target_path))
    target_directory_path = os.path.dirname(target_path)
    temp_directory_path = os.path.join(target_directory_path, target_name)
    os.makedirs(temp_directory_path, exist_ok=True)
    return temp_directory_path
