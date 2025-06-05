from scipy.io.wavfile import write , read
import sounddevice as sd
import os
import speech_recognition as sr
import soundfile as sf
import PySimpleGUI  as sg
import queue
import numpy as np
import threading


if not os.path.exists("sound"):
    fol= os.mkdir("sound")

audio_queue = queue.Queue()
layout=[[sg.Text("Program")],
        [sg.Button("Nagrywaj"),sg.Button("Stop"), sg.Button("Odtwórz"), sg.Button("Notatka Głosowa"), sg.Button("EXIT")],
        [sg.Text(key='-OUTPUT-')]]

window = sg.Window(("Program"),layout, resizable= True)

#czas=int(input("Podaj czas"))
sample_rate = 44100
def audio_callback(indata,frames, time, status):

    audio_queue.put(indata.copy())

def start_recording( sample_rate):
    global is_recording
    recording = True
    try:

        with sd.InputStream(samplerate=sample_rate, channels= 2, callback= 	audio_callback):
            frames = []

            while True:
                if is_recording:
                    frames.append(audio_queue.get())
                else:
                    audio = np.concatenate(frames, axis=0)
                    sf.write("sound/recorded.wav", audio, sample_rate)
                    break
    except Exception as e:
        print(f"Błąd{e}")


def play_recording(sample_rate):
    rate,audio_data = read( mmap=False)
    odt= sd.play(audio_data, rate)
    sd.wait()


def recognize_speech():
    r = sr.Recognizer()
    r.energy_threshold = 4000

    try:
        scie = os.path.abspath("dzwięk/dzwiek.wav")
        with sr.AudioFile(scie) as source:
            audio= r.record(source)
        text= r.recognize_google(audio, language="pl-PL")
        print("rozmoznano mowe", text)
        with open("recognized_text.txt", 'w', encoding="utf-8") as e:
            e.write(text)
    except sr.UnknownValueError:
        print("nie rozpoznano mowy")
    except Exception as e:
        print(f"niznany błąd {e}")
while True:
    try:
        event, value = window.read()
        print(event, value)
        if event == sg.WIN_CLOSED or event == "EXIT":
            break
        elif event == "Nagrywaj":
           thered= threading.Thread(target= start_recording, args=( sample_rate,))
           thered.start()
           window['-OUTPUT-'].update(f"Nagranie rospoczęte")
        elif event == "Stop":
            is_recording = False
            window['-OUTPUT-'].update(f"Nagranie wstszymane")
        elif event == "Notatka Głosowa" :
            recognize_speech()
    except Exception as e:
        window['-OUTPUT-'].update(f"Wystąpił nieoczekiwany błąd {e}")
window.close()