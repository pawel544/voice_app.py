import time

import PySimpleGUI as sg
import threading
import cv2
from PIL import Image
import io


def wideo(window, camer_control, start_video_event, stop_video_event):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 10.0
    recording = False
    out = None
    widht = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while not camer_control.is_set():

        ret, frame = cam.read()
        if not ret:
            continue

        if ret:
            try:
                # frame_small = cv2.resize(frame, (320, 240))
                frame_rbg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rbg)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)

                window.write_event_value("-IMAGE-", buf.getvalue())
                # window["-image-"].update(buf.getvalue())
                time.sleep(0.03)
            except Exception as e:
                print(f"{e}")
        if recording and out is not None:
            # print("lalal")
            out.write(frame)

        if start_video_event.is_set() and not recording:
            out = cv2.VideoWriter("lallal.avi", fourcc, fps, (widht, height))
            if not out.isOpened():
                print("Pompsuło się")
                recording = False
                out = None
            print("lalla")
            recording = True

        start_video_event.clear()
        if stop_video_event.is_set():
            if out and recording:
                recording = False
                out.release()

                out = None

                stop_video_event.clear()
                print("Zakończono")

    cam.release()

    cv2.destroyAllWindows()
