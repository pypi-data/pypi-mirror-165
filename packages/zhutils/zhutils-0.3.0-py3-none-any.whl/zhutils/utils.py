from .lib import *

__all__ = ['pil2tensor', 'tensor2pil', 'read_img', 'write_img']

pil2tensor = tv.transforms.ToTensor()
tensor2pil = tv.transforms.ToPILImage()


def read_img(path: str) -> torch.Tensor:
    return pil2tensor(Image.open(path)).unsqueeze(0)


def write_img(img: torch.Tensor, path: str):
    tv.utils.save_image(img, path)
