from .lib import *
from torch.utils.data import random_split


def _gamma_correction(imgs: torch.Tensor, gamma: float) -> torch.Tensor:
    """模拟运动模糊过程中图像的gamma校正影响

    Args:
        imgs (torch.Tensor): 需要有多张不同平移的图像作为输入
        gamma (float): gamma校正系数，通常取2.2

    Returns:
        torch.Tensor: 考虑gamma校正后生成的模糊图像
    """
    n = imgs.shape[0]
    out = 0
    for img in imgs:
        # 从RGB到光
        out += (1e-6 + img)**gamma
    # 从光到RGB
    out = (1e-6 + out / n)**(1 / gamma)
    return out


def _sine_grid(div: int, device: str) -> torch.Tensor:
    """正弦运动采样格点

    Args:
        div (int): 总共格点数

    Returns:
        torch.Tensor: 表征半个正弦运动过程的格点
    """
    # 此处假设是从两峰之间的半周期运动
    grid = torch.linspace(-0.5 * math.pi, 0.5 * math.pi, div, device=device)
    grid = (torch.sin(grid) + 1) / 2
    return grid


def _stn_blur_linear(img: torch.Tensor, div: int, x: float, y: float,
                     blur_grid: torch.Tensor, mean_func: Callable,
                     device: str) -> torch.Tensor:
    """pytorch基于STN实现线性模糊的方法

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        div (int): 使用多少张图像叠加生成模糊效果
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        blur_grid (torch.Tensor): 不同运动方式的采样格点，线性或正弦
        mean_func (Callable): 不同的合成方式，平均或考虑gamma校正
    """
    ones = torch.ones_like(blur_grid, device=device)
    zeros = torch.zeros_like(blur_grid, device=device)
    x = x * blur_grid
    y = y * blur_grid
    affine_tensor = torch.stack([
        torch.stack([ones, zeros, x]),
        torch.stack([zeros, ones, y]),
    ]).permute(2, 0, 1)
    grid = F.affine_grid(affine_tensor, [div, *img.shape[1:]],
                         align_corners=False)
    imgs = img.unsqueeze(dim=1).expand(-1, div, -1, -1, -1)
    res = []
    for i in range(img.shape[0]):
        samples = F.grid_sample(imgs[i],
                                grid,
                                padding_mode="border",
                                align_corners=False)
        blur_img = mean_func(samples)
        res.append(blur_img)
    res = torch.cat(res, dim=0)
    return res


def stn_blur_2d(img: torch.Tensor, x: float, y: float, div: int,
                device: str) -> torch.Tensor:
    """使用STN实现的图像线性模糊效果，支持同时处理多张图像

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        div (int): 使用多少张图像叠加生成模糊效果
    """
    blur_grid = torch.linspace(0, 1, div, device=device)
    mean_func = lambda x: torch.mean(x, dim=0, keepdim=True)
    res = _stn_blur_linear(img, div, x, y, blur_grid, mean_func, device)
    return res


def stn_blur_2d_gamma(img: torch.Tensor,
                      x: float,
                      y: float,
                      div: int,
                      device: str,
                      gamma: float = 2.2) -> torch.Tensor:
    """使用STN实现的图像线性模糊效果，支持同时处理多张图像，考虑了gamma校正

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        div (int): 使用多少张图像叠加生成模糊效果
        gamma (float, optional): gamma校正系数，通常取2.2
    """
    blur_grid = torch.linspace(0, 1, div, device=device)
    mean_func = lambda x: _gamma_correction(x, gamma).unsqueeze(0)
    res = _stn_blur_linear(img, div, x, y, blur_grid, mean_func, device)
    return res


def stn_blur_2d_sin(img: torch.Tensor, x: float, y: float, div: int,
                    device: str) -> torch.Tensor:
    """使用STN实现的图像线性模糊效果，支持同时处理多张图像，考虑了半周期正弦运动

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        div (int): 使用多少张图像叠加生成模糊效果
    """
    blur_grid = _sine_grid(div, device)
    mean_func = lambda x: torch.mean(x, dim=0, keepdim=True)
    res = _stn_blur_linear(img, div, x, y, blur_grid, mean_func, device)
    return res


