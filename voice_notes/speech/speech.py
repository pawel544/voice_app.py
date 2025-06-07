import speech_recognition as sr
import os


def recognize_speech():
    r = sr.Recognizer()
    r.energy_threshold = 4000

    try:
        scie = os.path.abspath("sound/recorded.wav")
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