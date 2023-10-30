# https://www.pianshen.com/article/949473269/
# author:ljj
# time:2021/7
import cv2
import math
import numpy as np
import time

class RmvFog:  # remove fog from video

    def __init__(self):
        None

    def DarkChannel(self, im, sz):
        b, g, r = cv2.split(im)
        dc = cv2.min(cv2.min(r, g), b);
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (sz, sz))
        dark = cv2.erode(dc, kernel)
        return dark

    def AtmLight(self, im, dark):
        [h, w] = im.shape[:2]
        imsz = h * w
        numpx = int(max(math.floor(imsz / 1000), 1))
        darkvec = dark.reshape(imsz, 1);
        imvec = im.reshape(imsz, 3);

        indices = darkvec.argsort();
        indices = indices[imsz - numpx::]

        atmsum = np.zeros([1, 3])
        for ind in range(1, numpx):
            atmsum = atmsum + imvec[indices[ind]]

        A = atmsum / numpx;
        return A

    def TransmissionEstimate(self, im, A, sz):
        omega = 0.95;
        im3 = np.empty(im.shape, im.dtype);

        for ind in range(0, 3):
            im3[:, :, ind] = im[:, :, ind] / A[0, ind]

        transmission = 1 - omega * self.DarkChannel(im3, sz);
        return transmission

    def Guidedfilter(self, im, p, r, eps):
        mean_I = cv2.boxFilter(im, cv2.CV_64F, (r, r));
        mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r));
        mean_Ip = cv2.boxFilter(im * p, cv2.CV_64F, (r, r));
        cov_Ip = mean_Ip - mean_I * mean_p;

        mean_II = cv2.boxFilter(im * im, cv2.CV_64F, (r, r));
        var_I = mean_II - mean_I * mean_I;

        a = cov_Ip / (var_I + eps);
        b = mean_p - a * mean_I;

        mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r));
        mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r));

        q = mean_a * im + mean_b;
        return q;

    def TransmissionRefine(self, im, et):
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY);
        gray = np.float64(gray) / 255;
        r = 60;
        eps = 0.0001;
        t = self.Guidedfilter(gray, et, r, eps);

        return t;

    def Recover(self, im, t, A, tx=0.1):
        res = np.empty(im.shape, im.dtype);
        t = cv2.max(t, tx);

        for ind in range(0, 3):
            res[:, :, ind] = (im[:, :, ind] - A[0, ind]) / t + A[0, ind]

        return res

    def RemoveSmoke(self, img):
        # src = cv2.imread(img);
        src = img
        I = src.astype('float64') / 255;
        dark = self.DarkChannel(I, 15);
        A = self.AtmLight(I, dark);
        te = self.TransmissionEstimate(I, A, 15);
        t = self.TransmissionRefine(src, te);
        J = self.Recover(I, t, A, 0.1);
        arr = np.hstack((I, J))
        return arr


if __name__ == '__main__':
    start_time = time.time()  # 记录开始时间
    import sys

    try:
        fn = sys.argv[1]
    except:
        fn = 'a1.jpg'


    def nothing(*argv):
        pass


    a = RmvFog()
    src = cv2.imread(fn);
    I = src.astype('float64') / 255;
    dark = a.DarkChannel(I, 15);
    A = a.AtmLight(I, dark);
    te = a.TransmissionEstimate(I, A, 15);
    t = a.TransmissionRefine(src, te);
    J = a.Recover(I, t, A, 0.1);
    arr = np.hstack((I, J))
    cv2.imshow("contrast", arr)
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算时间差
    print(f"运行时间: {elapsed_time:.2f} 秒")
    cv2.imwrite("dehaze.png", J * 255)
    cv2.imwrite("contrast.png", arr * 255);
    cv2.waitKey();