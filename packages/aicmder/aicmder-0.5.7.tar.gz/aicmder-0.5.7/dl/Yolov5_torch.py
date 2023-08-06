import torch
import os
from models.common import DetectMultiBackend
from models.general import check_img_size, non_max_suppression, scale_coords
import cv2
import time
import numpy as np
from datasets import letterbox
import base64
from yolo_util import numpy_nms, bbox_iou

def plot_one_box(x, im, color=(128, 128, 128), label=None, line_thickness=1):
    # Plots one bounding box on image 'im' using OpenCV
    assert im.data.contiguous, 'Image not contiguous. Apply np.ascontiguousarray(im) to plot_on_box() input image.'
    tl = line_thickness or round(0.002 * (im.shape[0] + im.shape[1]) / 2) + 1  # line/font thickness
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(im, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(im, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(im, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

        # cv2.rectangle(im, (550, 265), (555, 270), color, -1, cv2.LINE_AA)  # filled

def cv2_to_base64(image):
    return base64.b64encode(image).decode('utf8')



class Yolov5:

    def __init__(self, weights, imgsz, device, classes=None, conf_thres=0.55, iou_thres=0.45) -> None:
        self.imgsz = imgsz
        self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, self.max_det = conf_thres, iou_thres, classes, False, 1000
        self.device = device
        self.weights = weights
        self.model = DetectMultiBackend(
            self.weights, device=self.device, dnn=False)
        self.stride, self.names, pt, jit, onnx, engine = self.model.stride, self.model.names, self.model.pt, self.model.jit, self.model.onnx, self.model.engine
        # print(self.stride, self.names, pt, jit, onnx, engine)
        self.hide_labels, self.hide_conf = False, False
        self.imgsz = check_img_size(
            self.imgsz, s=self.stride)  # check image size
        print(self.imgsz, np.array(self.names)[self.classes], self.names, self.classes, self.stride)
        # not using half precision
        self.half = False
        self.model.model.float()

        self.model.warmup(imgsz=(1, 3, *self.imgsz), half=self.half)  # warmup



        
    def non_max_suppression(self, prediction, input_h, input_w, origin_h, origin_w, conf_thres, nms_thres, classes=None):
        """
        description: Removes detections with lower object confidence score than 'conf_thres' and performs
        Non-Maximum Suppression to further filter detections.
        param:
            prediction: detections, (x1, y1, x2, y2, conf, cls_id)
            origin_h: original image height
            origin_w: original image width
            conf_thres: a confidence threshold to filter detections
            nms_thres: a iou threshold to filter detections
        return:
            boxes: output after nms with the shape (x1, y1, x2, y2, conf, cls_id)
        """
        nc = prediction.shape[2] - 5 
        multi_label = False
        multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)

        mask = prediction[..., 4] >= conf_thres
        mask = mask.cuda()
        
        start = time.time()
        # Get the boxes that score > CONF_THRESH
        print(prediction.shape)
        boxes = prediction[mask]
        
        # boxes = boxes_cuda.cpu().numpy()

        print(time.time() - start, "-----")

        # Trandform bbox from [center_x, center_y, w, h] to [x1, y1, x2, y2]
        boxes[:, :4] = self.xywh2xyxy(input_h, input_w, origin_h, origin_w, boxes[:, :4])
        # clip the coordinates
        boxes[:, 0] = np.clip(boxes[:, 0], 0, origin_w - 1)
        boxes[:, 2] = np.clip(boxes[:, 2], 0, origin_w - 1)
        boxes[:, 1] = np.clip(boxes[:, 1], 0, origin_h - 1)
        boxes[:, 3] = np.clip(boxes[:, 3], 0, origin_h - 1)
        # Object confidence
        confs = boxes[:, 4]

        boxes[:, 5:] *= boxes[:, 4:5]  # conf = obj_conf * cls_conf
        if multi_label:
            assert "not implemented"
        else:
            # output_shape = boxes[:, 5:].shape
            j = np.argmax(boxes[:, 5:], axis=1).reshape(-1, 1)
            conf = np.max(boxes[:, 5:], axis=1).reshape(-1, 1)
            boxes = np.concatenate((boxes[:, :4], conf, j), 1)
            # conf, j = boxes[:, 5:].max(1, keepdim=True)

        # Filter by class
        if classes is not None:
            class_selection = (boxes[:, 5:6] == classes).any(1)
            boxes = boxes[class_selection]
            confs = confs[class_selection]

        ################################################
        # Sort by the confs
        boxes = boxes[np.argsort(-confs)]
        # Perform non-maximum suppression
        keep_boxes = []
        while boxes.shape[0]:
            large_overlap = bbox_iou(np.expand_dims(boxes[0, :4], 0), boxes[:, :4]) > nms_thres
            label_match = boxes[0, -1] == boxes[:, -1]
            # Indices of boxes with lower confidence scores, large IOUs and matching labels
            invalid = large_overlap & label_match
            keep_boxes += [boxes[0]]
            boxes = boxes[~invalid]
        boxes = np.stack(keep_boxes, 0) if len(keep_boxes) else np.array([])
        ################################################

        scores = boxes[:, 4]
        # ii = torch.ops.torchvision.nms(torch.from_numpy(boxes[:, :4]), torch.from_numpy(scores), nms_thres)
        i = numpy_nms(boxes[:, :4], scores, nms_thres)
        boxes = boxes[i]


        
        return boxes

    def xywh2xyxy(self, input_h, input_w, origin_h, origin_w, x):
        """
        description:    Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
        param:
            origin_h:   height of original image
            origin_w:   width of original image
            x:          A boxes numpy, each row is a box [center_x, center_y, w, h]
        return:
            y:          A boxes numpy, each row is a box [x1, y1, x2, y2]
        """
        y = np.zeros_like(x)
        r_w = input_w / origin_w
        r_h = input_h / origin_h
        if r_h > r_w:
            y[:, 0] = x[:, 0] - x[:, 2] / 2
            y[:, 2] = x[:, 0] + x[:, 2] / 2
            y[:, 1] = x[:, 1] - x[:, 3] / 2 - (input_h - r_w * origin_h) / 2
            y[:, 3] = x[:, 1] + x[:, 3] / 2 - (input_h - r_w * origin_h) / 2
            y /= r_w
        else:
            y[:, 0] = x[:, 0] - x[:, 2] / 2 - (input_w - r_h * origin_w) / 2
            y[:, 2] = x[:, 0] + x[:, 2] / 2 - (input_w - r_h * origin_w) / 2
            y[:, 1] = x[:, 1] - x[:, 3] / 2
            y[:, 3] = x[:, 1] + x[:, 3] / 2
            y /= r_h

        return y


    def predict_image(self, img_bgr, debug=0):
        img = letterbox(img_bgr, self.imgsz, stride=self.stride)[0]
        # print(img.shape, img_bgr.shape)
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img).astype(np.float32)

        im = torch.from_numpy(img).to(self.device)
        im = im.half() if self.half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        pred = self.model(im, augment=False, visualize=False)
        h, w, _ = img_bgr.shape
        

#################################################### yolov5 origin#####################################################################################
        # start = time.time()
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres,
                                   self.classes, self.agnostic_nms, max_det=self.max_det)
        # end = time.time()
        # print("time-------", end - start, img.shape, self.device, self.stride, self.imgsz, pred[0].device)
        # print("pred", pred)
