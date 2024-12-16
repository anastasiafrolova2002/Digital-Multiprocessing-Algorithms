import cv2
import numpy as np


def GAUSBlur(filepath: str, blur_kernel_size: int, scale: float = 1):  #шаг 1 и 2
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    small = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
    return cv2.GaussianBlur(small, (blur_kernel_size, blur_kernel_size), cv2.BORDER_DEFAULT)


def svertka(grayscale_image: np.ndarray, kernel: np.ndarray):
    result = np.zeros_like(grayscale_image, np.int32)   #результат
    h, w = grayscale_image.shape[:2]                    #размеры изображения
    kernel_size = kernel.shape[0]                       #размер ядра
    half_kernel_size = int(kernel_size // 2)            #половина размера ядра для обхода пикселей

    # идем по каждому пикселю изображения без границы
    for y in range(half_kernel_size, h - half_kernel_size):
        for x in range(half_kernel_size, w - half_kernel_size):

            val = 0# сумма свертки для текущего пикселя

            # идем по каждому элементу ядра
            for k in range(-half_kernel_size, half_kernel_size + 1):
                for l in range(-half_kernel_size, half_kernel_size + 1):
                    # умножаем пиксели изображения на соответствующие элементы ядра и складываем
                    val += grayscale_image[y + k, x + l] * kernel[half_kernel_size + k, half_kernel_size + l]

            result[y, x] = val# записываем полученное значение в результат
    return result


def angle_value(x, y, tang):
    if (x >= 0 and y <= 0 and tang < -2.414) or (x <= 0 and y <= 0 and tang > 2.414):
        return 0#сер
    elif x >= 0 and y <= 0 and tang < -0.414:
        return 1#корич
    elif (x >= 0 and y <= 0 and tang > -0.414) or (x >= 0 and y >= 0 and tang < 0.414):
        return 2#крас
    elif x >= 0 and y >= 0 and tang < 2.414:
        return 3#оранж
    elif (x >= 0 and y >= 0 and tang > 2.414) or (x <= 0 and y >= 0 and tang < -2.414):
        return 4#желт
    elif x <= 0 and y >= 0 and tang < -0.414:
        return 5#зел
    elif (x <= 0 and y >= 0 and tang > -0.414) or (x <= 0 and y <= 0 and tang < 0.414):
        return 6#голуб
    elif x <= 0 and y <= 0 and tang < 2.414:
        return 7#син


def edge_detection(grayscale_image: np.ndarray, lower_bar: float = None, high_bar: float = None, show_grad: bool = False, show_nms: bool = False):
     # Определение матриц Собеля для вычисления градиентов по горизонтали и вертикали
    ker_x = np.array([[3, 0, -3], [10, 0, -10], [3, 0, -3]])#[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]   #[[1, 0, -1], [1, 0, -1], [1, 0, -1]]
    ker_y = np.array([[3, 10, 3], [0, 0, 0], [-3, -10, -3]])#[[-1, -2, -1], [0, 0, 0], [1, 2, 1]]   #[[1, 1, 1], [0, 0, 0], [-1, -1, -1]]

    #применяем свертку для получения градиентов
    gx = svertka(grayscale_image, ker_x)
    gy = svertka(grayscale_image, ker_y)

    #шаг 3
    #длины и углы градиентов
    grad_len = np.sqrt(np.add(np.square(gx), np.square(gy))) # длина вектора град = (gx^2+gy^2)^0.5
    max_grad_len = grad_len.max()
    if show_grad:# Если указан флаг отображения градиентов
        cv2.imshow('Magic Cato GRADIENT', (grad_len / max_grad_len * 255).astype(np.uint8)) # показать градиенты

    tang = np.divide(gy, gx)# вычисление тангенса угла градиента
    tang = np.nan_to_num(tang)# Замена NaN на 0
    print(grad_len) # Вывод длины градиента
    print(tang)# Вывод углов градиента


    # Non-maximum suppression              3
    edges = np.zeros_like(grayscale_image)# создание пустого изображения для границ

    for y in range(1, edges.shape[0] - 1): # проход по всем пикселям, не включая границы
        for x in range(1, edges.shape[1] - 1):
            angle = angle_value(gx[y, x], gy[y, x], tang[y, x])# получение значения угла
            # Определение соседних пикселей в зависимости от угла
            if angle == 0 or angle == 4:
                neighbor1 = [y - 1, x]
                neighbor2 = [y + 1, x]
            elif angle == 1 or angle == 5:
                neighbor1 = [y - 1, x + 1]
                neighbor2 = [y + 1, x - 1]
            elif angle == 2 or angle == 6:
                neighbor1 = [y, x + 1]
                neighbor2 = [y, x - 1]
            elif angle == 3 or angle == 7:
                neighbor1 = [y + 1, x + 1]
                neighbor2 = [y - 1, x - 1]
            else:
                raise Exception('Angle not defined')
            if grad_len[y, x] >= grad_len[neighbor1[0], neighbor1[1]] and grad_len[y, x] > grad_len[neighbor2[0], neighbor2[1]]:# Сравнение текущего градиента с соседними
                edges[y, x] = 255  # пометка пикселя как границы
    
    if show_nms:# Отображение границ, если указан соответствующий флаг
        cv2.imshow('Magic Cato NON MAX', edges)

    # Double threshold filtering           task 4
    max_grad_len = grad_len.max() # максимальная длина градиента
    low_level = int(max_grad_len * lower_bar)  # низкий порог
    high_level = int(max_grad_len * high_bar)# высокий порог
    for y in range(edges.shape[0]):# проход по всем пикселям
        for x in range(edges.shape[1]):
            if edges[y, x] > 0: # если пиксель часть границы
                if grad_len[y, x] < low_level:
                    edges[y, x] = 0# убираем, если градиент ниже низкого порога
                elif grad_len[y, x] < high_level:
                    keep = False # флаг для хранения пикселя
                    # проверка соседей на высокий градиент
                    for neighbor_y in (y - 1, y, y + 1):
                        for neighbor_x in (x - 1, x, x + 1):
                            if neighbor_y != y or neighbor_x != x:
                                if edges[neighbor_y, neighbor_x] > 0 and grad_len[neighbor_y, neighbor_x] >= high_level:
                                    keep = True # сохраняем, если соседний пиксель границ
                    if not keep:
                        edges[y, x] = 0# убираем, если нет соседей с высоким градиентом

    return edges # возвращаем изображение с границами


if __name__ == '__main__':
    folder = 'pics/'
    images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']
    img = cv2.imread(r'pics/lazy.jpg', cv2.IMREAD_GRAYSCALE)
    small = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 

    select = 4

    scale = 1
    blur = 9
    lower_bar = 0.05
    high_bar = 0.15

    image = GAUSBlur(folder + images[select - 1], blur, scale) #image = GAUSBlur(folder + images[select - 1], blur, scale)
    edges = edge_detection(image, lower_bar, high_bar, show_grad=True, show_nms=True)

    cv2.imshow('Magic Cato Blur', image)
    cv2.imshow('DOUBLE FILTER', edges)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
