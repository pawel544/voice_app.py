
from scipy.io.wavfile import write , read
import sounddevice as sd
import os
import soundfile as sf
import PySimpleGUI  as sg
import queue
import numpy as np
import time

audio_queue = queue.Queue()
sample_rate = 44100
def audio_callback(indata,frames, time, status):

    audio_queue.put(indata.copy())

def start_recording( sample_rate, stop_event,pause_event,window):
    try:
        with sd.InputStream(samplerate=sample_rate, channels= 1, callback= 	audio_callback):
            frames = []
            while not stop_event.is_set():
                    if pause_event.is_set():
                        pause_event.wait()
                    frames.append(audio_queue.get())
            if frames:
                    audio = np.concatenate(frames, axis=0)
                    sf.write("sound/recorded.wav", audio, sample_rate)
            while not audio_queue.empty():
                audio_queue.get()
    except Exception as e:
        print(f"Błąd {e}")


def play_recording(sample_rate):
    rate,audio_data = read( mmap=False)
    odt= sd.play(audio_data, rate)
    sd.wait()