def stn_blur_2d_gamma_sin(img: torch.Tensor,
                          x: float,
                          y: float,
                          div: int,
                          device: str,
                          gamma: float = 2.2) -> torch.Tensor:
    """使用STN实现的图像线性模糊效果，支持同时处理多张图像，考虑了半周期正弦运动和gamma校正

    Args:
        img (torch.Tensor): 维度为4，支持多组图像
        x (float): x轴水平移动，取值范围为[-1, 1]
        y (float): y轴竖直移动，取值范围为[-1, 1]
        div (int): 使用多少张图像叠加生成模糊效果
        gamma (float, optional): gamma校正系数，通常取2.2
    """
    blur_grid = _sine_grid(div, device)
    mean_func = lambda x: _gamma_correction(x, gamma).unsqueeze(0)
    res = _stn_blur_linear(img, div, x, y, blur_grid, mean_func, device)
    return res


def load_imagenet_preprocess() -> tv.transforms.Normalize:
    """加载imagenet的归一化函数
    """
    return tv.transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    )


def load_imagenet_val(dataset: str,
                      batch_size: int = 1,
                      size: int = 50000,
                      shuffle: bool = True,
                      inc: bool = False) -> DataLoader:
    """加载ImageNet验证集

    Args:
        dataset (str): 存放数据集的位置，该位置下应该存在1000个文件夹，序号从0~999，存放各类图片
        size (int, optional): 所要加载的数据集大小，最大不超过50000，采用随机切分方法. Defaults to 50000.
        shuffle (bool, optional): 是否打乱加载顺序. Defaults to True.
        inc (bool, optional): 是否是Inception格式（299*299），默认是224*224. Defaults to False.
    """
    imagenet = tv.datasets.ImageFolder(dataset,
                                       transform=tv.transforms.Compose([
                                           tv.transforms.Resize(299),
                                           tv.transforms.CenterCrop(
                                               (299, 299)),
                                           tv.transforms.ToTensor(),
                                       ]) if inc else tv.transforms.Compose([
                                           tv.transforms.Resize(256),
                                           tv.transforms.CenterCrop(
                                               (224, 224)),
                                           tv.transforms.ToTensor(),
                                       ]))
    if size != 50000:
        partial = [size, 50000 - size]
        imagenet, _ = random_split(imagenet, partial)
    return DataLoader(
        imagenet,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=5 if batch_size >= 10 else 0,
    )


def read_img(path: str, device: str, crop_size: int = None) -> torch.Tensor:
    """加载单张图像

    Args:
        path (str): 图像所存储的路径
        crop_size (int, optional): 中心裁剪尺寸，默认是原图
    """
    if crop_size is None:
        tr = tv.transforms.ToTensor()
    else:
        tr = tv.transforms.Compose([
            tv.transforms.Resize(crop_size),
            tv.transforms.CenterCrop((crop_size, crop_size)),
            tv.transforms.ToTensor(),
        ])
    return tr(Image.open(path)).unsqueeze(0).to(device)


class ImageOnlyLoader:
    def __init__(self,
                 glob_path: str,
                 transform: Callable,
                 shuffle: bool = True) -> None:
        """一个仅输出图像的简易加载器，所要加载的图像依赖`glob`库进行索引

        Args:
            glob_path (str): glob匹配字符
            transform (Callable): 对转为Tensor格式后的原图片的预处理函数
            shuffle (bool, optional): 是否打乱加载顺序. Defaults to True.
        """
        self.img_names = sorted(glob(glob_path))
        self.length = len(self.img_names)
        self.shuffle = shuffle
        if self.shuffle:
            random.shuffle(self.img_names)
        self.pil2tensor = tv.transforms.ToTensor()
        self.transform = transform

    def __getitem__(self, key: int) -> torch.Tensor:
        img = self.transform(self.pil2tensor(Image.open(
            self.img_names[key]))).unsqueeze(dim=0)
        # deal with gray images
        if img.shape[1] == 1:
            img = torch.cat([img] * 3, dim=1)
        return img

    def __len__(self) -> int:
        return self.length


class MIFGSM(nn.Module):
    def __init__(self, m: float, lr: float):
        """MI-FGSM的简单实现

        Args:
            m (float): 动量项，取值范围为[0, 1]
            lr (float): 每次更新步长
        """
        super().__init__()
        self.m = m
        self.lr = lr
        self.h = 0

    @torch.no_grad()
    def forward(self, t: torch.Tensor) -> None:
        """对已经求得梯度的张量进行原地更新

        Args:
            t (torch.Tensor): 待更新的张量
        """
        l1 = t.grad.abs().mean()
        if l1 == 0:
            l1 += 1
        self.h = self.h * self.m + t.grad / l1
        t.data -= self.lr * self.h.sign()
        t.grad.zero_()


