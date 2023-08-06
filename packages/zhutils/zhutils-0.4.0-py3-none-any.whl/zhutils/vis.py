from .lib import *


def log_init(filename="example.log", show=True, file=True, level=logging.INFO):
    assert show or file, "must choose at least one"
    handlers = []
    if show:
        handlers.append(logging.StreamHandler())
    if file:
        handlers.append(logging.FileHandler(filename))
    logging.basicConfig(format='[%(asctime)s] (%(levelname)s) %(message)s',
                        level=level,
                        handlers=handlers)


def get_new_name(x, y="crop"):
    _, ext = os.path.splitext(x)
    return x.replace(ext, "_" + y + ext)


def get_new_extension(x, y=".png"):
    x, _ = os.path.splitext(x)
    return x + y


def recursive_print(model_output, level=None, max_depth=3):
    ms = model_output
    if level is None:
        level = []
    elif len(level) > max_depth:
        return
    else:
        print("-".join(str(k) for k in level), type(ms), end=" ")

    if isinstance(ms, torch.Tensor) or isinstance(ms, np.ndarray):
        print("shape:", tuple(ms.shape), "range:", (ms.min(), ms.max()))
    elif isinstance(ms, list) or isinstance(ms, tuple):
        print("length:", len(ms))
        for i, m in enumerate(ms):
            level.append(i)
            recursive_print(m, level)
            level.pop()
    elif isinstance(ms, dict):
        print("length:", len(ms.keys()))
        for i, (k, m) in enumerate(ms.items()):
            print(k + ":")
            level.append(i)
            recursive_print(m, level)
            level.pop()
    else:
        print("value:", ms)


class AdaptiveAxes:
    def __init__(self,
                 n_figure: int,
                 n_col: int = 4,
                 fig_size: tuple = (7, 5)) -> None:
        self.n = n_figure
        self.n_col = min(n_figure, n_col)
        self.n_row = (n_figure + n_col - 1) // n_col
        self.fig_size = (fig_size[0] * self.n_col, fig_size[1] * self.n_row)
        self.fig, self.axes = plt.subplots(self.n_row,
                                           self.n_col,
                                           squeeze=False,
                                           figsize=self.fig_size)

    def __iter__(self):
        for i in range(self.n):
            j = i // self.n_col
            k = i % self.n_col
            yield self.axes[j][k]