#################################################### yolov5 origin#####################################################################################


        # start = time.time()
        # # pred_ori_cpu = pred_ori.cpu().numpy()
        # origin_h, origin_w, _ = img_bgr.shape
        # input_h, input_w = im.shape[2:]
        # # print(origin_h, origin_w, input_h, input_w)
        # boxes = self.non_max_suppression(pred_ori, input_h, input_w, origin_h, origin_w, conf_thres=self.conf_thres, nms_thres=self.iou_thres, classes=self.classes)
        # end = time.time()
        # print("new time---", boxes.shape, end - start, self.conf_thres, self.iou_thres)
        # # print(boxes)



        # resp_list = []
        # for i, det in enumerate(boxes):
        #     if len(det) == 6:
        #         # print(det)
        #         start_x, start_y, end_x, end_y, conf, cls = det
                    
        #         c = int(cls)  # integer class
        #         label = None if self.hide_labels else (self.names[c] if self.hide_conf else f'{self.names[c]} {conf:.2f}')
        #         # start_x, start_y, end_x, end_y = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
        #         resp_list.append({
        #             "start_x": int(start_x),
        #             "start_y": int(start_y),
        #             "end_x": int(end_x),
        #             "end_y": int(end_y),
        #             "x0": start_x / w,
        #             "x1": end_x / w,
        #             "y0": start_y / h,
        #             "y1": end_y / h,
        #             "c" : c,
        #             "label": label,
        #             "conf": float(conf)
        #         })
        #         if debug > 0:
        #             plot_one_box((start_x, start_y, end_x, end_y), img_bgr, label=label)