class TPatch:
    def __init__(self,
                 h: int,
                 w: int,
                 device: str = "cpu",
                 lr: float = 1 / 255,
                 momentum: float = 0.9,
                 eot: bool = False,
                 eot_angle: float = math.pi / 9,
                 eot_scale: float = 0.8,
                 p: float = 0.5):
        """虽然叫TPatch，其实是AdvPatch的实现，默认使用MI-FGSM优化

        Args:
            h (int): patch的竖边
            w (int): patch的横边
            lr (float, optional): 更新步长. Defaults to 1/255.
            momentum (float, optional): 动量项. Defaults to 0.9.
            eot (bool, optional): 是否进行EoT变换. Defaults to False.
            eot_angle (float, optional): EoT的旋转角度，这里是范围的一半. Defaults to math.pi/9.
            eot_scale (float, optional): EoT的缩放尺寸. Defaults to 0.8.
            p (float, optional): 以一定概率随机进行EoT. Defaults to 0.5.
        """
        if eot:
            assert h == w, "只实现了正方形的EoT"
            self.robust = EoT(angle=eot_angle, scale=eot_scale, p=p)
        self.eot = eot
        self.w = int(w)
        self.h = int(h)
        self.shape = [1, 3, self.h, self.w]
        self.device = device
        self.data = torch.rand(self.shape, device=device, requires_grad=True)
        self.opt = MIFGSM(m=momentum, lr=lr)
        self.pil2tensor = tv.transforms.ToTensor()
        self.last_scale = 1.0

    def apply(self,
              img: torch.Tensor,
              pos: Tuple[int, int],
              test_mode: bool = False,
              set_rotate: float = None,
              set_resize: float = None,
              transform: Callable = None) -> torch.Tensor:
        """把patch放到img上

        Args:
            img (torch.Tensor): 背景图像
            pos (Tuple[int, int]): 用于放置的左上角位置坐标，注意这里不是真实坐标
            test_mode (bool, optional): 测试模式开关，用于固定旋转/尺寸进行测试. Defaults to False.
            set_rotate (float, optional): 固定旋转. Defaults to None.
            set_resize (float, optional): 固定尺寸. Defaults to None.
            transform (Callable, optional): 用于特殊的数值变换. Defaults to None.
        """
        assert len(pos) == 2, "pos should be (x, y)"
        if self.eot:
            if test_mode:
                switch, padding, _ = self.robust(self,
                                                 pos,
                                                 img.shape[-2:],
                                                 do_random_rotate=False,
                                                 do_random_color=False,
                                                 do_random_resize=False,
                                                 set_rotate=set_rotate,
                                                 set_resize=set_resize)
            else:
                switch, padding, self.last_scale = self.robust(
                    self, pos, img.shape[-2:])
        else:
            switch, padding = self.mask(img.shape, pos)
        if transform:
            padding = transform(padding)
        return (1 - switch) * img + switch * padding

    def update(self, loss: torch.Tensor) -> None:
        """输入loss，更新patch

        Args:
            loss (torch.Tensor): 可以反传梯度的张量
        """
        loss.backward()
        self.opt(self.data)
        self.data.data.clamp_(0, 1)

    def mask(self, shape: torch.Size,
             pos: Tuple[int, int]) -> Tuple[torch.Tensor, torch.Tensor]:
        """产生一个简单的非EoT的mask，其中1代表属于patch的像素，0代表属于img的像素

        Args:
            shape (torch.Size): 背景图像尺寸
            pos (Tuple[int, int]): 放置的左上角坐标

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: 一个mask和做完padding的patch
        """
        mask = torch.zeros(shape, dtype=torch.float, device=self.device)
        mask[..., pos[0]:pos[0] + self.h, pos[1]:pos[1] + self.w] = 1
        padding = torch.zeros(shape, dtype=torch.float, device=self.device)
        padding[..., pos[0]:pos[0] + self.h,
                pos[1]:pos[1] + self.w] = self.data
        return mask, padding

    def random_pos(self, shape: torch.Size) -> Tuple[int, int]:
        """用于获取一个合法的随机放置位置

        Args:
            shape (torch.Size): 背景图像尺寸

        Returns:
            Tuple[int, int]: 位置坐标，(h, w)格式
        """
        h = random.randint(0, shape[-2] - self.h)
        w = random.randint(0, shape[-1] - self.w)
        return h, w

    def save(self, path: str):
        """保存patch
        """
        tv.utils.save_image(self.data, path)

    def load(self, path: str):
        """加载patch
        """
        self.data = self.pil2tensor(Image.open(path))
        self.data = self.data.unsqueeze(0).to(self.device)
        self.data.requires_grad_()
        self.shape = list(self.data.shape)
        _, _, self.h, self.w = self.shape


