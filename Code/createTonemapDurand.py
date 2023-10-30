import cv2
import numpy as np

def dehaze(image, t_min=3, A=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean_t = np.mean(gray) / 255.0
    t = cv2.blur(gray, (9, 9)).astype(np.float32) / 255.0

    t = np.maximum(t, t_min)

    # 扩展透射率通道数
    t = cv2.cvtColor(t, cv2.COLOR_GRAY2BGR)

    J = (image - A) / t + A
    J = np.uint8(np.clip(J, 0, 255))
    return J

# 读取图像
image = cv2.imread('a1.jpg')

# 进行去雾操作
dehazed_image = dehaze(image)

# 保存去雾后的图像
cv2.imwrite('dehazed_image.jpg', dehazed_image)

# 显示原始图像和去雾后的图像
cv2.imshow('Original Image', image)
cv2.imshow('Dehazed Image', dehazed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
