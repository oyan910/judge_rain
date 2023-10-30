import cv2
import numpy as np


def dehaze(image, w=0.4, t0=0.4):
    # 计算图像的暗通道
    min_channel = np.min(image, axis=2)

    # 计算每个像素的大气光值
    atm_light = np.max(min_channel)

    # 估计透射率
    transmission = 1 - w * (min_channel / atm_light)

    # 限制透射率
    transmission = np.maximum(transmission, t0)

    # 估计场景辐射值
    scene_radiance = np.empty_like(image, dtype=np.uint8)
    for i in range(3):
        scene_radiance[:, :, i] = (image[:, :, i] - atm_light) / transmission + atm_light

    return scene_radiance


if __name__ == "__main__":
    # 读取有雾的图像
    image = cv2.imread('a1.jpg')

    # 去雾处理
    dehazed_image = dehaze(image)

    # 创建一个窗口来显示原始图像和去雾后的图像
    cv2.namedWindow('Dehazed Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Dehazed Image', np.hstack((image, dehazed_image)))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
