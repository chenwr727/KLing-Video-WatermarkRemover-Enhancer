import concurrent.futures
from typing import List

import cv2
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm

from modules import CONFIG
from modules.sttn import build_sttn_model, inpaint_video_with_builded_sttn
from utils.image_utils import load_img


@torch.no_grad()
def inpaint_video(
    paths: List[str],
    frames: List[Image.Image],
    masks: List[Image.Image],
    neighbor_stride: int,
    ckpt_p="./sttn/checkpoints/sttn.pth",
):
    """
    Inpaint missing parts in a video sequence using the STTN model.

    Parameters:
    - paths: A list of file paths for each frame in the video.
    - frames: A list of frame images, where missing parts are to be inpainted.
    - masks: A list of mask images corresponding to the frames, indicating the areas to be inpainted.
    - neighbor_stride: The stride size for selecting neighboring frames in the inpainting process.
    - ckpt_p: The file path for loading the pre-trained STTN model parameters.

    Returns:
    - results: A list of inpainted frame images.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # build sttn model
    model = build_sttn_model(ckpt_p, device)

    results = []

    results = inpaint_video_with_builded_sttn(
        model, paths, frames, masks, neighbor_stride, device
    )

    return results


def inpaint_imag(mask_result: List[tuple]):
    """
    Process image frames using multithreading.

    This function creates a thread pool using `concurrent.futures.ThreadPoolExecutor`
    and displays a progress bar using `tqdm`. This approach significantly improves
    the efficiency of image processing, especially when dealing with a large number
    of frames.

    Parameters:
    - mask_result: A list containing tuples representing each frame.

    Returns:
    - This function does not return any value.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(
            tqdm(
                executor.map(process_frame, mask_result),
                total=len(mask_result),
                desc="Save Image",
            )
        )
    return None


def process_frame(value: tuple):
    """
    Process and save a single video frame.

    Given a tuple containing the file path and frame data, this function saves the frame data as an image file.
    This is particularly useful in video processing or saving image sequences.

    Parameters:
        value (tuple): A tuple where the first element is the file path to save the frame and the second element is the frame data as a numpy array.
    """
    frame_path, comp_frame = value
    Image.fromarray(np.uint8(comp_frame)).save(frame_path)


def extract_mask(
    frame_paths: List[str],
    position: List[int],
    mask_expand: int = 20,
):
    """
    Extracts masks from each frame based on the given frame paths and position.

    Parameters:
    - frame_paths: A list of frame file paths.
    - position: The target region's position, represented as [xmin, ymin, xmax, ymax].
    - mask_expand: The pixel width to expand the mask, default is 20.

    Returns:
    - frames_list: A list of original frames.
    - masks_list: A list of corresponding masks for each frame.
    """
    frames_list = []
    masks_list = []
    xmin, ymin, xmax, ymax = position
    for frame_path in tqdm(frame_paths, desc="Set Mask"):
        image = load_img(frame_path)
        mask = np.zeros(image.size[::-1], dtype="uint8")
        cv2.rectangle(
            mask,
            (max(0, xmin - mask_expand), max(0, ymin - mask_expand)),
            (
                min(xmax + mask_expand, image.size[0] - 1),
                min(ymax + mask_expand, image.size[1] - 1),
            ),
            (255, 255, 255),
            thickness=-1,
        )
        mask = Image.fromarray(mask)

        frames_list.append(image)
        masks_list.append(mask)

    return frames_list, masks_list


def remove_watermark(frame_paths: List[str]):
    """
    Remove watermark from video frames.

    This function removes watermarks by extracting masks and inpainting the affected areas using surrounding pixels.

    Parameters:
    - frame_paths: A list of file paths to the video frames.
    - config: A dictionary containing watermark position, mask expansion, neighbor stride, and checkpoint path.

    Returns:
    None. The function modifies the video frames in place.
    """
    frames_list, masks_list = extract_mask(
        frame_paths, CONFIG["watermark"]["position"], CONFIG["watermark"]["mask_expand"]
    )
    results = inpaint_video(
        frame_paths,
        frames_list,
        masks_list,
        CONFIG["watermark"]["neighbor_stride"],
        CONFIG["watermark"]["ckpt_p"],
    )
    inpaint_imag(results)
