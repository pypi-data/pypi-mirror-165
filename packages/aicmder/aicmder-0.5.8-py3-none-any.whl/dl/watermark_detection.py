from enum import unique
from torch_utils import InfiniteDataLoader
from huggingface_hub import hf_hub_url, cached_download
import os
from tqdm import tqdm
from PIL import Image
import numpy as np
from pathlib import Path

import torch
import torchvision
from torchvision import datasets, transforms, models
from torch.utils.data import Dataset
from torch.utils.data import BatchSampler, DataLoader
from torchvision import models
import torch.nn as nn
from fp16module import FP16Module
import time
from train_utils import smart_optimizer
from torch.optim import lr_scheduler
from copy import deepcopy
from datetime import datetime
import glob
import base64
import random
from torchmetrics.functional import precision_recall
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from aicmder.torch import freeze_parameter, train_params
from CustomNet import FC

def read_image_rgb(path):
    pil_img = Image.open(path)
    pil_img.load()
    if pil_img.format is 'PNG' and pil_img.mode is not 'RGBA':
        pil_img = pil_img.convert('RGBA')
    pil_img = pil_img.convert('RGB')
    return pil_img


def vprint(*args, verbose=True):
    if verbose:
        print(*args)


def seed_worker(worker_id):
    # Set dataloader worker seed https://pytorch.org/docs/stable/notes/randomness.html#dataloader
    worker_seed = torch.initial_seed() % 2 ** 32
    np.random.seed(worker_seed)
    random.seed(worker_seed)


