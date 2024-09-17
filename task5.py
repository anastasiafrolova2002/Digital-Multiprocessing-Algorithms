import cv2

cat1 = cv2.imread(r'C:/Users/User/Desktop/wizard_cat.png')
cat2 = cv2.imread(r'C:/Users/User/Desktop/wizard_cat.png')

cv2.namedWindow('cat normal wizard', cv2.WINDOW_NORMAL)
cv2.namedWindow('cat hsv wizard', cv2.WINDOW_NORMAL)

cv2.imshow('cat normal wizard',cat1)

hsv = cv2.cvtColor(cat2, cv2.COLOR_BGR2HSV)
cv2.imshow('cat hsv wizard', hsv)

cv2.waitKey(0)
cv2.destroyAllWindows()
