
import cv2
from matplotlib import collections
import numpy as np
import shapely.geometry
import shapely.affinity
from collections import defaultdict
import base64

from fence_detect import RotatedRect, Fence


class Wearing(RotatedRect):

    def set_label(self, label):
        self.label = label

def check_person_wear_helmet(resp_d_person, resp_d, h, w):
    
    obj_rect_set = set()
    for i, obj in enumerate(resp_d["data"]):
        start_x, end_x, end_y, start_y = obj["start_x"], obj["end_x"], obj["end_y"], obj["start_y"]
        width = end_x - start_x
        height = end_y - start_y
        center_x = start_x + width / 2
        center_y = start_y + height / 2
        obj_rect = Wearing()
        obj_rect.set_param(center_x, center_y, width, height, 0)
        obj_rect.set_label(obj["label"])
        obj_rect_set.add(obj_rect)

    resp_d["person"] = []
    for i, obj in enumerate(resp_d_person["data"]):
        start_x, end_x, end_y, start_y = obj["start_x"], obj["end_x"], obj["end_y"], obj["start_y"]
        width = end_x - start_x
        height = end_y - start_y
        center_x = start_x + width / 2
        center_y = start_y + height / 2
        x0, x1, y0, y1 = obj["x0"], obj["x1"], obj["y0"], obj["y1"]
        person_rect = Fence([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], w=w, h=h)
        # person_rect = RotatedRect()
        # person_rect.set_param(center_x, center_y, width, height, 0)
        
        # for debug
        # if obj["label"] == "person 0.69":
        #     print("debug")

        selected_objects = set()
        for obj_rect in obj_rect_set:
            if  "detection" in obj and (("reflective_clothes" in obj["detection"] and "reflective_clothes" in obj_rect.label) or 
                                            ("helmet" in obj["detection"] and "helmet" in obj_rect.label)):
                continue
            if  "detection" in obj and "reflective_clothes" in obj["detection"] and "helmet" in obj["detection"]:
                break
            if person_rect.pointPolygonTest((obj_rect.cx, obj_rect.cy)) == 1:
                if "detection" in obj:
                    obj["detection"] += obj_rect.label + " "
                else:
                    obj["detection"] = obj_rect.label + " "
                selected_objects.add(obj_rect)
        
        obj_rect_set = obj_rect_set.difference(selected_objects)
        resp_d["person"].append(obj)
    
    # print(obj_rect_set)
 



def filter_with_fence(resp_d, fence_list, iouThreshold=0.8):
    new_person = []
    for j, obj in enumerate(resp_d["person"]):
        start_x, end_x, end_y, start_y = obj["start_x"], obj["end_x"], obj["end_y"], obj["start_y"]
        width = end_x - start_x
        height = end_y - start_y
        center_x = start_x + width / 2
        center_y = start_y + height / 2

        obj_rect = RotatedRect()
        obj_rect.set_param(center_x, center_y, width, height, 0)

        for i, fence in enumerate(fence_list):
            if obj_rect.occlusion_rate(fence.fence_rect) >= iouThreshold:
                new_person.append(obj)
                break
    resp_d["person"] = new_person



def draw_restrict_fence(fence_list, img_bgr, resp_d, debug=None):
    if debug is not None and debug > 0:
        try:
            line_thickness = 3
            tl = line_thickness or round(
                0.002 * (img_bgr.shape[0] + img_bgr.shape[1]) / 2) + 1  # line/font thickness
            tf = max(tl - 1, 1)  # font thickness

            for i, fence in enumerate(fence_list):
                # label = str(i)
                cv2.drawContours(img_bgr, fence.contours, 0, (255, 0, 0), 2)
                # print(c1)
            cv2.imwrite('detect_torch_restrict_fence.png', img_bgr)

            # return fence
            if debug > 1:
                with open('detect_torch_restrict_fence.png',  'rb') as img_f:
                    img = img_f.read()
                    resp_d["img"] = base64.b64encode(img).decode('utf8')
        except Exception as e:
            pass