classifier_transforms = transforms.Compose([
    transforms.Resize((320, 320)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# def predict_image(pil_image, model, device):
#     input_img = classifier_transforms(pil_image).float().unsqueeze(0)
#     outputs = model(input_img.to(device))
#     result = torch.max(outputs, 1)[1].cpu().reshape(-1).tolist()[0]
#     return result


class ImageDataset(Dataset):

    def __init__(self, objects):
        self.objects = objects
        self.resnet_transforms = classifier_transforms

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, idx):
        obj = self.objects[idx]
        assert isinstance(obj, (str, np.ndarray, Image.Image))
        if isinstance(obj, str):
            pil_img = read_image_rgb(obj)
        elif isinstance(obj, np.ndarray):
            pil_img = Image.fromarray(obj)
        elif isinstance(obj, Image.Image):
            pil_img = obj

        resnet_img = self.resnet_transforms(pil_img).float()

        return resnet_img





class WatermarksPredictor:

    def __init__(self, model, device, feature_extract=True, workers=6, bs=8, verbose=False, save_dir="./", name='resnext101_32x8d-large', fp16=False, cache_dir='weights/'):
        """
        Predict with watermark classifier using batches and torch.DataLoader
        resnet_model: watermark classifier model
        device: torch.device to use
        workers: number of workers for dataloader
        bs: batch size to use
        verbose: print additional info or not
        """
        config = MODELS[name]
        self.model = config['resnet'](pretrained=True)
        # pretrain_statedict = self.model.state_dict()

        if feature_extract:
            # Freeze
            freeze_parameter(self.model)
            # for param in self.model.parameters():
            #     param.requires_grad = False
        num_ftrs = self.model.fc.in_features

        # self.model.fc = nn.Sequential(nn.Linear(num_ftrs, 512),
        #                                 nn.ReLU(),
        #                                 nn.Dropout(0.2),
        #                                 nn.Linear(512, 2),
        #                                 nn.LogSoftmax(dim=1))
        self.model.fc = FC(num_ftrs)
        # self.model.fc = nn.Linear(num_ftrs, 2)

        if isinstance(model, str):
            # path, load checkpoint first
            # load checkpoint to CPU to avoid CUDA memory leak
            # import os, sys
            # sys_path = os.path.join(os.path.dirname(__file__), "CustomNet.py")
            # sys.path.append(sys_path)
            # print(sys_path)

            ckpt = torch.load(model, map_location='cpu')
            # csd = ckpt['model'].float().state_dict()
            csd = ckpt['model']
            self.model.load_state_dict(csd, strict=False)  # load
        else:
            config_file_url = hf_hub_url(
                repo_id=config['repo_id'], filename=config['filename'])
            cached_download(config_file_url, cache_dir=cache_dir,
                            force_filename=config['filename'])
            weights = torch.load(os.path.join(cache_dir, config['filename']), device)

            # for pretrain, train in zip(pretrain_statedict, weights):
            #     print(pretrain, train)
            # self.model.load_state_dict(weights)

        if fp16:
            self.model = FP16Module(self.model)

        self.model = self.model.to(device)
        self.model.eval()

        self.num_workers = workers
        self.bs = bs
        self.device = device
        self.verbose = verbose

        vprint(f'Using device {self.device}', verbose=self.verbose)
        save_dir = Path(save_dir)
        w = save_dir / 'train'  # weights dir
        w.mkdir(parents=True, exist_ok=True)  # make dir
        self.last, self.best = w / 'last.pt', w / 'best.pt'
        self.input_size = 320

    def run(self, files):
        """
        Processes input objects (list of paths, list of PIL images, list of numpy arrays) and returns model results.
        files: objects to process. Should be list of paths to images or list of PIL images or list of numpy arrays
        """
        # vprint(f'Files to process: {len(files)}', verbose=self.verbose)
        if isinstance(files, list):
            eval_dataset = ImageDataset(files)
        else:
            eval_dataset = datasets.ImageFolder(files, transforms.Compose([
                transforms.Resize((self.input_size, self.input_size)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [
                                     0.229, 0.224, 0.225])
            ]))

        loader = DataLoader(
            eval_dataset,
            sampler=torch.utils.data.SequentialSampler(eval_dataset),
            batch_size=self.bs,
            drop_last=False,
            num_workers=self.num_workers
        )
        if self.verbose:
            loader = tqdm(loader)

        preds, targets = [], []
        if isinstance(files, list):
            for batch in loader:
                with torch.no_grad():
                    outputs = self.model(batch.to(self.device))
                    _, pred = torch.max(outputs, 1)
                    preds.extend(pred.cpu().reshape(-1).tolist())

        else:
            for batch, target in loader:
                try:
                    with torch.no_grad():
                        outputs = self.model(batch.to(self.device))
                        _, pred = torch.max(outputs, 1)
                        preds.extend(pred.cpu().reshape(-1).tolist())
                        targets.extend(target.cpu().reshape(-1).tolist())
                except Exception as e:
                    pass

            preds = torch.tensor(preds)
            targets = torch.tensor(targets)
            # print(preds.shape, targets.shape)
            print(precision_recall(preds, targets, average='macro', num_classes=2))
        return preds

    # def freeze_conv_param(self):
    #     for v in self.model.modules():
    #         if isinstance(v, nn.modules.conv.Conv2d) and hasattr(v, 'weight') and isinstance(v.weight, nn.Parameter):
    #             # print("--")
    #             v.weight.requires_grad = False
    #         elif isinstance(v, torchvision.models.resnet.Bottleneck):
    #             if hasattr(v, 'conv1'):
    #                 v.conv1.weight.requires_grad = False
    #             if hasattr(v, 'conv2'):
    #                 v.conv2.weight.requires_grad = False
    #             if hasattr(v, 'conv3'):
    #                 v.conv3.weight.requires_grad = False
    #         else:
    #             print(type(v))

    def train(self, traindir, criterion=nn.CrossEntropyLoss(), start_epoch=0, epochs=1, opt='SGD', lr=0.01, lrf=0.01, momentum=0.937, weight_decay=0.0005, amp=False):
        # vprint(f'Files to process: {len(files)}', verbose=self.verbose)
        # train_dataset = ImageDataset(files)
        # loader = DataLoader(
        #     train_dataset,
        #     sampler=None, #torch.utils.data.SequentialSampler(train_dataset),
        #     batch_size=self.bs,
        #     pin_memory=True,
        #     drop_last=False,
        #     num_workers=self.num_workers
        # )
        image_dataset = datasets.ImageFolder(traindir, transforms.Compose([
            transforms.RandomResizedCrop(self.input_size),
            transforms.RandomHorizontalFlip(),
            # transforms.Resize((320, 320)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]))

        np_target = np.array(image_dataset.targets)
        unique_target = np.unique(np_target)

        # https://discuss.pytorch.org/t/how-to-handle-imbalanced-classes/11264/2
        class_sample_count = np.array(
            [len(np.where(np_target == t)[0]) for t in unique_target])
        weight = 1. / class_sample_count
        samples_weight = np.array([weight[t] for t in np_target])
        samples_weight = torch.from_numpy(samples_weight)
        samples_weight = samples_weight.double()
        sampler = torch.utils.data.WeightedRandomSampler(
            samples_weight, len(samples_weight))

        # target = torch.from_numpy(target).long()
        # train_dataset = torch.utils.data.TensorDataset(data, target)

        # print("size", train_size, image_dataset.imgs, samples_weight)
        loader = InfiniteDataLoader(
            image_dataset,
            # torch.utils.data.SequentialSampler(train_dataset),
            sampler=sampler,
            shuffle=False,
            batch_size=self.bs,
            pin_memory=True,
            drop_last=False,
            worker_init_fn=seed_worker,
            num_workers=self.num_workers
        )
        train_size = len(loader.dataset)  # len(image_dataset.imgs)

        nb = len(loader)  # number of batches
        criterion = criterion
        # optimizer = smart_optimizer(self.model, opt, lr, momentum, weight_decay)

        # params_to_update = self.model.parameters()
        params_to_update = train_params()
        optimizer = torch.optim.SGD(params_to_update, lr=0.001, momentum=0.9)

        def lr_lambda(x): return (1 - x / epochs) * (1.0 - lrf) + lrf  # linear
        scheduler = lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_lambda)
        scheduler.last_epoch = start_epoch - 1  # do not move
        # scaler = torch.cuda.amp.GradScaler(enabled=amp)

        # self.freeze_conv_param()
        best_train_acc = 0.0
        best_train_loss = None

        for epoch in range(start_epoch, epochs):
            self.model.train()

            train_count = 0

            if self.verbose:
                # progress bar
                loader = tqdm(loader, total=nb,
                              bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')

            running_loss = 0.0
            running_corrects = 0

            for batch_idx, (inputs, labels) in enumerate(loader):
                # print(batch_idx, inputs.shape, labels)
                # inputs = torch.autograd.Variable(inputs)
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)

                optimizer.zero_grad()

                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)

                # Input(N, C) where C = number of classes
                # target(N) where each value is 0 <= targets[i] <= C - 1
                loss = criterion(outputs, labels)

                loss.backward()

                optimizer.step()
                # optimizer.zero_grad()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
                train_count += inputs.size(0)

            # end batch
            lr = [x['lr'] for x in optimizer.param_groups]  # for loggers
            scheduler.step()

            epoch_loss = running_loss / train_count
            epoch_acc = running_corrects.double() / train_count

            print('training {} Loss: {:.4f} Acc: {:.4f} Count: {} Train_size: {}'.format(
                epoch + 1, epoch_loss, epoch_acc, train_count, train_size))

            if epoch_acc > best_train_acc or (epoch_acc == best_train_acc and not best_train_loss and epoch_loss < best_train_loss):
                best_train_acc = epoch_acc
                best_train_loss = epoch_loss
                state_dict = self.model.state_dict()
                ckpt = {
                    'epoch': epoch,
                    # 'model': deepcopy(self.model),
                    'model': state_dict,
                    'optimizer': optimizer.state_dict(),
                    # 'wandb_id': None,  # loggers.wandb.wandb_run.id if loggers.wandb else None,
                    'date': datetime.now().isoformat()}
                torch.save(ckpt, self.best)
                del ckpt
        state_dict = self.model.state_dict()
        ckpt = {
            'epoch': epoch,
            # 'model': deepcopy(self.model),
            'model': state_dict,
            'optimizer': optimizer.state_dict(),
            # 'wandb_id': None,  # loggers.wandb.wandb_run.id if loggers.wandb else None,
            'date': datetime.now().isoformat()}
        torch.save(ckpt, self.last)
        del ckpt


MODELS = {
    'resnext101_32x8d-large': dict(
        resnet=models.resnext101_32x8d,
        repo_id='boomb0om/dataset-filters',
        filename='watermark_classifier-resnext101_32x8d-input_size320-4epochs_c097_w082.pth',
    ),
    'resnext50_32x4d-small': dict(
        resnet=models.resnext50_32x4d,
        repo_id='boomb0om/dataset-filters',
        filename='watermark_classifier-resnext50_32x4d-input_size320-4epochs_c082_w078.pth',
    )
}


def check_result(ret, testFiles):
    total = len(testFiles)
    correct = 0
    for r, f in zip(ret, testFiles):
        dir_name = os.path.dirname(f)
        if str(r) in dir_name:
            correct += 1
        else:
            pass
            # vprint(f, 'watermark' if r == 1 else 'clear')
    print(correct, total, correct / total)


# https://www.cnblogs.com/wanghui-garcia/p/10679089.html

# https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html
# "https://download.pytorch.org/models/resnext101_32x8d-8ba56ff5.pth" to /home/faith/.cache/torch/hub/checkpoints/resnext101_32x8d-8ba56ff5.pth
def test_and_train():
    device = torch.device('cuda:0')
    # model_name = 'resnext50_32x4d-small'
    model_name = 'resnext101_32x8d-large'

    # bug
    # img = Image.open('/home/faith/aicmder/dl/dataset/1/Picture2.png')
    # img = Image.open('/home/faith/aicmder/dl/Picture5.png')
    # img = Image.open('/home/faith/aicmder/dl/dataset/0/3.jpg')

    # img = Image.open('/home/faith/aicmder/dl/1111.png')
    # predict
    # start = time.time()
    # res = predict_image(img, model, device)
    # end = time.time()
    # print(end - start, 'watermark' if res == 1 else 'clear')

    testFiles = glob.glob("/home/faith/aicmder/dl/dataset/*/*")
    # testFiles = ["/home/faith/aicmder/dl/dataset/0/IMG_5980.jpg"]

    # predictor = WatermarksPredictor("/home/faith/aicmder/train/best.pt", device, bs=256, verbose=True, name=model_name)
    # ret = predictor.run(testFiles)
    # print(ret)
    # check_result(ret, testFiles)

    print("-----------------------")
    # predictor = WatermarksPredictor(None, device, bs=32, verbose=True, name='resnext101_32x8d-large', feature_extract=False)
    predictor = WatermarksPredictor("/home/faith/aicmder/dl/train/last.pt", device, bs=32, verbose=True, name='resnext101_32x8d-large', feature_extract=False)
    criterion = nn.NLLLoss()
    predictor.train("/home/faith/aicmder/dl/dataset2", criterion=criterion, epochs=20, opt='Adam', lr=0.125)
    # ret = predictor.run(testFiles)
    # check_result(ret, testFiles)


def test_base64():
    from YoloModule import readb64
    device = torch.device('cuda:0')

    image_file = "/home/faith/aicmder/dl/dataset/0/IMG_5980.jpg"
    image_file = "/home/faith/aicmder/dl/room472.jpg"
    image_file = "/home/faith/aicmder/tests_model/wx1.png"
    image_file = "/home/faith/aicmder/dl/IMG_5980.jpg"
    image_file = "/home/faith/aicmder/tests_model/IMG_6006.JPG"
    image_file = "/home/faith/aicmder/dl/IMG_6007.JPG"
    # image_file = "/home/faith/aicmder/dl/IMG_6008.JPG"
    # image_file = "/home/faith/aicmder/dl/dataset/1/6.jpg"

    # image_file = "/home/faith/aicmder/dl/dataset/1/Picture5.png"
    # image_file = "/home/faith/aicmder/dl/dataset/1/Picture2.png"
    image_file = "/home/faith/aicmder/dl/dataset/1/Picture3.png"

    image_file = "/home/faith/aicmder/dl/dataset2/1/H2202286_image_20220525140211376.jpg"
    # image_file = "/home/faith/aicmder/dl/dataset2/1/H2202286_image_20220525140211477.jpg"
    image_file = "/home/faith/aicmder/dl/dataset2/1/H2022653_image_20210615003225318.JPG"
    image_file = "/home/faith/aicmder/dl/dataset2/1/H2022653_image_20210615003225232.JPG"
    with open(image_file,  'rb') as img_f:
        img = img_f.read()
        img_base64 = base64.b64encode(img).decode('utf8')
        img_bgr = readb64(img_base64)
        predictor = WatermarksPredictor(
            "/home/faith/aicmder/dl/train/last.pt", device, bs=4, verbose=True, name='resnext101_32x8d-large')
        # predictor = WatermarksPredictor(None, device, bs=32, verbose=True, name='resnext101_32x8d-large')

        # a = glob.glob("/home/faith/wm-nowm/d/*/*")
        # a = glob.glob("/home/faith/aicmder/dl/dataset/*/*")
        print(predictor.run([img_bgr]))

        # ret = predictor.run("/home/faith/wm-nowm/d/")
        # ret = predictor.run("/home/faith/aicmder/dl/dataset2")
        # print(ret)
        # check_result(ret, ret)


if __name__ == "__main__":
    # test_and_train()
    test_base64()