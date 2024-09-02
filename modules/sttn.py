import sys

sys.path.insert(0, "./STTN")

from typing import List

import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

from STTN.core.utils import Stack, ToTorchFormatTensor
from STTN.model import sttn

_to_tensors = transforms.Compose([Stack(), ToTorchFormatTensor()])


def get_ref_index(neighbor_ids, length):
    """
    Generate a list of reference indices based on the provided neighbor IDs and length.

    This function iterates through a range up to the specified length, selecting indices
    that are not present in the neighbor IDs list as reference points.
    
    Parameters:
    - neighbor_ids (list): A list of integer IDs representing neighboring positions.
    - length (int): The total length or range to consider for generating reference indices.

    Returns:
    - ref_index (list): A list of integers representing the selected reference indices.
    """
    ref_length = 20
    ref_index = []
    for i in range(0, length, ref_length):
        if not i in neighbor_ids:
            ref_index.append(i)
    return ref_index


def build_sttn_model(ckpt_p: str, device="cuda"):
    """
    Builds the STTN model.

    Parameters:
    ckpt_p (str): Path to the model checkpoint file.
    device (str): Device to run the model on, default is "cuda".

    Returns:
    model: The loaded STTN model ready for evaluation.
    """
    model = sttn.InpaintGenerator().to(device)
    data = torch.load(ckpt_p, map_location=device)
    model.load_state_dict(data["netG"])
    model.eval()
    return model


@torch.no_grad()
def inpaint_video_with_builded_sttn(
    model,
    paths: List[str],
    frames: List[Image.Image],
    masks: List[Image.Image],
    neighbor_stride: int = 10,
    device="cuda",
) -> List[Image.Image]:
    """
    Inpaints missing parts of video frames using a pre-trained STTN model.

    Parameters:
    - model: Pre-trained STTN model for frame inpainting.
    - paths: List of file paths corresponding to each frame.
    - frames: List of original video frames as PIL images.
    - masks: List of masks indicating the regions to be inpainted.
    - neighbor_stride: Stride for selecting neighboring frames.
    - device: Device for computation (e.g., 'cuda', 'cpu').

    Returns:
    - List of tuples containing the path and the inpainted frame as a numpy array.
    """
    w, h = 432, 240
    video_length = len(frames)

    feats = [frame.resize((w, h)) for frame in frames]
    feats = _to_tensors(feats).unsqueeze(0) * 2 - 1
    _masks = [mask.resize((w, h), Image.NEAREST) for mask in masks]
    _masks = _to_tensors(_masks).unsqueeze(0)

    feats, _masks = feats.to(device), _masks.to(device)
    comp_frames = [None] * video_length

    feats = (feats * (1 - _masks).float()).view(video_length, 3, h, w)
    feats = model.encoder(feats)
    _, c, feat_h, feat_w = feats.size()
    feats = feats.view(1, video_length, c, feat_h, feat_w)

    # completing holes by spatial-temporal transformers
    for f in tqdm(
        range(0, video_length, neighbor_stride), desc="Inpaint Image", leave=False
    ):
        neighbor_ids = list(
            range(
                max(0, f - neighbor_stride), min(video_length, f + neighbor_stride + 1)
            )
        )
        ref_ids = get_ref_index(neighbor_ids, video_length)

        pred_feat = model.infer(
            feats[0, neighbor_ids + ref_ids, :, :, :],
            _masks[0, neighbor_ids + ref_ids, :, :, :],
        )
        pred_img = model.decoder(pred_feat[: len(neighbor_ids), :, :, :])
        pred_img = torch.tanh(pred_img)
        pred_img = (pred_img + 1) / 2
        pred_img = pred_img.permute(0, 2, 3, 1) * 255
        for i in range(len(neighbor_ids)):
            idx = neighbor_ids[i]
            b_mask = _masks.squeeze()[idx].unsqueeze(-1)
            b_mask = (b_mask != 0).int()
            frame = torch.from_numpy(np.array(frames[idx].resize((w, h))))
            frame = frame.to(device)
            img = pred_img[i] * b_mask + frame * (1 - b_mask)
            img = img.cpu().numpy()
            if comp_frames[idx] is None:
                comp_frames[idx] = img
            else:
                comp_frames[idx] = comp_frames[idx] * 0.5 + img * 0.5

    result = []
    ori_w, ori_h = frames[0].size
    for idx in tqdm(range(len(frames)), desc="Restore Image", leave=False):
        frame = np.array(frames[idx])
        b_mask = np.uint8(np.array(masks[idx])[..., np.newaxis] != 0)
        comp_frame = np.uint8(comp_frames[idx])
        comp_frame = Image.fromarray(comp_frame).resize((ori_w, ori_h))
        comp_frame = np.array(comp_frame)
        comp_frame = comp_frame * b_mask + frame * (1 - b_mask)
        result.append([paths[idx], comp_frame])
    return result
