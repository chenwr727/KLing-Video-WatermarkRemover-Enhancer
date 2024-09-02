import numpy as np
from PIL import Image


def load_img(img_p: str):
    img = Image.open(img_p)
    if img.mode == "RGBA":
        img = img.convert("RGB")
    return img


def load_img_to_array(img_p: str):
    return np.array(load_img(img_p))


def save_array_to_img(img_arr: np.ndarray, img_p: str):
    Image.fromarray(img_arr.astype(np.uint8)).save(img_p)
