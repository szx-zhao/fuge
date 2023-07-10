import torch
import torch.nn as nn
import random
from torch.utils.data import Dataset
import os
from PIL import Image
import time
from torchvision import transforms

class ConvNet(nn.Module):

    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=4, stride=1, padding=2),  # in:(bs,3,60,160)
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.2, inplace=True),
            nn.MaxPool2d(kernel_size=2),  # out:(bs,32,30,80)

            nn.Conv2d(32, 64, kernel_size=4, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2, inplace=True),
            nn.MaxPool2d(kernel_size=2),  # out:(bs,64,15,40)

            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2, inplace=True),
            nn.MaxPool2d(kernel_size=2)  # out:(bs,64,7,20)
        )

        self.fc1 = nn.Linear(64 * 7 * 20, 500)
        self.fc2 = nn.Linear(500, 40)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)  # reshape to (batch_size, 64 * 7 * 30)
        output = self.fc1(x)
        output = self.fc2(output)

        return output

def predict_number(img_path):
    img = Image.open(img_path)
    img = transforms.ToTensor()(img)
    img = torch.unsqueeze(img, dim=0)

    # 加载模型权重
    model = ConvNet()
    model.load_state_dict(torch.load('back-end/data/best_model.pkl'))
    pred = model(img)
    pred_t = pred[:, 0:10]

    for i in range(1, 4):
        pred_t = torch.cat((pred_t, pred[:, 10 * i:10 * i + 10]), 0)
    predict_cla = torch.argmax(pred_t, dim=1)
    return predict_cla.numpy()


# img_path = r'back-end/test_data/0000.jpg'
# predicted_number = predict_number(img_path)
# print(predicted_number)