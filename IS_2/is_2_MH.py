
import cv2
import numpy as np

laplacian_kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])

# свертка
def convolve(img: np.ndarray, ker: np.ndarray) -> np.ndarray:

    B = np.zeros_like(img, np.int32)
    x0 = ker.shape[0] // 2
    y0 = ker.shape[1] // 2
    size_ker = int(ker.shape[0] // 2)
    for i in range(x0, B.shape[0] - x0):
        for j in range(y0, B.shape[1] - y0):
            val = 0

            for k in range(-size_ker, size_ker + 1):
                for l in range(-size_ker, size_ker + 1):
                    val += img[i + k, j + l] * ker[k + size_ker, l + size_ker]

                B[i, j] = val

    return B


# что-то про нули
def zero_crossing(image: np.ndarray, threshold: float = 0) -> np.ndarray:

    N, M = image.shape

    edges = np.zeros_like(image, dtype=np.uint8)
    for i in range(N):
        for j in range(M):
            if i > 0 and i < N - 1:
                left = image[i - 1, j]
                right = image[i + 1, j]
                if left * right < 0 and np.abs(left - right) > threshold:
                    edges[i, j] = 255
            if j > 0 and j < M - 1:
                up = image[i, j + 1]
                down = image[i, j - 1]
                if up * down < 0 and np.abs(up - down) > threshold:
                    edges[i, j] = 255
            if (i > 0 and i < N - 1) and (j > 0 and j < M - 1):
                up_left = image[i - 1, j - 1]
                down_right = image[i + 1, j + 1]
                down_left = image[i - 1, j + 1]
                up_right = image[i + 1, j - 1]
                if (
                        up_left * down_right < 0
                        and np.abs(up_left - down_right) > threshold
                ):
                    edges[i, j] = 255
                elif (
                        down_left * up_right < 0
                        and np.abs(down_left - up_right) > threshold
                ):
                    edges[i, j] = 255
    return edges


# сам алгоритм
def marrhildreth(image, sigma, threshold, size_ker):


    blurred=cv2.GaussianBlur(image, (size_ker, size_ker), sigma)
    laplacian = convolve(blurred, laplacian_kernel)

    edges = zero_crossing(laplacian, threshold=threshold)
    return edges


img = cv2.imread(r'C:/Users/User/Desktop/pp/pics/5.jpg', cv2.IMREAD_GRAYSCALE)

size_ker = 5
sigma=30
threshold=13

edges = marrhildreth(img, sigma=sigma, threshold=threshold, size_ker=size_ker)
small = cv2.resize(edges, (0,0), fx=0.5, fy=0.5) 
cv2.imshow('Marr–Hildreth', small)

cv2.waitKey(0)
cv2.destroyAllWindows()
