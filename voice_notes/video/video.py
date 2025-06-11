import PySimpleGUI as sg
import threading
import cv2
from PIL import Image
import io


def wideo(window, control_event, start_rec_event, stop_rec_event):
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 20.0
    recording = False
    out = None

    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while not control_event.is_set():
        ret, frame = cam.read()
        if not ret:
            continue

        # Convert image to PNG byte format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        window.write_event_value("-IMAGE-", buf.getvalue())

        # Start recording
        if start_rec_event.is_set() and not recording:
            out = cv2.VideoWriter("output.avi", fourcc, fps, (width, height))
            recording = True
            start_rec_event.clear()

        # Stop recording
        if stop_rec_event.is_set() and recording:
            recording = False
            if out:
                out.release()
                out = None
            stop_rec_event.clear()

        if recording and out:
            out.write(frame)

    cam.release()
    if out:
        out.release()
    cv2.destroyAllWindows()