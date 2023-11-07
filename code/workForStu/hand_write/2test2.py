# -*- coding: utf-8 -*-
"""
@File  : 2test2.py
@author: FxDr
@Time  : 2023/11/07 22:07
@Description:
"""
import torch
import torchvision.transforms as transforms
from PIL import Image
from matplotlib import pyplot as plt

# 导入模型定义类
from code.workForStu.model import FeedforwardNeuralNetModel

# 设备配置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载模型
model = FeedforwardNeuralNetModel().to(device)
model.load_state_dict(torch.load('./hand_write_model.pth', map_location=device))
model.eval()

# 图像处理转换器
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # 如果图片是RGB，转换为灰度图
    transforms.Resize((28, 28)),  # 将图片大小调整为28x28
    transforms.ToTensor(),  # 将图片转换为PyTorch张量
    transforms.Normalize((0.5,), (0.5,))  # 归一化
])

# 加载图片
image_path = '../../data/infer_3.png'
image = Image.open(image_path)

# 处理图片
image = transform(image).unsqueeze(0).to(device)  # 添加一个批次维度并发送到设备

# 预测
with torch.no_grad():
    output = model(image)
    _, predicted = torch.max(output.data, 1)

print(f'Predicted digit: {predicted.item()}')

# 可视化图片
plt.imshow(image.cpu().squeeze(), cmap='gray')  # 如果需要在CPU上运行，确保调用.cpu()
plt.show()
