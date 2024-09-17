import cv2
#задание 2 - картинки
pic1 = cv2.imread(r'C:/Users/User/Desktop/MmGD5hxHhPA.jpg',cv2.IMREAD_GRAYSCALE)
pic2 = cv2.imread(r'C:/Users/User/Desktop/wizard_cat.png',cv2.IMREAD_COLOR)
pic3 = cv2.imread(r'C:/Users/User/Desktop/idk.bmp',cv2.IMREAD_UNCHANGED)
pic3 = cv2.bitwise_not(pic3)
cv2.namedWindow('leaf', cv2.WINDOW_NORMAL)
cv2.namedWindow('cato', cv2.WINDOW_NORMAL)
cv2.namedWindow('time', cv2.WINDOW_NORMAL)
cv2.imshow('leaf',pic1)
cv2.imshow('cato', pic2)
cv2.imshow('time', pic3)
cv2.waitKey(0)
cv2.destroyAllWindows()
