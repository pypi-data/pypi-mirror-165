import torch.nn as nn


class FC(nn.Module):
    def __init__(self, inFeat, nbCls=2, dropoutRatio=0.2):
        super(FC, self).__init__()
        # self.dropout = nn.Dropout(dropoutRatio)
        # self.fc1 = nn.Linear(inFeat, nbCls)
        self.sequential = nn.Sequential(nn.Linear(inFeat, 512),
                                        nn.ReLU(),
                                        nn.Dropout(dropoutRatio),
                                        nn.Linear(512, nbCls),
                                        nn.LogSoftmax(dim=1))

    def forward(self, x):
        # x = self.dropout(x)
        # x = self.fc1(x)
        x = self.sequential(x)
        return x