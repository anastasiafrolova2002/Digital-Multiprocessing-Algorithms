import cv2

def Lab5(kernel_size, standard_deviation, delta_tresh, min_area):
    video = cv2.VideoCapture(r'videos/DUCKS.MOV', cv2.CAP_ANY)#открываем видео

    ret, frame = video.read()#считываем первый кадр
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#переводим в чб
    img = cv2.GaussianBlur(img, (kernel_size, kernel_size), standard_deviation)#применяем размытие по гауссу

    #Настройка выходного видео
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(r'videos_out/OUT ' + str(i) + '.mp4', fourcc, 144, (w, h))#создаем видео для записи 

    while True:
        old_img = img.copy() # Сохраняем текущее изображение для расчета разности
        ok, frame = video.read()# Читаем новый кадр
        if not ok:# Проверяем, успешно ли прочитан кадр
            break # Выходим из цикла, если чтение завершено

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#
        img = cv2.GaussianBlur(img, (kernel_size, kernel_size), standard_deviation)#

        diff = cv2.absdiff(img, old_img)# Вычисляем разницу между текущим и старым кадром
        thresh = cv2.threshold(diff, delta_tresh, 255, cv2.THRESH_BINARY)[1]# Применяем пороговое значение для выделения изменений
        (contors, hierarchy) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# Находим контуры на основе порогового изображения

        for contr in contors:# Проходим по каждому найденному контуру
            area = cv2.contourArea(contr)# Вычисляем площадь контура

            if area < min_area:# Если площадь меньше минимальной, пропускаем
                continue
            video_writer.write(frame)# Записываем текущий кадр в выходное видео

    video_writer.release() # Освобождаем ресурсы записи видео

#
kernel_size = 3# размер гауссового ядра для размытия изображения
standard_deviation = 50#стандартное отклонение для гауссовского размытия
delta_tresh = 60#пороговое значение для определения изменений между кадрами
min_area = 20#минимальная площадь контура, чтобы он считался значимым
Lab5(kernel_size, standard_deviation, delta_tresh, min_area)