#################################################### yolov5 origin#####################################################################################
        resp_list = []
        # print("shape", w, h, img_bgr.shape)
        for i, det in enumerate(pred):  # per image
            if len(det) > 0:
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], img_bgr.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    if len(xyxy) >= 4:
                        c = int(cls)  # integer class
                        label = None if self.hide_labels else (self.names[c] if self.hide_conf else f'{self.names[c]} {conf:.2f}')
                        # print(xyxy, conf, c, label)
                        start_x, start_y, end_x, end_y = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                        resp_list.append({
                            "start_x": start_x,
                            "start_y": start_y,
                            "end_x": end_x,
                            "end_y": end_y,
                            "x0": float(start_x) / w,
                            "x1": float(end_x) / w,
                            "y0": float(start_y) / h,
                            "y1": float(end_y) / h,
                            "c" : c,
                            "label": label,
                            "conf": float(conf)
                        })

                        if debug > 0:
                            plot_one_box(xyxy, img_bgr, label=label)
#################################################### yolov5 origin#####################################################################################

            
        if len(resp_list) > 0:
            resp_list = sorted(resp_list, key=lambda x: x["conf"], reverse=True)
            # print(resp_list)
        
        resp_d = {}
        resp_d["data"] = resp_list
        if debug > 0:
            cv2.imwrite('detect_torch.png', img_bgr)
            if debug > 1:
                with open('detect_torch.png',  'rb') as img_f:
                    img = img_f.read()
                    resp_d["img"] = cv2_to_base64(img)
        return resp_d


def coin():
    imgsz = [1280, 1280]
    weights = '/home/faith/android_viewer/thirdparty/yolov5/runs/train/exp26/weights/best.pt'
    weights = "/home/faith/dl_project/coin/42.pt"
    yolo = Yolov5(weights=weights, imgsz=imgsz, conf_thres=0.82)
    image_file = "/home/faith/750.png"
    img = cv2.imread(image_file, cv2.COLOR_RGB2BGR)
    for i in range(4):
        start = time.time()
        resp_d = yolo.predict_image(img, debug=0)
        end = time.time()
        print("Total time", end - start)
    print(resp_d)

def people():
    from torch_utils import select_device
    imgsz = [1280, 1280]
    # weights = '/home/faith/yolov5m6.pt'
    # yolo = Yolov5(weights=weights, imgsz=imgsz)

    imgsz = [640, 640]
    # weights = '/home/faith/yolov5m.pt'
    weights = '/home/faith/yolov5m6.pt'
    # weights = '/home/faith/yolov5l.pt'
    device = select_device("1")
    yolo = Yolov5(weights=weights, imgsz=imgsz, classes=[0], conf_thres=0.25, device=device)
    image_file = "/home/faith/aicmder/dl/detect_torch.png"
    image_file = "/home/faith/aicmder/tests_model/222.jpg"

    img = cv2.imread(image_file, cv2.COLOR_RGB2BGR)

    for i in range(5):
        start = time.time()
        resp_d = yolo.predict_image(img, debug=0)
        # if len(resp_d["data"]) > 0:
        # print(resp_d)
        end = time.time()
        print(end - start)

if __name__ == "__main__":
    people()
    # coin()