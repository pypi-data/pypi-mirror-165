from .lib import *
from .third_party.yolov5.models.yolo import attempt_load, non_max_suppression
from .third_party.yolov5.utils.loss import ComputeLoss

__all__ = ['YOLOv5']


class YOLOv5:
    def __init__(self, device, conf_thres: float = 0.25):
        if not os.path.exists("weights"):
            os.makedirs("weights")
        self.model = attempt_load("weights/yolov5m.pt",
                                  map_location=device,
                                  fuse=True).eval()
        for k in self.model.model.children():
            if "Detect" in str(type(k)):
                k.inplace = False
        self.conf_thres = conf_thres
        self.nms = lambda x: non_max_suppression(x, conf_thres=self.conf_thres)
        self.compute_loss = ComputeLoss(self.model)

    def __call__(self, x, eval=True):
        if eval:
            with torch.no_grad():
                pred = self.model(x)[0]
                ret = self.nms(pred)
        else:
            ret = self.model(x)[0]
        return ret

