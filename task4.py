import cv2

#задание 4 - записать видео в другой файл
def readIPWriteTOFile():
    video = cv2.VideoCapture(r'C:/Users/User/Downloads/vid1.mp4',cv2.CAP_ANY)
    ok, img = video.read()
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("C:/Users/User/Desktop/output.mov", fourcc, 25, (w, h))
    while (True):
        ok, img = video.read()
        cv2.imshow('img', img)
        video_writer.write(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

readIPWriteTOFile()