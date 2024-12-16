
import cv2
import numpy as np
# Чтение изображения
img = cv2.imread(r'C:/Users/User/Desktop/pp/pics/5.jpg', cv2.IMREAD_GRAYSCALE)
# Применение пороговой обработки для бинаризации изображения
_, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
# Поиск контуров
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Отрисовка контуров на изображении
cv2.drawContours(img, contours, -1, (255, 0, 0), 2)  
small = cv2.resize(img, (0,0), fx=0.3, fy=0.3) 
# Отображение изображения с контурами
cv2.imshow('Contours', small)
cv2.waitKey(0)
cv2.destroyAllWindows()
