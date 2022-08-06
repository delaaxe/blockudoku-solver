import pathlib

import skimage
import PIL


def latest_airdropped_screenshot(index=-1):
    folder = pathlib.Path.home() / "Downloads"
    paths = [path for glob in ["IMG_*.jpeg", "IMG_*.PNG"] for path in folder.glob(glob)]
    path = sorted(paths, key=lambda path: path.stat().st_ctime)[index]
    return skimage.io.imread(path)[:, :, :3]


def display(img):
    image = PIL.Image.fromarray(img)
    return image.resize((image.width // 3, image.height // 3))

