import cv2
import numpy as np

img = cv2.imread(r'C:/Users/User/Desktop/tomato_tiger.jpg', cv2.IMREAD_GRAYSCALE)

core_size = 11
standard_deviation = 50

imgBlurOpenCV = cv2.GaussianBlur(img, (core_size, core_size), standard_deviation)

cv2.imshow('TOMATO-TIGER', img)
cv2.imshow('BLURY TOMATO-TIGER', imgBlurOpenCV)
cv2.waitKey(0)
