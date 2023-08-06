from .lib import *
from .third_party.yolov5.utils.plots import Annotator as _Annotator
from colorsys import hsv_to_rgb

__all__ = ['pil2tensor', 'tensor2pil', 'tensor2ndarray', 'ndarray2tensor', 'read_img', 'write_img', 
           'Annotator', 'ValidPad']

pil2tensor = tv.transforms.ToTensor()
tensor2pil = tv.transforms.ToPILImage()


def tensor2ndarray(img: torch.Tensor):
    img = img.cpu().detach()
    if img.ndim == 4:
        img = img[0]
    img = img.mul(255).permute(1, 2, 0).numpy().astype(np.uint8)[..., ::-1]
    img = np.ascontiguousarray(img)
    return img


def ndarray2tensor(img: np.ndarray):
    img = img[..., ::-1]
    img = img.astype(np.float32) / 255
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).contiguous()
    return img


def read_img(path: str) -> torch.Tensor:
    return pil2tensor(Image.open(path).convert("RGB")).unsqueeze(0)


def write_img(img: torch.Tensor, path: str):
    tv.utils.save_image(img, path)


class Annotator(_Annotator):
    def __init__(self, im, line_width=None, font_size=None, font='Arial.ttf', pil=False, example='abc'):
        im = tensor2ndarray(im) if isinstance(im, torch.Tensor) else np.ascontiguousarray(im)
        super().__init__(im, line_width, font_size, font, pil, example)
        self.colorset = [
            (int(r*255), int(g*255), int(b*255)) for k in range(80) 
                for r, g, b in [hsv_to_rgb((k%20)/20, 0.5+(k//20)/8, 0.5+(k//20)/8)]
        ]
        random.seed(0)
        random.shuffle(self.colorset)
    
    def box_label(self, box, label, idx):
        color = self.colorset[idx]
        txt_color = (255, 255, 255)
        return super().box_label(box, label, color, txt_color)
    
    def box_label_all(self, pred):
        for *box, conf, cls in pred:
            cls = int(cls.item())
            conf = float(conf.item())
            label = f"{cls} {conf:.2f}"
            self.box_label(box, label, cls)

    def save(self, path):
        img = self.result()
        cv2.imwrite(path, img)


class ValidPad:
    def __init__(self, base=64) -> None:
        self.base = base
    
    def __call__(self, x:torch.Tensor) -> torch.Tensor:
        nc = x.shape[:-2]
        h, w = x.shape[-2:]
        h2 = (h+self.base-1)//self.base*self.base
        w2 = (w+self.base-1)//self.base*self.base
        x2 = torch.ones((*nc, h2, w2), device=x.device, dtype=x.dtype)
        x2[..., :h, :w] = x
        return x2
