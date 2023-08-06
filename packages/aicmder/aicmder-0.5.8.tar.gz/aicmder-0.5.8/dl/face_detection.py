from collections import OrderedDict
from turtle import distance
import numpy as np
import cv2
from image_utils import *
import json
import zlib
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


def _detect_face(detector, img, align=True):
    resp = []

    detected_face = None
    img_region = [0, 0, img.shape[0], img.shape[1]]

    faces = []
    try:
        #faces = detector["face_detector"].detectMultiScale(img, 1.3, 5)
        faces = detector["face_detector"].detectMultiScale(img, 1.1, 10)
    except:
        pass

    if len(faces) > 0:

        for x, y, w, h in faces:
            detected_face = img[int(y):int(y+h), int(x):int(x+w)]

            if align:
                detected_face = align_face(
                    detector["eye_detector"], detected_face)

            img_region = [x, y, w, h]

            resp.append((detected_face, img_region))

    return resp


def align_face(eye_detector, img):

    # eye detector expects gray scale image
    detected_face_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #eyes = eye_detector.detectMultiScale(detected_face_gray, 1.3, 5)
    eyes = eye_detector.detectMultiScale(detected_face_gray, 1.1, 10)

    # ----------------------------------------------------------------

    # opencv eye detectin module is not strong. it might find more than 2 eyes!
    # besides, it returns eyes with different order in each call (issue 435)
    # this is an important issue because opencv is the default detector and ssd also uses this
    # find the largest 2 eye. Thanks to @thelostpeace

    eyes = sorted(eyes, key=lambda v: abs(
        (v[0] - v[2]) * (v[1] - v[3])), reverse=True)

    # ----------------------------------------------------------------

    if len(eyes) >= 2:

        # decide left and right eye

        eye_1 = eyes[0]
        eye_2 = eyes[1]

        if eye_1[0] < eye_2[0]:
            left_eye = eye_1
            right_eye = eye_2
        else:
            left_eye = eye_2
            right_eye = eye_1

        # -----------------------
        # find center of eyes
        left_eye = (int(left_eye[0] + (left_eye[2] / 2)),
                    int(left_eye[1] + (left_eye[3] / 2)))
        right_eye = (int(right_eye[0] + (right_eye[2]/2)),
                     int(right_eye[1] + (right_eye[3]/2)))
        img = alignment_procedure(img, left_eye, right_eye)
    return img  # return img anyway


class FaceDetector:

    face_detector = build_model()

    # def build_model(self, detector_backend):
    #     if 'opencv' == detector_backend:
    #         self.face_detector

    @staticmethod
    def detect_face(detector_backend, img, align=True):
        # detector_backend
        obj = _detect_face(FaceDetector.face_detector, img, align)
        print("---detect faces", len(obj))
        if len(obj) > 0:
            if len(obj) == 1:
                face, region = obj[0]  # discard multiple faces
            else:
                face, region = obj[0]
                # face = None
                # region = [0, 0, img.shape[0], img.shape[1]]
        else:  # len(obj) == 0
            face = None
            region = [0, 0, img.shape[0], img.shape[1]]

        return face, region


def detect_face(img, detector_backend='opencv', grayscale=False, enforce_detection=True, align=True):

    img_region = [0, 0, img.shape[0], img.shape[1]]

    # ----------------------------------------------
    # people would like to skip detection and alignment if they already have pre-processed images
    if detector_backend == 'skip':
        return img, img_region

    # ----------------------------------------------

    # detector stored in a global variable in FaceDetector object.
    # this call should be completed very fast because it will return found in memory
    # it will not build face detector model in each call (consider for loops)
    # face_detector = FaceDetector.build_model(detector_backend)

    try:
        # detected_face, img_region = FaceDetector.detect_face(face_detector, detector_backend, img, align)
        detected_face, img_region = FaceDetector.detect_face(
            detector_backend, img, align)
    # if detected face shape is (0, 0) and alignment cannot be performed, this block will be run
    except Exception as e:
        print(e)
        detected_face = None

    if (isinstance(detected_face, np.ndarray)):
        return detected_face, img_region
    else:
        if detected_face == None:
            if enforce_detection != True:
                return img, img_region
            else:
                raise ValueError(
                    "Face could not be detected. Please confirm that the picture is a face photo or consider to set enforce_detection param to False.")


