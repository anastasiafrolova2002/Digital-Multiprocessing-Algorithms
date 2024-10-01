import cv2
import numpy as np

def GaussBlur(img, core_size, standard_deviation):
    core = np.ones((core_size, core_size))
    a = b = (core_size + 1) // 2

    for i in range(core_size):
        for j in range(core_size):
            core[i, j] = gauss(i, j, standard_deviation, a, b)

    print(core)

    sum = 0
    for i in range(core_size):
        for j in range(core_size):
            sum += core[i, j]

    for i in range(core_size):
        for j in range(core_size):
            core[i, j] /= sum

    print(core)

    imgBlur = img.copy()
    x_start = core_size // 2
    y_start = core_size // 2
    for i in range(x_start, imgBlur.shape[0] - x_start):
        for j in range(y_start, imgBlur.shape[1] - y_start):
            # операция свёртки
            val = 0
            for k in range(-(core_size // 2), core_size // 2 + 1):
                for l in range(-(core_size // 2), core_size // 2 + 1):
                    val += img[i + k, j + l] * core[k + (core_size // 2), l + (core_size // 2)]
            imgBlur[i, j] = val

    return imgBlur

def gauss(x, y, omega, a, b):
    omega2 = 2 * omega ** 2

    m1 = 1 / (np.pi * omega2)
    m2 = np.exp(-((x-a) ** 2 + (y-b) ** 2) / omega2)

    return m1 * m2

img = cv2.imread(r'C:/Users/User/Desktop/tomato_tiger.jpg', cv2.IMREAD_GRAYSCALE)

#def BlurFuss(img):
    #img = cv2.imread(r'C:/Users/User/Desktop/tomato_tiger.jpg', cv2.IMREAD_GRAYSCALE)

core_size = 5
standard_deviation = 100

imgBlur1 = GaussBlur(img, core_size, standard_deviation)
cv2.imshow(str(core_size) + 'x' + str(core_size) + ' and deviation ' + str(standard_deviation), imgBlur1)

core_size = 11
standard_deviation = 50

imgBlur2 = GaussBlur(img, core_size, standard_deviation)
cv2.imshow(str(core_size)+'x'+str(core_size) + ' and deviation ' + str(standard_deviation), imgBlur2)

imgBlurOpenCV = cv2.GaussianBlur(img, (core_size, core_size), standard_deviation)

cv2.imshow('img', img)
cv2.imshow('OpenCV_blur', imgBlurOpenCV)
cv2.waitKey(0)



#BlurFuss(img)
