import onnxruntime as ort
import numpy as np
from yolo_util import *
import cv2
import time

# options = self.sess.get_provider_options()
# print(options)
# cuda_options = options['CUDAExecutionProvider']
# cuda_options['cudnn_conv_use_max_workspace'] = '1'
# self.sess.set_providers(['CUDAExecutionProvider'], [cuda_options])

# so = ort.SessionOptions()
# so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
# so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

# exproviders = ['CUDAExecutionProvider', 'CPUExecutionProvider']
# self.sess = ort.InferenceSession('/home/faith/aicmder/tests_model/best.onnx', so, providers=exproviders)

# if "cuda" in device:
#     providers = ["CUDAExecutionProvider"]
# else:
#     providers = ["CPUExecutionProvider"]


class Yolov5:

    def __init__(self, imgsz, model='/home/faith/yolov5m6.onnx', names=[''], classes=None, conf_thres=0.55, iou_thres=0.45, fp16=False) -> None:
        # python export.py --weights runs/train/exp26/weights/best.pt --img 736 1280
        print(ort.get_available_providers())

        cuda = False
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else [
            'CPUExecutionProvider']

        # https://stackoverflow.com/questions/70844974/onnxruntime-vs-onnxruntimeopenvinoep-inference-time-difference
        # pip install onnxruntime-openvino
        device = 'CPU_FP32'
        self.sess = ort.InferenceSession(model, providers=['OpenVINOExecutionProvider'], provider_options=[{'device_type' : device}])

        # self.sess = ort.InferenceSession(model, providers=providers)
        # self.sess.set_providers(['CUDAExecutionProvider'], [ {'device_id': 1}])

        print(ort.get_device(), providers, "----")
        self.stride = 64
        self.hide_labels, self.hide_conf = False, False
        # self.names = ['enermy']
        self.names = names
        self.fp16 = fp16
        self.imgsz = imgsz  # (768, 1280)
        self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, self.max_det = conf_thres, iou_thres, classes, False, 1000

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

        # Get the boxes that score > CONF_THRESH
        print(prediction.shape)
        boxes = prediction[mask]

        # Trandform bbox from [center_x, center_y, w, h] to [x1, y1, x2, y2]
        boxes[:, :4] = self.xywh2xyxy(
            input_h, input_w, origin_h, origin_w, boxes[:, :4])
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
            large_overlap = bbox_iou(np.expand_dims(
                boxes[0, :4], 0), boxes[:, :4]) > nms_thres
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
        # img_bgr = cv2.resize(img_bgr, self.imgsz)
        img = letterbox(img_bgr, self.imgsz, stride=self.stride)[0]
        print(img.shape, img_bgr.shape)
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img).astype(np.float32)
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        start = time.time()
        pred = self.sess.run([self.sess.get_outputs()[0].name], {
                             self.sess.get_inputs()[0].name: img.astype(np.float16) if self.fp16 else img})[0]
        end = time.time()
        print("time--", end - start)

        h, w, _ = img_bgr.shape
        # start = time.time()
        origin_h, origin_w, _ = img_bgr.shape
        input_h, input_w = img.shape[2:]
        # # print(origin_h, origin_w, input_h, input_w)
        boxes = self.non_max_suppression(pred, input_h, input_w, origin_h, origin_w,
                                         conf_thres=self.conf_thres, nms_thres=self.iou_thres, classes=self.classes)
        # end = time.time()
        # print("new time---", boxes.shape, end - start, self.conf_thres, self.iou_thres)
        # # print(boxes)

        resp_list = []
        for i, det in enumerate(boxes):
            if len(det) == 6:
                # print(det)
                start_x, start_y, end_x, end_y, conf, cls = det

                c = int(cls)  # integer class
                label = None if self.hide_labels else (
                    self.names[c] if self.hide_conf else f'{self.names[c]} {conf:.2f}')
                # start_x, start_y, end_x, end_y = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                resp_list.append({
                    "start_x": int(start_x),
                    "start_y": int(start_y),
                    "end_x": int(end_x),
                    "end_y": int(end_y),
                    "x0": start_x / w,
                    "x1": end_x / w,
                    "y0": start_y / h,
                    "y1": end_y / h,
                    "c": c,
                    "label": label,
                    "conf": float(conf)
                })
                if debug > 0:
                    plot_one_box((start_x, start_y, end_x, end_y),
                                 img_bgr, label=label)

        # pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)
        # for i, det in enumerate(pred):  # detections per image
        #     if len(det) > 0:
        #         det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img_bgr.shape).round()
        #         # print("--", det)
        #         for *xyxy, conf in reversed(det):
        #             if len(xyxy) >= 4:
        #                 # print(xyxy, conf)
        #                 plot_one_box(xyxy, img_bgr, label=self.names)
        if debug > 1:
            cv2.imwrite('detect.png', img_bgr)


def onnx_convert():
    from onnxconverter_common.float16 import convert_float_to_float16
    import onnx
    model = onnx.load_model('/home/faith/yolov5m6.onnx')
    fp16_model = convert_float_to_float16(model)
    onnx.save_model(fp16_model, '/home/faith/yolov5m6_fp16.onnx')


def inference():
    model_name = '/home/faith/yolov5m6.onnx'
    # model_name = '/home/faith/yolov5m6_fp16.onnx'

    yolo = Yolov5(model=model_name, names=['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                                                            'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'], classes=[0], imgsz=(640, 640), fp16=False)
    image_file = "/home/faith/aicmder/tests_model/222.jpg"
    image_file = "/home/faith/aicmder/dl/IMG_5980.jpg"
    for i in range(5):
        img = cv2.imread(image_file, cv2.COLOR_RGB2BGR)
        # time.sleep(2)
        start = time.time()
        yolo.predict_image(img, debug=0)
        end = time.time()
        print(end - start)


if __name__ == "__main__":
    # onnx_convert()
    inference()
