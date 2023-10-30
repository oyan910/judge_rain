import cv2
import numpy as np

# 读取图片
img_path = "a1.jpg"
img = cv2.imread(img_path)

# 显示原图
cv2.imshow("original", img)
cv2.waitKey(0)

# 计算暗通道图像
patch_size = 15
half_patch_size = (patch_size - 1) // 2
dark_channel = np.zeros((img.shape[0], img.shape[1]), np.uint8)
for i in range(half_patch_size, img.shape[0] - half_patch_size):
    for j in range(half_patch_size, img.shape[1] - half_patch_size):
        patch = img[i - half_patch_size:i + half_patch_size + 1, j - half_patch_size:j + half_patch_size + 1]
        dark_channel[i, j] = np.min(patch)

# 显示暗通道图像
cv2.imshow("dark_channel", dark_channel)
cv2.waitKey(0)

# 估计大气浓度
top_num = int(np.prod(img.shape[:2]) * 0.001)
dark_channel_flat = dark_channel.flatten()
indices = dark_channel_flat.argsort()[-top_num:]
atmosphere = np.zeros(3)
for index in indices:
    atmosphere += img.reshape(-1, 3)[index]
atmosphere = atmosphere / top_num

print("atmosphere:", atmosphere)

# 图像去雾
t = 0.1
omega = 0.95
img_norm = img / 255.0
transmission = 1 - omega * dark_channel.astype("float32") / np.max(dark_channel)
for i in range(3):
    img_norm[:, :, i] = (img_norm[:, :, i] - atmosphere[i]) / transmission + atmosphere[i]
img_norm = np.clip(img_norm, 0, 1)

# 显示去雾后的图像
cv2.imshow("dehazed", img_norm)
cv2.waitKey(0)
