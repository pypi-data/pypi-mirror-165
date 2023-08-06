import os, json
os.environ["CMD_CLIENT_PORT"] = "6655"
os.environ["CMD_WORKER_PORT"] = "6656"
import aicmder as cmder
from aicmder.module.module import serving, moduleinfo
from image_utils import readb64
from face_detection import ImageEmbeddings, SFaceModel, load_embeds
import threading
import time

@moduleinfo(name='face')
class FaceModule(cmder.Module):

    def __init__(self, **kwargs) -> None:
        print("init FaceModule", kwargs)
        self.model = SFaceModel("/home/faith/.deepface/weights/face_recognition_sface_2021dec.onnx")
        e = load_embeds()
        self.embed = ImageEmbeddings() if e is None else e
        self.face_dir = os.path.abspath(os.path.dirname(__file__))
        if not os.path.exists( self.face_dir):
            os.makedirs(self.face_dir)
        print("current face dir", self.face_dir)
        self.save_thread = threading.Thread(target=self.save_face)
        self.save_thread.start()

    def save_face(self):
        while True:
            self.embed.save()
            # print("saving")
            time.sleep(8)

    @serving
    def predict(self, **kwargs):
        if "method" in kwargs:     
            resp_d = {}
            # print(kwargs["method"], kwargs["method"] == "VerifyFace")
            if "AddFace" == kwargs["method"]:
                img_base64 = kwargs["img"]
                id = kwargs["id"]
                file_path = "{}/face/{}.png".format(self.face_dir , id)
  
                img_bgr = readb64(img_base64, filename=file_path, save=True)
                ret = self.embed.add_file(file_path, self.model)
                resp_d["code"] = 1 if ret else -1
                json_ret = json.dumps(resp_d)
                return json_ret
            if "DelFace" == kwargs["method"]:
                id = kwargs["id"]
                ret = self.embed.remove(id)
                resp_d["code"] = 1 if ret else -1
                json_ret = json.dumps(resp_d)
                return json_ret
            if "VerifyFace" == kwargs["method"]:
                img_base64 = kwargs["img"]
                ret = self.embed.verify_face(img_base64, self.model, base64_img=True)
                if ret is None:
                    ret = resp_d
                json_ret = json.dumps(ret)
                return json_ret
        return '{"data": "-1"}'


# https://github.com/serengil/deepface/issues/351
# from deepface.detectors import FaceDetector
# import cv2

# img_path = "couple.jpg"
# detector_name = "opencv"

# img = cv2.imread(img_path)

# detector = FaceDetector.build_model(detector_name) #set opencv, ssd, dlib, mtcnn or retinaface

# obj = FaceDetector.detect_faces(detector, detector_name, img)

# print("there are ",len(obj)," faces")


# https://github.com/serengil/deepface/issues/419
# from retinaface import RetinaFace
# from deepface import DeepFace

# faces = RetinaFace.extract_faces("img.jpg")
# for face in faces:
#     obj = DeepFace.analyze(img)
#     print(obj["age"])


if __name__ == "__main__":
    with open("face.json") as json_f:
        config = json.load(json_f)
        # print(config)
        exec_cmd = ['-w', config["w"], '-c', json.dumps(config["config"]),
                   '-p', config["port"], '--max_connect', config["max_conn"], '--device_map']
        exec_cmd.extend(config["device"])
        print(exec_cmd)
        serve = cmder.serve.ServeCommand()
        serve.execute(exec_cmd)