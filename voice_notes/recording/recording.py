
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
            last_update_time = 0
            start = time.time()
            while not stop_event.is_set():
                    if pause_event.is_set():

                        pause_event.wait()

                    frames.append(audio_queue.get())
                    elapse = (time.time() - start)
                    if elapse - last_update_time > 0.2:
                        window.write_event_value('-TIMER-', f"{elapse:.2f}")
                        last_update_time = elapse


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