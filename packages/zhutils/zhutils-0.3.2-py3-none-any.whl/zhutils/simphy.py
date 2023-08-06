from .lib import *
from .vis import get_new_name, get_new_extension
from string import ascii_uppercase


def _ascii_mask():
    mask = np.zeros((64, 64, 3), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_COMPLEX
    fontsize = 0.5
    white = (255, 255, 255)
    bold = 2
    text = ascii_uppercase[:5]
    mask = cv2.putText(mask, text, (4, 16), font, fontsize, white, bold)
    text = ascii_uppercase[5:10]
    mask = cv2.putText(mask, text, (4, 30), font, fontsize, white, bold)
    text = ascii_uppercase[10:15]
    mask = cv2.putText(mask, text, (4, 44), font, fontsize, white, bold)
    text = ascii_uppercase[15:20]
    mask = cv2.putText(mask, text, (4, 58), font, fontsize, white, bold)
    return mask


def _test_colors():
    colors = []
    for i in range(0, 256, 17):
        for j in range(0, 256, 17):
            for k in range(0, 256, 17):
                colors.append((i, j, k))
    return colors


def _train(model, metric, opt, sch, loader, epoch, device):
    for i in range(epoch):
        log_loss = 0
        for src, dst in loader:
            src, dst = src.to(device), dst.to(device)
            pred = model(src)
            loss = metric(pred, dst)
            opt.zero_grad()
            loss.backward()
            opt.step()
            log_loss += loss.detach()
        sch.step()
        print(i, log_loss)


def smooth_color():
    patch = np.zeros((64, 64, 3), dtype=np.uint8)
    for r in range(16):
        for g in range(16):
            for b in range(16):
                starth = r // 4
                startl = r % 4
                if starth % 2 == 0:
                    if startl % 2 == 0:
                        c = (r * 17, g * 17, b * 17)
                    else:
                        c = (r * 17, g * 17, (15 - b) * 17)
                else:
                    if startl % 2 == 0:
                        c = (r * 17, (15 - g) * 17, b * 17)
                    else:
                        c = (r * 17, (15 - g) * 17, (15 - b) * 17)
                patch[starth * 16 + g, startl * 16 + b] = c
    return patch


def sift_align(sim, phy, save_path=None):
    _h, _w = sim.shape[:2]
    bgr1 = cv2.resize(sim, (_w * 8, _h * 8), interpolation=cv2.INTER_NEAREST)
    bgr2 = phy

    img1 = cv2.cvtColor(bgr1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(bgr2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    patch = None
    MINIMAL_POINTS = 10
    if len(good) < MINIMAL_POINTS:
        if save_path is not None:
            img_match = cv2.drawMatches(img1, kp1, img2, kp2, good, None)
            name = get_new_name(save_path, "fail")
            cv2.imwrite(name, img_match)
        print(f"Too Less Matching Points. filename: {save_path}")
    else:
        src_pts = np.float32([kp1[m.queryIdx].pt
                              for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt
                              for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w = img1.shape
        patch = cv2.warpPerspective(bgr2,
                                    np.linalg.inv(M), (w, h),
                                    flags=cv2.INTER_NEAREST)

        if save_path is not None:
            pts = np.array([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]],
                           dtype=np.float).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3,
                                 cv2.LINE_AA)
            matchesMask = mask.ravel().tolist()
            draw_params = dict(
                matchColor=(0, 255, 0),  # draw matches in green color
                singlePointColor=None,
                matchesMask=matchesMask,  # draw only inliers
                flags=2)

            name = get_new_name(save_path, "succ")
            img_match = cv2.drawMatches(img1, kp1, img2, kp2, good, None,
                                        **draw_params)
            cv2.imwrite(name, img_match)

            name = get_new_name(save_path, "crop")
            name = get_new_extension(name, ".png")
            cv2.imwrite(name, patch)
    return patch


def ascii_color():
    mask = _ascii_mask()
    patch1 = np.zeros_like(mask)
    patch2 = np.ones_like(mask) * 255
    sep = np.ones((64, 8, 3), dtype=np.uint8) * 255
    mask = np.mean(mask, axis=2)
    white = []
    black = []
    for i in range(64):
        for j in range(64):
            if mask[i, j] == 0:
                black.append((i, j))
            else:
                white.append((i, j))
    n = len(white)
    colors = _test_colors()
    colors.sort(key=lambda x: sum(x), reverse=True)
    whites = colors[:n]
    blacks = colors[n:]
    random.seed(0)
    random.shuffle(whites)
    random.shuffle(blacks)
    for (i, j), c in zip(white, whites):
        patch1[i, j] = c
    for (i, j), c in zip(black, blacks):
        patch2[i, j] = c
    patch = np.concatenate([patch1, sep, patch2], axis=1)
    return patch


def upscale(img, x: int):
    h, w, c = img.shape
    img_u = np.zeros((h * x, w * x, c), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            img_u[i * x:(i + 1) * x, j * x:(j + 1) * x] = img[i:i + 1, j:j + 1]
    return img_u


def colormap2D(img, ax):
    values = img.flatten().astype(np.float32)
    df = pd.DataFrame({"values": values})
    sns.histplot(data=df, x="values", bins=50, ax=ax)


def colormap3D(img, ax):
    img = img.reshape(-1, 3).astype(np.float32)
    l = img.shape[0]
    values = np.concatenate([img[:, 0], img[:, 2], img[:, 1]])
    colors = ["Blue"] * l + ["Red"] * l + ["Green"] * l
    df = pd.DataFrame({"values": values, "colors": colors})
    sns.histplot(data=df, x="values", hue="colors", bins=50, ax=ax)


def compare_colors(img1, img2, save_path):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colormap3D(img1, axes[0])
    colormap3D(img2, axes[1])
    fig.savefig(save_path)
    plt.close(fig)


def show_diff(difimg, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(21, 5))
    titles = ["Blue", "Green", "Red"]
    for i in range(3):
        colormap2D(difimg[..., i], axes[i])
        axes[i].set_title(titles[i])
    fig.savefig(save_path)
    plt.close(fig)


def heatmap(img, ax):
    sns.heatmap(img,
                ax=ax,
                cmap="YlGnBu",
                center=0,
                xticklabels=8,
                yticklabels=8,
                square=True)


def show_diff_heatmap(difimg, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    titles = ["Blue", "Green", "Red"]
    for i in range(3):
        heatmap(difimg[..., i], axes[i])
        axes[i].set_title(titles[i])
    fig.savefig(save_path)
    plt.close(fig)


def cut_tail(x: np.ndarray, percentage: float) -> np.ndarray:
    x = x.reshape(-1, 3)
    n = x.shape[0]
    l = [(i, x[i]) for i in range(n)]
    remove_set = set()
    for i in range(3):
        l.sort(key=lambda x: x[1][i])
        for j in range(int(math.ceil(n * percentage))):
            remove_set.add(l[j][0])
        for j in range(int(math.floor(n * (1 - percentage))), n):
            remove_set.add(l[j][0])
    y = []
    for i in range(n):
        if i not in remove_set:
            y.append(x[i])
    y = np.array(y)
    return y


def show_all_channels(x: np.ndarray) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(21, 5))
    for i in range(3):
        axes[i].imshow(x[..., i])


class CornerFinder:
    def __init__(self, img) -> None:
        self.img = img.copy()
        self.cnt = 0
        self.ratio = self.adjust_image_ratio()
        self.points = []
        self.winname = "image"
        cv2.imshow(self.winname, self.img)
        cv2.setMouseCallback(self.winname, self.click_event)
        while self.cnt < 4:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyWindow(self.winname)
        self.sort()

    def adjust_image_ratio(self):
        h_lim, w_lim = 1080, 1920
        h, w = self.img.shape[:2]
        ratio = max(h / h_lim, w / w_lim)
        h, w = int(h / ratio), int(w / ratio)
        self.img = cv2.resize(self.img, (w, h), interpolation=cv2.INTER_AREA)
        return ratio

    def sort(self):
        pts = np.array(self.points)
        x_m = pts[:, 0].mean()
        y_m = pts[:, 1].mean()
        new_pts = [None] * 4
        for p in self.points:
            if p[0] - x_m < 0 and p[1] - y_m < 0:
                new_pts[0] = p
            elif p[0] - x_m > 0 and p[1] - y_m < 0:
                new_pts[1] = p
            elif p[0] - x_m > 0 and p[1] - y_m > 0:
                new_pts[2] = p
            elif p[0] - x_m < 0 and p[1] - y_m > 0:
                new_pts[3] = p
            else:
                raise NotImplementedError
        self.points = new_pts

    def click_event(self, event, x, y, flags, params):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 0.5
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)
            cv2.putText(self.img,
                        str(x) + ',' + str(y), (x, y), font, font_size,
                        (255, 0, 0), 2)
            cv2.imshow(self.winname, self.img)
            self.cnt += 1
            self.points.append((x * self.ratio, y * self.ratio))
        elif event == cv2.EVENT_RBUTTONDOWN:
            print(x, y)
            b = self.img[y, x, 0]
            g = self.img[y, x, 1]
            r = self.img[y, x, 2]
            cv2.putText(self.img,
                        str(b) + ',' + str(g) + ',' + str(r), (x, y), font,
                        font_size, (255, 255, 0), 2)
            cv2.imshow(self.winname, self.img)


class Pixel2Pixel(Dataset):
    def __init__(self, sim_img: Union[str, np.ndarray],
                 phy_img: Union[str, np.ndarray]) -> None:
        super().__init__()
        if isinstance(sim_img, str):
            sim_img = self.default_load(sim_img)
        if isinstance(phy_img, str):
            phy_img = self.default_load(phy_img)
        self.src = sim_img.reshape(-1, 3).astype(np.float32) / 255 - 0.5
        self.src = torch.from_numpy(self.src)
        self.dst = phy_img.reshape(-1, 3).astype(np.float32) / 255 - 0.5
        self.dst = torch.from_numpy(self.dst)
        self.length = self.src.shape[0]

    def default_load(self, path: str) -> np.ndarray:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def __getitem__(self, index):
        return self.src[index], self.dst[index]

    def __len__(self):
        return self.length


class ColorModel(nn.Module):
    def __init__(self, n_neuron: int) -> None:
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(3, n_neuron),
            nn.ReLU(),
            nn.Linear(n_neuron, n_neuron),
            nn.ReLU(),
            nn.Linear(n_neuron, 3),
        )

    def forward(self, x: Union[np.ndarray, torch.Tensor]):
        if self.training:
            x = self.model(x)
        elif isinstance(x, torch.Tensor):
            if x.ndim == 3:
                x = x.permute(1, 2, 0)
                x = self.model(x - 0.5) + 0.5
                x = x.permute(2, 0, 1)
            else:
                x = x.permute(0, 2, 3, 1)
                x = self.model(x - 0.5) + 0.5
                x = x.permute(0, 3, 1, 2)
            x = torch.clamp(x, 0, 1)
        elif isinstance(x, np.ndarray):
            h, w = x.shape[:2]
            x = x.reshape(-1, 3).astype(np.float32)
            x = x / 255 - 0.5
            x = torch.from_numpy(x)
            x = self.model(x)
            x = ((x + 0.5) * 255).cpu().detach().numpy()
            x = np.clip(x, 0, 255).astype(np.uint8)
            x = x.reshape(h, w, 3)
        else:
            raise NotImplementedError
        return x

    def pickle_dump(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self.model.state_dict(), f, protocol=2)

    def pickle_load(self, path: str):
        with open(path, "rb") as f:
            params = pickle.load(f)
        self.model.load_state_dict(params)


class AdaptiveCropper:
    def __init__(self, img, corner, save_path) -> None:
        self.img = img
        self.save_path = save_path
        self.winname = "adaptive crop"
        self.dsize = (512, 512)
        dst = [[0, 0], [511, 0], [511, 511], [0, 511]]
        self.dst = np.array(dst, dtype=np.float32)
        self.src = np.array(corner, dtype=np.float32)
        self.bias = np.zeros((1, 2), dtype=np.float32)
        self.crop()

    def crop(self):
        while True:
            self.mat = cv2.getPerspectiveTransform(self.src + self.bias,
                                                   self.dst)
            patch = cv2.warpPerspective(self.img, self.mat, self.dsize)
            cv2.imshow(self.winname, patch)
            key = cv2.waitKey(0) & 0xFF
            if key == ord("w"):
                self.bias[0, 1] -= 1
            elif key == ord("s"):
                self.bias[0, 1] += 1
            elif key == ord("a"):
                self.bias[0, 0] -= 1
            elif key == ord("d"):
                self.bias[0, 0] += 1
            elif key == ord("q"):
                cv2.imwrite(self.save_path, patch)
                cv2.destroyWindow(self.winname)
                break


def train_color_model(sim_img: Union[str, np.ndarray],
                      phy_img: Union[str, np.ndarray],
                      device: str = "cpu",
                      n_neuron: int = 16) -> ColorModel:
    model = ColorModel(n_neuron)
    model.to(device).train()
    loader = DataLoader(Pixel2Pixel(sim_img, phy_img),
                        batch_size=16,
                        shuffle=True)
    metric = nn.MSELoss()
    opt = optim.SGD(model.parameters(), 1, 0.9)
    sch = optim.lr_scheduler.StepLR(opt, 30, 0.1)
    epoch = 100
    _train(model, metric, opt, sch, loader, epoch, device)
    model.eval()
    return model