class EoT(nn.Module):
    def __init__(self, angle=math.pi / 9, scale=0.8, p=0.5):
        """EoT模块

        Args:
            angle ([type], optional): 旋转角度，这里是范围的一半. Defaults to math.pi/9.
            scale (float, optional): 缩放尺寸范围. Defaults to 0.8.
            p (float, optional): 以一定概率随机进行EoT. Defaults to 0.5.
        """
        super(EoT, self).__init__()
        self.angle = angle
        self.scale = scale
        self.p = p
        self.color = tv.transforms.ColorJitter(brightness=0.2)

    def forward(self,
                patch: TPatch,
                pos: Tuple[int, int],
                img_shape: Tuple[int, int],
                do_random_rotate=True,
                do_random_color=True,
                do_random_resize=True,
                set_rotate=None,
                set_resize=None) -> Tuple[torch.Tensor, torch.Tensor, float]:
        """获取旋转的mask

        Args:
            pos (Tuple[int, int]): 放置的左上角坐标
            img_shape (Tuple[int, int]): 背景图像尺寸
            do_random_rotate (bool, optional): 随机旋转开关. Defaults to True.
            do_random_color (bool, optional): 随机色差开关. Defaults to True.
            do_random_resize (bool, optional): 随机尺寸开关. Defaults to True.
            set_rotate ([type], optional): 设定固定旋转. Defaults to None.
            set_resize ([type], optional): 设定固定尺寸. Defaults to None.

        Returns:
            Tuple[torch.Tensor, torch.Tensor, float]: 一个mask和做完padding的patch，以及随机resize的数值，常用于detector的框位置的确定
        """
        # 以一定概率EoT来稳定训练
        if torch.rand(1) > self.p:
            do_random_rotate = False
            do_random_color = False
            do_random_resize = False

        if do_random_color:
            img = self.color(patch.data)
        else:
            img = patch.data

        if do_random_rotate:
            angle = torch.FloatTensor(1).uniform_(-self.angle, self.angle)
        elif set_rotate is None:
            angle = torch.zeros(1)
        else:
            angle = torch.full((1, ), set_rotate)

        # ! 动态解决旋转带来的超出区域问题
        pre_scale = 1 / (torch.cos(angle) + torch.sin(torch.abs(angle)))
        pre_scale = pre_scale.item()

        if do_random_resize:
            min_scale = min(self.scale / pre_scale, 1.0)
            scale_ratio = torch.FloatTensor(1).uniform_(min_scale, 1)
        elif set_resize is None:
            scale_ratio = torch.ones(1)
        else:
            scale_ratio = torch.full((1, ), set_resize)

        # ! 这里实现并不完美，现在是先平均降采样，再双线性插值，目的是避免出现仅关注几个点的问题
        scale = scale_ratio * pre_scale
        logging.debug(
            f"scale_ratio: {scale_ratio.item():.2f}, "
            f"angle: {angle.item():.2f}, pre_scale: {pre_scale:.2f}, "
            f"scale: {scale.item():.2f}, ")

        t = -torch.ceil(torch.log2(scale))
        t = 1 << int(t.item())
        if t > 1:
            size = (patch.h // t, patch.w // t)
            img = F.interpolate(img, size=size, mode="area")
            scale *= t

        angle = angle.to(patch.device)
        scale = scale.to(patch.device)
        sin = torch.sin(angle)
        cos = torch.cos(angle)

        theta = torch.zeros((1, 2, 3), device=patch.device)
        theta[:, 0, 0] = cos / scale
        theta[:, 0, 1] = sin / scale
        theta[:, 0, 2] = 0
        theta[:, 1, 0] = -sin / scale
        theta[:, 1, 1] = cos / scale
        theta[:, 1, 2] = 0

        size = torch.Size((1, 3, patch.h // t, patch.w // t))
        grid = F.affine_grid(theta, size, align_corners=False)
        output = F.grid_sample(img, grid, align_corners=False)

        # * 利用grid_sample的zero填充来实现对应mask的生成
        rotate_mask = torch.ones(size, device=patch.device)
        mask = F.grid_sample(rotate_mask, grid, align_corners=False)

        tw1 = (patch.w - patch.w // t) // 2
        tw2 = patch.w - patch.w // t - tw1
        th1 = (patch.h - patch.h // t) // 2
        th2 = patch.h - patch.h // t - th1

        pad = nn.ZeroPad2d(padding=(
            pos[1] + tw1,
            img_shape[1] - patch.w - pos[1] + tw2,
            pos[0] + th1,
            img_shape[0] - patch.h - pos[0] + th2,
        ))
        mask = pad(mask)
        padding = pad(output)
        mask = torch.clamp(mask, 0, 1)

        return mask, padding, scale_ratio.item()


class TVLoss(nn.Module):
    def __init__(self) -> None:
        """Total Variation，通常用于衡量图像色彩连续程度
        """
        super().__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """直接当函数使用

        Args:
            x (torch.Tensor): 输入图像，支持3或4维格式

        Returns:
            torch.Tensor: TV loss
        """
        lr = torch.abs(x[..., :, 1:] - x[..., :, :-1]).mean()
        tb = torch.abs(x[..., 1:, :] - x[..., :-1, :]).mean()
        return lr + tb


class ContentLoss(nn.Module):
    def __init__(self,
                 extractor: nn.Module,
                 ref_fp: str,
                 device: str,
                 extract_layer=20) -> None:
        """计算内容损失，内容损失指神经网络对两张图像所提取特征间距离

        Args:
            extractor (nn.Module): 用于提取的训练好的卷积神经网络，例如vgg网络的backbone
            ref_fp (str): 参考图像的路径
            extract_layer (int, optional): 所参照的第几层特征. Defaults to 20.
        """
        super().__init__()
        self.extractor = extractor
        self.content_hook = extract_layer
        self.preprocess = load_imagenet_preprocess()
        self.resize = tv.transforms.Compose([
            tv.transforms.Resize([224, 224], interpolation=Image.BICUBIC),
            tv.transforms.ToTensor(),
        ])
        self.ref = self.resize(Image.open(ref_fp))[:3]
        self.ref = self.ref.unsqueeze(0).to(device)
        self.ref = self.get_content_layer(self.ref).detach()
        self.upsample = nn.Upsample(size=(224, 224), mode="bilinear")

    def get_content_layer(self, x: torch.Tensor) -> torch.Tensor:
        """提取第几层的特征结果

        Args:
            x (torch.Tensor): 输入图像

        Returns:
            torch.Tensor: 所要的特征向量
        """
        x = self.preprocess(x)
        for i, m in enumerate(self.extractor.children()):
            x = m(x)
            if i == self.content_hook:
                break
        return x

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """计算内容损失

        Args:
            x (torch.Tensor): 与参考图像对比的图像

        Returns:
            torch.Tensor: 内容损失
        """
        x = self.upsample(x)
        x = self.get_content_layer(x)
        loss = F.mse_loss(x, self.ref)
        return loss


def compute_iou(bboxes_a: torch.Tensor,
                bboxes_b: torch.Tensor,
                xyxy: bool = True) -> torch.Tensor:
    """计算多个框与多个框的交并面积比，两者需要统一坐标格式

    Args:
        bboxes_a (torch.Tensor): shape==n*4的框
        bboxes_b (torch.Tensor): shape==m*4的框
        xyxy (bool, optional): xyxy格式或者xywh格式. Defaults to True.

    Returns:
        torch.Tensor: n*m格式的交并比
    """
    if xyxy:
        tl = torch.max(bboxes_a[:, None, :2], bboxes_b[:, :2])
        br = torch.min(bboxes_a[:, None, 2:], bboxes_b[:, 2:])
        area_a = torch.prod(bboxes_a[:, 2:] - bboxes_a[:, :2], 1)
        area_b = torch.prod(bboxes_b[:, 2:] - bboxes_b[:, :2], 1)
    else:
        tl = torch.max((bboxes_a[:, None, :2] - bboxes_a[:, None, 2:] / 2),
                       (bboxes_b[:, :2] - bboxes_b[:, 2:] / 2))
        br = torch.min((bboxes_a[:, None, :2] + bboxes_a[:, None, 2:] / 2),
                       (bboxes_b[:, :2] + bboxes_b[:, 2:] / 2))
        area_a = torch.prod(bboxes_a[:, 2:], 1)
        area_b = torch.prod(bboxes_b[:, 2:], 1)

    logging.debug(f"shape of tl or br: {tl.shape.__repr__()}")
    logging.debug(f"shape of area a: {area_a.shape.__repr__()}")

    en = (tl < br).type(tl.type()).prod(dim=2)
    area_i = torch.prod(br - tl, 2) * en  # * ((tl < br).all())
    area_u = area_a[:, None] + area_b - area_i
    iou = area_i / area_u
    return iou
