import torch
import torch.nn as nn
import random
from torch.utils.data import Dataset,DataLoader
import os
from PIL import Image
import time
from captcha.image import ImageCaptcha
from torch.autograd import Variable
import numpy as np
from torchvision import transforms
import torch.nn.functional as F
import math
file_path = './data'
def random_captcha_text(char_set=['0','1','2','3','4','5','6','7','8','9'], captcha_size=4):  # 可以设置只用来生成数字
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text
def gen_capthcha_text_and_image(m):
    image = ImageCaptcha()
    captcha_text = random_captcha_text()  # 生成数字
    captcha_text = ' '.join(captcha_text)  # 生成标签

    image.write(captcha_text, "./data/image/" + '%.4d' % m + '.jpg')  # 保存图片

    # 将标签信息写入
    with open('./data' + "label.txt", "a") as f:
        f.write(captcha_text)
        f.writelines("\n")
# 加载数据集，自己重写DataSet类
class dataset(Dataset):
    # root_dir为数据目录，label_file，为标签文件
    def __init__(self, root_dir, label_file, transform=None):
        self.root_dir = root_dir
        self.label = np.loadtxt(label_file)
        self.transform = transform

    def __getitem__(self, idx):
        # 每个图片，其中idx为数据索引
        img_name = os.path.join(self.root_dir, '%.4d.jpg' % idx)
        image = Image.open(img_name)
        # 对应标签
        labels = self.label[idx, :]

        if self.transform:
            image = self.transform(image)

        return image, labels

    def __len__(self):
        return (self.label.shape[0])
# 自定义卷积网络模型
class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=4, stride=1, padding=2),  # 验证码的大小为(3,60,160)
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
        self.fc2 = nn.Linear(500, 40) # 每个图片中有4个数字，每个数字为10分类，所以为40个输出

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)  # reshape to (batch_size, 64 * 7 * 30)
        output = self.fc1(x)
        output = self.fc2(output)
        return output
# 自定义损失函数
class nCrossEntropyLoss(torch.nn.Module):

    def __init__(self, n=4):
        super(nCrossEntropyLoss, self).__init__()
        self.n = n
        self.total_loss = 0
        self.loss = nn.CrossEntropyLoss() # 交叉熵函数

    def forward(self, output, label):
        output_t = output[:, 0:10] # output：[_,40]，先提取出第一个数字对应的10列
        label = Variable(torch.LongTensor(label.data.cpu().numpy()))
        label_t = label[:, 0] # 提取第一个数字对应的label

        # 将其形状进行堆叠，变成[4*_,10]，变成4*图片数个数字
        for i in range(1, self.n):
            output_t = torch.cat((output_t, output[:, 10 * i:10 * i + 10]),
                                 0)  # 损失的思路是将一张图平均剪切为4张小图即4个多分类，然后再用多分类交叉熵方损失
            label_t = torch.cat((label_t, label[:, i]), 0)
            self.total_loss = self.loss(output_t, label_t)

        return self.total_loss
if __name__ == '__main__':
    dataset_size = 1000
    EPOCH = 10
    BATCH_SIZE = 32
    if not os.path.exists('./data/image/0000.jpg'):
        for i in range(dataset_size):
            gen_capthcha_text_and_image(i)
    # for i in range(dataset_size):
    #     gen_capthcha_text_and_image(i)
    transfrom = transforms.Compose([transforms.ToTensor()])
    dataset_data = dataset('./data/image','./datalabel.txt',transfrom)
    dataloader = DataLoader(dataset=dataset_data,batch_size=BATCH_SIZE)
    net = ConvNet()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.0001)
    loss_func = nCrossEntropyLoss()

    # 最好模型的权重，以及准确率
    best_model_wts = net.state_dict()
    best_acc = 0.0
    since = time.time()
    for epoch in range(EPOCH):
        running_loss = 0.0
        running_corrects = 0
        for step, (inputs, label) in enumerate(dataloader):
            pred = torch.LongTensor(len(inputs), 1).zero_()
            inputs = Variable(inputs)  # (bs, 3, 60, 240)
            label = Variable(label)  # (bs, 4)

            optimizer.zero_grad()

            output = net(inputs)  # (bs, 40),前向传播
            loss = loss_func(output, label)#求损失

            for i in range(4):
                pre = F.log_softmax(output[:, 10 * i:10 * i + 10], dim=1)  # (bs, 10)
                pred = torch.cat((pred, pre.data.max(1, keepdim=True)[1].cpu()), dim=1) #统计预测标签
            loss.backward()#反向传播
            optimizer.step()#更新参数

            running_loss += loss.data * inputs.size()[0]
            #         running_loss += loss.data[0] * inputs.size()[0]
            running_corrects += int((pred.numpy()[:, 1:].astype(int)==label.data.cpu().numpy().astype(int)).sum()/4)#统计正确预测数字的数量

        epoch_loss = running_loss / dataset_size
        epoch_acc = running_corrects / (dataset_size)

        if epoch_acc > best_acc:
            best_acc = epoch_acc
            best_model_wts = net.state_dict()

        if epoch == EPOCH - 1:
            # 保存模型
            torch.save(best_model_wts, file_path + '/best_model.pkl')

        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        print('Train Loss:{:.4f} Acc: {:.4f}'.format(epoch_loss, epoch_acc))
