from .lib import *
from collections import namedtuple

__all__ = ['OptCfg', 'EoTCfg', 'AdvPatch', 'EoT', 'FGSM', 'GPOptimizer']

OptCfg = namedtuple("OptCfg", ["optimizer", "learning_rate", "momentum"],
                    defaults=["FGSM", 1e-3, 0.9])
EoTCfg = namedtuple("EoTCfg", ["activate", "angle", "scale", "brightness"],
                    defaults=[True, 20.0, 0.8, 0.2])


class AdvPatch:
    def __init__(self, shape: Tuple[int, int], device: str, opt_cfg: OptCfg,
                 eot_cfg: EoTCfg):
        self.h = int(shape[0])
        self.w = int(shape[1])
        self.shape = [1, 3, self.h, self.w]
        self.device = device
        self.data = torch.rand(self.shape, device=device, requires_grad=True)

        self.opt_cfg = opt_cfg
        self.eot_cfg = eot_cfg
        self.pil2tensor = tv.transforms.ToTensor()

        if opt_cfg.optimizer == "FGSM":
            self.opt = FGSM(opt_cfg, self.data)
        else:
            self.opt = GPOptimizer(opt_cfg, self.data)
        self.eot = EoT(eot_cfg)

    def apply(self,
              img: torch.Tensor,
              pos: Tuple[int, int],
              eval: bool = False) -> torch.Tensor:
        if eval:
            self.eot.activate = False
        img = self.eot(img, self.data, pos)
        if eval:
            self.eot.activate = True
        return img

    def update(self, loss: torch.Tensor) -> None:
        loss.backward()
        self.opt()
        self.data.data.clamp_(0, 1)

    def random_pos(self, shape: torch.Size) -> Tuple[int, int]:
        h = random.randint(0, shape[-2] - self.h)
        w = random.randint(0, shape[-1] - self.w)
        return h, w

    def save(self, path: str):
        tv.utils.save_image(self.data, path)

    def load(self, path: str):
        self.data = self.pil2tensor(Image.open(path))
        self.data.data = self.data.unsqueeze(0).to(self.device)


class EoT:
    def __init__(self, eot_cfg: EoTCfg):
        self.activate = eot_cfg.activate
        self.angle = math.radians(eot_cfg.angle)
        self.scale = eot_cfg.scale
        self.color = tv.transforms.ColorJitter(brightness=eot_cfg.brightness)

    def __call__(self, img: torch.Tensor, x: torch.Tensor,
                 pos: Tuple[int, int]) -> torch.Tensor:
        h, w = x.shape[-2:]
        img_shape = img.shape[-2:]

        if self.activate:
            x = self.color(x)

            a = torch.FloatTensor(1).uniform_(-self.angle, self.angle)
            pre_scale = 1 / (torch.cos(a) + torch.sin(torch.abs(a)))
            pre_scale = pre_scale.item()
            min_scale = min(self.scale / pre_scale, 1.0)
            b = torch.FloatTensor(1).uniform_(min_scale, 1) * pre_scale

            t = -torch.ceil(torch.log2(b))
            t = 1 << int(t.item())
            if t > 1:
                size = (h // t, w // t)
                x = F.interpolate(x, size=size, mode="area")
                b *= t

            a = a.to(x.device)
            b = b.to(x.device)
            sin = torch.sin(a)
            cos = torch.cos(a)

            theta = torch.zeros((1, 2, 3), device=x.device)
            theta[:, 0, 0] = cos / b
            theta[:, 0, 1] = sin / b
            theta[:, 0, 2] = 0
            theta[:, 1, 0] = -sin / b
            theta[:, 1, 1] = cos / b
            theta[:, 1, 2] = 0

            size = torch.Size((1, 3, h // t, w // t))
            grid = F.affine_grid(theta, size, align_corners=False)
            x = F.grid_sample(x, grid, align_corners=False)

            rotate_mask = torch.ones(size, device=x.device)
            mask = F.grid_sample(rotate_mask, grid, align_corners=False)

            tw1 = (w - w // t) // 2
            tw2 = w - w // t - tw1
            th1 = (h - h // t) // 2
            th2 = h - h // t - th1

            pad = nn.ZeroPad2d(padding=(
                pos[1] + tw1,
                img_shape[1] - w - pos[1] + tw2,
                pos[0] + th1,
                img_shape[0] - h - pos[0] + th2,
            ))
        else:
            mask = torch.ones_like(x)
            pad = nn.ZeroPad2d(padding=(
                pos[1],
                img_shape[1] - w - pos[1],
                pos[0],
                img_shape[0] - h - pos[0],
            ))

        padding = torch.clamp(pad(x), 0, 1)
        mask = torch.clamp(pad(mask), 0, 1)
        return (1 - mask) * img + mask * padding


class FGSM:
    def __init__(self, opt_cfg: OptCfg, opt_tensor: torch.Tensor):
        """Fast Gradient Sign Method
        Support I-FGSM, MI-FGSM
        
        Args:
            opt_cfg (OptCfg): config the learning_rate and momentum
            opt_tensor (torch.Tensor): the tensor to be optimized
        """
        self.lr = opt_cfg.learning_rate
        self.m = opt_cfg.momentum
        self.t = opt_tensor
        self.h = torch.zeros_like(self.t)

    @torch.no_grad()
    def __call__(self):
        l1 = self.t.grad.abs().mean()
        if l1 == 0: l1 += 1
        self.h = self.h * self.m + self.t.grad / l1
        self.t.data -= self.lr * self.h.sign()
        self.t.grad.zero_()


class GPOptimizer:
    def __init__(self, opt_cfg: OptCfg, opt_tensor: torch.Tensor):
        """Wrapper of General Purposed Optimizer

        Args:
            opt_cfg (OptCfg): config the optimizer, learning_rate and momentum
            opt_tensor (torch.Tensor): the tensor to be optimized

        Raises:
            NotImplementedError: Only Support SGD and Adam
        """
        self.optimizer = opt_cfg.optimizer
        self.opt_tensor = [opt_tensor]
        if self.optimizer == "SGD":
            self.lr = opt_cfg.learning_rate
            self.m = opt_cfg.momentum
            self._opt = optim.SGD(self.opt_tensor, self.lr, self.m)
        elif self.optimizer == "Adam":
            self.lr = opt_cfg.learning_rate
            self._opt = optim.Adam(self.opt_tensor, self.lr)
        else:
            raise NotImplementedError

    def __call__(self):
        self._opt.step()
        self._opt.zero_grad()