def preprocess_face(
        img, target_size=(224, 224),
        grayscale=False, enforce_detection=True, detector_backend='opencv', return_region=False, align=True, base64_img=False):

    # img might be path, base64 or numpy array. Convert it to numpy whatever it is.
    img = load_image(img, base64_img=base64_img)
    base_img = img.copy()

    img, region = detect_face(img=img, detector_backend=detector_backend,
                              grayscale=grayscale, enforce_detection=enforce_detection, align=align)

    # --------------------------

    if img.shape[0] == 0 or img.shape[1] == 0:
        if enforce_detection == True:
            raise ValueError("Detected face shape is ", img.shape,
                             ". Consider to set enforce_detection argument to False.")
        else:  # restore base image
            img = base_img.copy()

    # --------------------------

    # post-processing
    if grayscale == True:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ---------------------------------------------------
    # resize image to expected shape

    # img = cv2.resize(img, target_size) #resize causes transformation on base image, adding black pixels to resize will not deform the base image

    if img.shape[0] > 0 and img.shape[1] > 0:
        factor_0 = target_size[0] / img.shape[0]
        factor_1 = target_size[1] / img.shape[1]
        factor = min(factor_0, factor_1)

        dsize = (int(img.shape[1] * factor), int(img.shape[0] * factor))
        img = cv2.resize(img, dsize)

        # Then pad the other side to the target size by adding black pixels
        diff_0 = target_size[0] - img.shape[0]
        diff_1 = target_size[1] - img.shape[1]
        if grayscale == False:
            # Put the base image in the middle of the padded image
            img = np.pad(img, ((diff_0 // 2, diff_0 - diff_0 // 2),
                               (diff_1 // 2, diff_1 - diff_1 // 2), (0, 0)), 'constant')
        else:
            img = np.pad(img, ((diff_0 // 2, diff_0 - diff_0 // 2),
                               (diff_1 // 2, diff_1 - diff_1 // 2)), 'constant')

    # ------------------------------------------

    # double check: if target image is not still the same size with target.
    if img.shape[0:2] != target_size:
        img = cv2.resize(img, target_size)

    # ---------------------------------------------------

    # normalizing the image pixels

    img_pixels = img_to_array(img)  # what this line doing? must?
    img_pixels = np.expand_dims(img_pixels, axis=0)
    img_pixels /= 255  # normalize input in [0, 1]

    # ---------------------------------------------------

    if return_region == True:
        return img_pixels, region
    else:
        return img_pixels


class _Layer:
    input_shape = (None, 112, 112, 3)
    output_shape = (None, 1, 128)


class SFaceModel:

    def __init__(self, model_path):

        self.model = cv2.FaceRecognizerSF.create(
            model=model_path,
            config="",
            backend_id=0,
            target_id=0)

        self.layers = [_Layer()]

    def predict(self, image):
        # Preprocess
        # revert the image to original format and preprocess using the model
        input_blob = (image[0] * 255).astype(np.uint8)

        # Forward
        embeddings = self.model.feature(input_blob)

        return embeddings


def represent(
        img_path, model_name='SFaceModel', model=None, enforce_detection=True, detector_backend='opencv', align=True,
        normalization='base', encode=False, base64_img=False):
    embedding = None
    try:
        # decide input shape
        input_shape_x, input_shape_y = find_input_shape(model)

        #detect and align
        img = preprocess_face(img=img_path, target_size=(input_shape_y, input_shape_x),
                              enforce_detection=enforce_detection, detector_backend=detector_backend, align=align, base64_img=base64_img)

        # ---------------------------------
        # custom normalization

        img = normalize_input(img=img, normalization=normalization)
        # represent
        embedding = model.predict(img)[0].tolist()
        # print(embedding)
        if encode:
            content = json.dumps(embedding)
            content = zlib.compress(content.encode('utf-8'))
            content = base64.b64encode(content)
            embedding = str(content, 'utf-8')
    except:
        pass
    return embedding


# https://www.delftstack.com/zh/howto/python/cosine-similarity-between-lists-python/
def partition_arg_topK(matrix, K, axis=0):
    """
    perform topK based on np.argpartition
    :param matrix: to be sorted
    :param K: select and sort the top K items
    :param axis: 0 or 1. dimension to be sorted.
    :return:
    """
    a_part = np.argpartition(matrix, K, axis=axis)
    if axis == 0:
        row_index = np.arange(matrix.shape[1 - axis])
        a_sec_argsort_K = np.argsort(
            matrix[a_part[0:K, :], row_index], axis=axis)
        return a_part[0:K, :][a_sec_argsort_K, row_index]
    else:
        column_index = np.arange(matrix.shape[1 - axis])[:, None]
        a_sec_argsort_K = np.argsort(
            matrix[column_index, a_part[:, 0:K]], axis=axis)
        return a_part[:, 0:K][column_index, a_sec_argsort_K]


def topk(array, k, reverse=True):
    ind = np.argpartition(array, -k)[-k:]
    if reverse:
        newind = np.argsort(array[ind])[::-1][:k]
    else:
        newind = np.argsort(array[ind])
    return ind[newind]


def topk_simlilar(List1, List2, k):
    # print(List1.shape, List2.shape)
    if isinstance(List1, list):
        List1 = np.array(List1)
    if isinstance(List2, list):
        List2 = np.array(List2)
    similarity_scores = np.dot(List1, List2) / (np.linalg.norm(List1, axis=1) * np.linalg.norm(List2))
    distance = 1 - similarity_scores

    threshold = findThreshold('SFace', 'cosine')
    if np.max(distance) > threshold:
        return None

    # print(distance)
    # print(findCosineDistance(List1.tolist()[0], List2.tolist()), findCosineDistance(List2.tolist(), List1.tolist()[0]))
    topk_index = topk(similarity_scores, k, reverse=True)
    return {"topk": topk_index.tolist(), "similarity": similarity_scores[topk_index].tolist()}


def test_cosine_similarity():
    # from numpy import dot
    # from numpy.linalg import norm
    np.random.seed(1)
    # List1 = np.array([4, 47, 8, 3])
    # List2 = np.array([3, 52, 12, 16])
    # result = dot(List1, List2)/(norm(List1)*norm(List2))
    # print(result)
    k = 1

    # List1 = np.array([[4, 47, 8, 3],
    #                   [1, 2000,  100,  2],
    #                   [2, 23,  6,  4],
    #                   [1, 2,  200,  2]])

    List1 = np.random.random((2, 128))
    List2 = np.random.random((1, 128))
    List2 = List2.squeeze()
    similarity_scores = List1.dot(List2) / (np.linalg.norm(List1, axis=1) * np.linalg.norm(List2))
    print(List1.shape, List2.shape)
    print(similarity_scores,  np.dot(List1, List2) / (np.linalg.norm(List1, axis=1) * np.linalg.norm(List2)))
    print(topk(similarity_scores, k, reverse=True))

    # np.array(self.qa_set.questions)[torch.topk(similarity, k)[1]]

    import torch
    import torch.nn.functional as F

    a = torch.FloatTensor(List1.tolist())

    # t2 = [4,54,3,7]
    b = torch.FloatTensor(List2.reshape(1, -1))
    # print(a.shape, b.shape)
    result = F.cosine_similarity(a, b, dim=1, eps=1e-8)
    print(result, torch.topk(result, k)[1])

    # from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
    # A = List1
    # B = List2
    # result = cosine_similarity(A.reshape(1, -1), B.reshape(1, -1))
    # print(result)


def verify_face(image_path, model, embeds, k=5, base64_img=False):
    verify_embed = represent(img_path=image_path, model=model, base64_img=base64_img)
    if verify_embed is None:
        return None

    if isinstance(verify_embed, list):
        verify_embed = np.array(verify_embed)

    # verify_embed = verify_embed.reshape(1, -1)
    if isinstance(embeds, list):
        embeds = np.array(embeds)
    if len(embeds.shape) == 1:
        k = 1
        embeds = embeds.reshape(1, -1)
    else:
        k = min(k, embeds.shape[0])
    # print(verify_embed.shape, embeds.shape, k)
    return topk_simlilar(embeds, verify_embed, k=k)


class ImageEmbeddings:

    def __init__(self) -> None:
        self.order_dict = OrderedDict()
        self.key_index = []
        self.embeds = []

    # add and update
    def add_file(self, file_path, model):
        if not os.path.exists(file_path):
            return False
        filename = os.path.basename(file_path)
        filename = os.path.splitext(filename)[0]
        embed = represent(img_path=file_path, model=model)
        if filename not in self.order_dict:
            self.key_index.append(filename)
        self.order_dict[filename] = embed
        return True

    def remove(self, key):
        if key in self.order_dict:
            del self.order_dict[key]
            self.key_index.remove(key)
            self.generate_embeds()
            return True
        else:
            return False

    def generate_embeds(self):
        self.embeds = []
        for key, val in self.order_dict.items():
            self.embeds.append(val)
        return self.embeds

    def verify_face(self, file_path, model, base64_img=False):
        if not base64_img and os.path.exists(file_path) or base64_img:
            if len(self.embeds) == 0:
                self.generate_embeds()
            ret = verify_face(file_path, model, self.embeds, base64_img=base64_img)
            try:
                ret["files"] = np.array(self.key_index)[ret["topk"]].tolist()
            except Exception as e:
                print(e)
            return ret

    def save(self, filename='embeds.pkl'):
        with open(filename, 'wb') as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)


def load_embeds(filename='embeds.pkl'):
    if os.path.exists(filename):
        with open(filename, 'rb') as inp:
            embeds = pickle.load(inp)
            return embeds


#: 'WzEsIDIsIDNd'
# decoded_list = base64.b64decode(b64_encoded_list)
# #: '[1, 2, 3]'
# my_list_again = json.loads(decoded_list)
# #: [1, 2, 3]
if __name__ == "__main__":
    model = SFaceModel("/home/faith/.deepface/weights/face_recognition_sface_2021dec.onnx")
    # print(model)
    # embeds = []
    # image_path = "/home/faith/MUSTPHD/deepface/me2.jpg"
    # embeds.append(represent(img_path=image_path, model=model))

    # image_path = "/home/faith/MUSTPHD/deepface/me.jpg"
    # embeds.append(represent(img_path=image_path, model=model))

    # topk_face = verify_face("/home/faith/MUSTPHD/deepface/me2.jpg", model, embeds)
    # print(topk_face)

    # b64_encoded_list = represent(img_path=image_path, model=model, encode=True)
    # print(len(b64_encoded_list))

    embed = ImageEmbeddings()
    embed.add_file("/home/faith/MUSTPHD/deepface/me2.jpg", model)

    # denglun
    # embed.add_file("/home/faith/aicmder/me2.png")

    embed.add_file("/home/faith/MUSTPHD/deepface/me.jpg", model)

    # embed.remove("me2")

    embed.save()
    e = load_embeds()
    print(e.order_dict.keys(), e.key_index)
    # print(e.verify_face("/home/faith/aicmder/dl/IMG_5972.JPG", model))
    # print(e.verify_face("/home/faith/aicmder/dl/IMG_8314.JPG", model))

    print("verify", e.verify_face("/home/faith/aicmder/dl/IMG_4259.JPG", model))
    # print("verify", e.verify_face("/home/faith/aicmder/dl/aaaaa.png", model))

    # image_file = "/home/faith/MUSTPHD/deepface/me.jpg"
    # with open(image_file,  'rb') as img_f:
    #     img = img_f.read()
    #     img_base64 = base64.b64encode(img).decode('utf8')
    #     print(e.verify_face(img_base64, model, base64_img=True))

    # print(e.verify_face("/home/faith/aicmder/dl/IMG_5029.jpg", model))
    # save(embed)

    # decoded_list = base64.b64decode(b64_encoded_list)
    # print(decoded_list, type(decoded_list))
    # embedding = json.loads(decoded_list.decode())
    # print(embedding)

    # test_cosine_similarity()
