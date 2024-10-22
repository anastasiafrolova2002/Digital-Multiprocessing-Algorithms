import cv2
import numpy as np

class TLDTracker:
    def __init__(self):
        self.tracking = False # флаг на отслеживание
        self.model = None # модель объекта для отслеживания

    def initialize(self, frame, bbox):
        self.tracking = True # флаг отслеживания
        self.model = frame[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]].copy()# сохраняем часть кадра для последующего отслеживания

    def track(self, frame):
        if not self.tracking:
            return None # если нет отслеживание
        
        # Простой метод трекинга: обратная корреляция (или просто поиск по шаблону)
        result = cv2.matchTemplate(frame, self.model, cv2.TM_CCOEFF_NORMED)# юзаем метод корреляции для поиска шаблона в текущем кадре
        _, _, _, max_loc = cv2.minMaxLoc(result)# находим координаты лучшего совпадения

        # обновляем координаты рамки
        return (max_loc[0], max_loc[1], self.model.shape[1], self.model.shape[0])# возвращаем обновленные координаты рамки вокруг найденного объекта

    def update_model(self, frame, bbox):
        self.model = frame[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]].copy()# обновляем модель (шаблон) на основе новых координат рамки

    def detect(self, frame):
        # Простая детекция: поиск шаблона
        result = cv2.matchTemplate(frame, self.model, cv2.TM_CCOEFF_NORMED)# применяем метод корреляции для обнаружения шаблона в текущем кадре
        _, _, _, max_loc = cv2.minMaxLoc(result)# находим координаты лучшего совпадения
        
        threshold = 0.8# устанавливаем порог для уверенности в обнаружении
        if result[max_loc[1], max_loc[0]] > threshold:# Проверяем, превышает ли совпадение порог
            return (max_loc[0], max_loc[1], self.model.shape[1], self.model.shape[0]) # Возвращаем координаты рамки
        else:
            return None# если совпадение низкое

if __name__ == "__main__":
    
    cap = cv2.VideoCapture('videos/red_yellow_toy_cars.mp4')  #  путь к видео
    output_path = f'C:/Users/User/Desktop/pp/red_yellow_toy_cars_tld_2_0.mp4'
    tracker = TLDTracker()# создаем экземпляр трекера
    path = 'videos/red_yellow_toy_cars.mp4'
    bbox = (220, 50, 50, 50)  # начальные координаты и размеры рамки
    ret, frame = cap.read()# читаем первый кадр из видео
    tracker.initialize(frame, bbox)# инициализируем трекер с первым кадром и рамкой
    fps = cap.get(cv2.CAP_PROP_FPS)# получаем количество кадров в секунду
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)# вычисление длительности видео
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC)) # получение кодека видео
    fourcc = chr(fourcc & 0xff) + chr((fourcc >> 8) & 0xff) + chr((fourcc >> 16) & 0xff) + chr((fourcc >> 24) & 0xff)# преобразование кода FourCC в строку
    print(f'{path} | {fourcc} | {w}x{h} | {fps} fps | {duration} seconds')

    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))  # создание объекта для записи видео.

    while cap.isOpened(): # запускаем цикл, пока видео открыто
        ret, frame = cap.read()# читаем следующий кадр
        
        if not ret:
            break

        tracked_bbox = tracker.track(frame)# попытка трекинга объекта на текущем кадре
        
        
        if tracked_bbox is not None:
            bbox = tracked_bbox# обновляем рамку
            timer = cv2.getTickCount()
            frametime = (cv2.getTickCount() - timer) / cv2.getTickFrequency()
            
            
        else:
            detected_bbox = tracker.detect(frame)# если трекинг не удался, пробуем обнаружить объект
            if detected_bbox is not None:
                bbox = detected_bbox# обновляем рамку

        # Рисуем прямоугольник вокруг объекта
        cv2.rectangle(frame, (bbox[0]+250, bbox[1]), (bbox[0] + bbox[2]+350, bbox[1] + bbox[3]+50), (73,73,0), 2)
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0]+200, bbox[1] -35), (73,73,0), -1)# черное окно для текста
        cv2.putText(frame, f'Tracker: TLD', (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame, f'FT: {round(frametime * 1000)} ms = {int(1 / frametime)} FPS', (bbox[0], bbox[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        video_writer.write(frame)
        # Отображаем результат
        cv2.imshow('TLD Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release() # освобождаем ресурсы видео
    cv2.destroyAllWindows()
