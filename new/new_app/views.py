from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import cv2
import numpy as np
from .models import RequestHistory


def generate_video(text, output_path):
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_color = (255, 255, 255)
    font_thickness = 2

    frame_width = 100
    frame_height = 100
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    text_length = cv2.getTextSize(text, font, font_scale, font_thickness)[0][0]
    scroll_speed = text_length / (3 * 30)  # Вычисляем скорость прокрутки текста для показа за 3 секунды

    out = cv2.VideoWriter(output_path, fourcc, 30, (frame_width, frame_height))

    text_x = frame_width

    while text_x > -text_length:
        frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

        cv2.putText(frame, text, (int(text_x), 50), font, font_scale, font_color, font_thickness)


        out.write(frame)

        text_x -= scroll_speed

    out.release()

    history_entry = RequestHistory.objects.create(text=text)
    history_entry.save()




def download_video(request):
    
    if request.method == 'POST':
        text = request.POST.get('text', '')  # Получаем текст из формы

        video_name = 'running_text.avi'
        generate_video(text, video_name)

        

        # Отправляем видео для скачивания
        video_path = os.path.join(settings.BASE_DIR, video_name)
        with open(video_path, 'rb') as video_file:
            response = HttpResponse(video_file, content_type='video/avi')
            response['Content-Disposition'] = f'attachment; filename="{video_name}"'
            return response

    return render(request, 'video.html')

