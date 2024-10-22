import cv2
import numpy as np

trackers = {#доступные трекеры
    'csrt': cv2.TrackerCSRT.create,                     # ! пикачу я выбираю тебя !
    'kcf': cv2.TrackerKCF.create,
    'medianflow': cv2.legacy.TrackerMedianFlow.create,
    'mosse': cv2.legacy.TrackerMOSSE.create,
    'mil': cv2.TrackerMIL.create,
    'tld': cv2.legacy.TrackerTLD.create,                # ! пикачу я выбираю тебя !
    'boosting': cv2.legacy.TrackerBoosting.create,      # ! пикачу я выбираю тебя !
}

videos = ['cats_run', 'dance', 'ducks_1', 'pikachu', 'red_yellow_toy_cars']

# Настройки
name = videos[2]# номер видео
path = f'videos/{name}.mp4'
tracker_selection = 'boosting'# сюда заменяется имя метода, например: tld 
reset_tracker_on_fail = False # Настройка сброса трекера при потере объекта.
write_video = True# Опция записи видео.
#win_name = name+tracker_selection
window_name = 'Tracking'
window_size = (1024, 576)
output_path = f'C:/Users/User/Desktop/pp/{name}_{tracker_selection}.mp4'
 #video_writer = cv2.VideoWriter("C:/Users/User/Desktop/output.mov", fourcc, 25, (w, h))

cap = cv2.VideoCapture(path)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)# Вычисление длительности видео.
fourcc = int(cap.get(cv2.CAP_PROP_FOURCC)) # Получение кодека видео.
fourcc = chr(fourcc & 0xff) + chr((fourcc >> 8) & 0xff) + chr((fourcc >> 16) & 0xff) + chr((fourcc >> 24) & 0xff)# Преобразование кода FourCC в строку.
print(f'{path} | {fourcc} | {w}x{h} | {fps} fps | {duration} seconds')
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, *window_size)
tracker = trackers[tracker_selection]()# Инициализация выбранного трекера.
roi = None# Переменная для хранения области интереса (ROI).
if write_video:
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

while True:
    ok, frame = cap.read()
    key = cv2.waitKey(1) & 0xFF
    if not ok or key == 27:
        break

    if roi is not None:
        timer = cv2.getTickCount()
        success, box = tracker.update(frame)
        frametime = (cv2.getTickCount() - timer) / cv2.getTickFrequency()
        if success:
            x, y, w, h = [int(c) for c in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (133, 143, 0), 2)# окно для объекта
            cv2.rectangle(frame, (x, y), (x+177, y -35), (73,73,0), -1)# черное окно для текста
            cv2.putText(frame, f'Tracker: {tracker_selection.upper()}', (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, f'FT: {round(frametime * 1000)} ms = {int(1 / frametime)} FPS', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        else:
            print('Target Loss')
            cv2.putText(frame, 'Target Loss', (w+150, h+100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (10, 0, 255), 2, cv2.LINE_AA)
            if reset_tracker_on_fail:
                roi = None
                tracker = trackers[tracker_selection]()
    else:
        cv2.putText(frame, 'Press "s" to select ROI', (20, h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow('Tracking', frame)
    if key == ord('s'):
        roi = cv2.selectROI(window_name, frame)
        tracker = trackers[tracker_selection]()
        tracker.init(frame, roi)
    elif key == ord('x'):
        roi = None
    if write_video:
        video_writer.write(frame)

cv2.destroyAllWindows()
