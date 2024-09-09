import sys

sys.path.insert(0, "./Real-ESRGAN")

import threading
import warnings
from typing import Any, Callable, List

import cv2
import numpy
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from tqdm import tqdm

from gfpgan import GFPGANer
from modules import CONFIG

warnings.filterwarnings("ignore", category=UserWarning)

Frame = numpy.ndarray[Any, Any]


FACE_ENHANCER = None
THREAD_SEMAPHORE = threading.Semaphore()
THREAD_LOCK = threading.Lock()


def get_face_enhancer():
    """
    Global function to obtain the face enhancer instance.

    This function ensures thread safety using a lock and checks if the face enhancer (FACE_ENHANCER) instance has already been created.
    """
    global FACE_ENHANCER

    with THREAD_LOCK:
        if FACE_ENHANCER is None:
            model = RRDBNet(
                num_in_ch=3,
                num_out_ch=3,
                num_feat=64,
                num_block=23,
                num_grow_ch=32,
                scale=2,
            )

            upsampler = RealESRGANer(
                scale=2,
                model_path=CONFIG["enhance"]["RealESRGAN_model_path"],
                dni_weight=None,
                model=model,
                tile=0,
                tile_pad=10,
                pre_pad=0,
                half=False,
                gpu_id=0,
            )

            FACE_ENHANCER = GFPGANer(
                model_path=CONFIG["enhance"]["GFPGANer_model_path"],
                upscale=2,
                arch="clean",
                channel_multiplier=2,
                bg_upsampler=upsampler,
            )
    return FACE_ENHANCER


def enhance_frame(temp_frame: Frame) -> Frame:
    """
    Enhance the quality of a given face image.

    This function uses a face enhancer to process the given frame, ensuring that the enhanced face image is properly aligned and integrated back into the original image context.

    Parameters:
    temp_frame (Frame): The temporary frame object, representing the face image that needs to be enhanced.

    Returns:
    Frame: The processed frame object, containing the enhanced face image.
    """
    _, _, output = get_face_enhancer().enhance(
        temp_frame, has_aligned=False, only_center_face=False, paste_back=True
    )
    return output


def enhance_frames(
    temp_frame_paths: List[str], update: Callable[[], None] = None
) -> None:
    """
    Process a series of temporary frame files.

    Parameters:
    - temp_frame_paths: A list of strings containing the file paths of the frames to be processed.
    - update: An optional callback function with no arguments for updating progress during processing.

    Returns:
    None
    """
    for temp_frame_path in tqdm(temp_frame_paths, desc="Enhancing: "):
        temp_frame = cv2.imread(temp_frame_path, cv2.IMREAD_UNCHANGED)
        result = enhance_frame(temp_frame)
        cv2.imwrite(temp_frame_path, result)
        if update:
            update()
