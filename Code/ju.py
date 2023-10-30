import cv2
import numpy as np

# 读取输入图像
image = cv2.imread('a1.jpg')

# 将图像转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
me = cv2.mean(gray)
print(f'图像平均数据:{me}')
# 计算透射率（Transmission）
mean_gray = me[0]  # 计算图像的平均亮度
transmission = 1 - mean_gray / 255.0  # 计算透射率

print(f'当前透射率：{transmission}')
# 阈值化透射率以判断是否有雾
threshold = 0.4  # 设置透射率阈值
has_haze = transmission <= threshold

# 显示结果
cv2.putText(image, f"Has Haze: {has_haze}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
