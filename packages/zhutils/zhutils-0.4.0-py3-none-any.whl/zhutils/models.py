from .lib import *
from .third_party.yolov5.models.yolo import attempt_load, non_max_suppression
from .third_party.yolov5.utils.loss import ComputeLoss
from .third_party.facenet import MTCNN
from .third_party.facenet import InceptionResnetV1 as IResnet
from .utils import ValidPad

__all__ = ['YOLOv5', 'MTCNN', 'IResnet']


class YOLOv5:
    def __init__(self, device, conf_thres: float = 0.25, varient: str = "m"):
        if not os.path.exists("weights"):
            os.makedirs("weights")
        assert varient in ["n", "s", "m", "l", "x"]
        self.model = attempt_load(f"weights/yolov5{varient}.pt",
                                  map_location=device,
                                  fuse=True).eval()
        for k in self.model.model.children():
            if "Detect" in str(type(k)):
                k.inplace = False
        self.conf_thres = conf_thres
        self.pad = ValidPad(32)
        self.nms = lambda x: non_max_suppression(x, conf_thres=self.conf_thres)
        self.compute_loss = ComputeLoss(self.model)

    def __call__(self, x:torch.Tensor, eval=True, roi=None):
        x = self.pad(x)
        if eval:
            with torch.no_grad():
                pred = self.model(x)[0]
                ret = self.nms(pred)
            if roi is not None:
                roi = set([roi] if isinstance(roi, int) else roi)
                tmp = []
                for ret_i in ret:
                    tmp_i = []
                    for y in ret_i:
                        if int(y[-1]) in roi:
                            tmp_i.append(y)
                    if len(tmp_i):
                        tmp.append(torch.stack(tmp_i))
                    else:
                        tmp.append(torch.empty((0, 6), device=x.device))
                ret = tmp
        else:
            ret = self.model(x)[0]
        return ret

