from recording.recording import start_recording, play_recording
from video.video import wideo
from recording.time import record_timer
from speech.speech import recognize_speech
import os
import threading
import PySimpleGUI as sg

if not os.path.exists("sound"):
    fol= os.mkdir("sound")


#pause_event = None
#stop_event = None
#thered = None
sample_rate = 44100
layout=[[sg.Text("Program")],
        #[sg.Image(filename='', key='image')],
        [sg.Image(key="-IMAGE-")],
        [sg.Button("Nagrywaj"),sg.Button("Stop"), sg.Button("Odtwórz"), sg.Button("Notatka Głosowa"),
         sg.Button("Nagraj Wideo"), sg.Button("EXIT")]
         ,
        [sg.Button("Zatszymaj"), sg.Button("Wznów"), sg.Button("Rpzpocznij Nagranie"), sg.Button("zapisz nagranie")],
        [sg.Text(key='-OUTPUT-')],
        [sg.Text(key='-TIMER-')]]

window = sg.Window(("Program"),layout, resizable= True)
while True:
    try:
        event, value = window.read()

        if event == sg.WIN_CLOSED or event == "EXIT": break

        elif event == "Nagrywaj":

           pause_event = threading.Event()
           stop_event = threading.Event()
           thered= threading.Thread(target= start_recording, args=( sample_rate,stop_event,pause_event,window))
           thered.start()
           time_tender= threading.Thread(target= record_timer, args=(window,pause_event, stop_event))
           time_tender.start()

           window['-OUTPUT-'].update(f"Nagranie rospoczęte")
        elif event == "Nagraj Wideo":
           start_video_event = threading.Event()
           camer_control= threading.Event()
           pause_event = threading.Event()
           stop_event = threading.Event()
           stop_video_event =threading.Event()
           #thered = threading.Thread(target=start_recording, args=(sample_rate, stop_event, pause_event, window))
           thered_wideo = threading.Thread(target=wideo, args=(window,camer_control,start_video_event,stop_video_event))
           #time_tender = threading.Thread(target=record_timer, args=(window, pause_event, stop_event))

           thered_wideo.start()
           #thered.start()
           #time_tender.start()
           window['-OUTPUT-'].update(f'Start')
        elif event=="Rpzpocznij Nagranie":
            start_video_event.set()

        elif event == "zapisz nagranie":
            stop_video_event.set()
        elif event == "Stop":

            stop_event.set()
            thered.join()

            window['-OUTPUT-'].update(f"Nagranie wstszymane")
        elif event == '-TIMER-':
            window['-TIMER-'].update(value)
        elif event == "-IMAGE-":
            window["-IMAGE-"].update(data=value["-IMAGE-"])
        elif event =="Zatszymaj":
            pause_event.set()
        elif event == "Wznów":
            pause_event.clear()
        elif event == "Notatka Głosowa" :
            recognize_speech()

    except Exception as e:
        #window['-OUTPUT-'].update(f"Wystąpił nieoczekiwany błąd {e}")
        print(f"{e}")
window.close()