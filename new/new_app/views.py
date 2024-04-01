from django.shortcuts import render
from django.http import HttpResponse
import os
import cv2
import numpy as np

# Установка параметров видео
width, height = 100, 100
fps = 40
duration = 3  # длительность видео в секундах
text = "New text here"  # текст для бегущей строки

def generate_video():
     # Создание видеопотока
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('running_text.mp4', fourcc, fps, (width, height))

    # Создание кадров видео
    text_width = len(text) * 20
    for i in range(fps * duration):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        text_position = int((width - text_width) * i / (fps * duration))
        cv2.putText(frame, text, (text_position, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        out.write(frame)

    # Завершение записи видео
    out.release()
    cv2.destroyAllWindows()


def download_video(request):
    generate_video()
    video_path = os.path.join(os.getcwd(), 'running_text.mp4')
    video_file = open(video_path, 'rb')
    response = HttpResponse(video_file.read(), content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(video_path)
    video_file.close()
    return response

