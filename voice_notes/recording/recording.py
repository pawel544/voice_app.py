from scipy.io.wavfile import write , read
import sounddevice as sd
import os
import soundfile as sf
import PySimpleGUI  as sg
import queue
import numpy as np


audio_queue = queue.Queue()
sample_rate = 44100
def audio_callback(indata,frames, time, status):

    audio_queue.put(indata.copy())

def start_recording( sample_rate, stop_event):

    try:

        with sd.InputStream(samplerate=sample_rate, channels= 1, callback= 	audio_callback):
            frames = []

            while not stop_event.is_set():

                    frames.append(audio_queue.get())


            if frames:
                    audio = np.concatenate(frames, axis=0)
                #if stop_event.is_set():

                    sf.write("sound/recorded.wav", audio, sample_rate)
            while not audio_queue.empty():
                audio_queue.get()
    except Exception as e:
        print(f"Błąd {e}")


def play_recording(sample_rate):
    rate,audio_data = read( mmap=False)
    odt= sd.play(audio_data, rate)
    sd.wait()