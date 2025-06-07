from recording.recording import start_recording, play_recording
from speech.speech import recognize_speech
import os
import threading
import PySimpleGUI as sg

if not os.path.exists("sound"):
    fol= os.mkdir("sound")

sample_rate = 44100
layout=[[sg.Text("Program")],
        [sg.Button("Nagrywaj"),sg.Button("Stop"), sg.Button("Odtwórz"), sg.Button("Notatka Głosowa"), sg.Button("EXIT")],
        [sg.Text(key='-OUTPUT-')]]

window = sg.Window(("Program"),layout, resizable= True)
while True:
    try:
        event, value = window.read()
        print(event, value)
        if event == sg.WIN_CLOSED or event == "EXIT":
            break
        elif event == "Nagrywaj":
           stop_event = threading.Event()
           thered= threading.Thread(target= start_recording, args=( sample_rate,stop_event))
           thered.start()
           window['-OUTPUT-'].update(f"Nagranie rospoczęte")
        elif event == "Stop":

            stop_event.set()
            thered.join()
           # is_recording = False
            #start_recording()
            window['-OUTPUT-'].update(f"Nagranie wstszymane")
        elif event == "Notatka Głosowa" :
            recognize_speech()
    except Exception as e:
        window['-OUTPUT-'].update(f"Wystąpił nieoczekiwany błąd {e}")
window.close()