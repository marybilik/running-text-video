from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import cv2
import numpy as np

import cv2
import numpy as np

def generate_video(text, output_path):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)
    font_thickness = 2

    text_width, _ = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

    frame_width = 640
    frame_height = 480
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

    text_x = frame_width

    while text_x > -text_width:
        frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

        cv2.putText(frame, text, (text_x, 50), font, font_scale, font_color, font_thickness)

        out.write(frame)

        text_x -= 5  # Изменяем положение текста по горизонтали на каждом кадре

    out.release()

text = "Привет, мир!"
output_path = "output_video.avi"
generate_video(text, output_path)



def download_video(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')  # Получаем текст из формы

        video_name = 'running_text.avi'
        generate_video(text, video_name)

        # Отправляем видео для скачивания
        video_path = os.path.join(settings.BASE_DIR, video_name)
        with open(video_path, 'rb') as video_file:
            response = HttpResponse(video_file, content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="{video_name}"'
            return response

    return render(request, 'video.html')

