from .lib import *
from .adv import *
from .models import *
from .utils import *
from .third_party.yolov5.utils.downloads import safe_download

def hiding_attack_on_yolov5():
    h, w = 80, 80
    device = 'cuda:0'
    patch = AdvPatch((h, w), device, OptCfg(), EoTCfg())

    tf = tv.transforms.Resize((640, 640))
    url = 'https://raw.githubusercontent.com/forget2save/yolov5/master/data/images/bus.jpg'
    path = 'bus.jpg'
    safe_download(path, url)
    img = read_img(path).to(device)
    img = tf(img)

    target_class = 5
    bbox = [7.76074e+00, 1.34380e+02, 6.10551e+02, 4.49180e+02]
    topleft_center = [
        int((bbox[1] + bbox[3]) * 0.5 - h // 2),
        int((bbox[0] + bbox[2]) * 0.5 - w // 2),
    ]

    model = YOLOv5(device)
    print(model(img))

    print('=' * 30)
    print("Start Attacking...")

    for e in range(200):
        adv_img = patch.apply(img, topleft_center)
        pred = model(adv_img, eval=False)[0]
        loss = (pred[:, 4] * pred[:, 5 + target_class]).max()
        patch.update(loss)
        print(e, loss)

    print(model(adv_img))
    return adv_img, patch
