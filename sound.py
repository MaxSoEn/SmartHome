import pyaudio
import wave
import time
import speech_recognition as sr

class sound:

    def  __init__(self):
        # initialize the recognizer
        self.r = sr.Recognizer()
    def record(self, delay = 3):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
        self.frames = []
        try:
            self.t = time.time()
            print("START")
            while True:
                self.data = self.stream.read(1024)
                self.frames.append(self.data)
                if(time.time() > self.t + delay):
                    print("END")
                    break
        except KeyboardInterrupt:
            pass
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.file = wave.open("record.wav", "wb")
        self.file.setnchannels(2)
        self.file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        self.file.setframerate(44100)
        self.file.writeframes(b''.join(self.frames))
        self.file.close()

    def getText(self):
        self.filename = "record.wav" #"test.wav"

        # initialize the recognizer
        self.r = sr.Recognizer()
    
        # open the file
        with sr.AudioFile(self.filename) as source:
            # listen for the data (load audio to memory)
            self.audio_data = self.r.record(source)
            # recognize (convert from speech to text)
            self.text = self.r.recognize_google(self.audio_data)
        return self.text
if __name__ == '__main__':
    s = sound()
    t = time.time()
    s.record()
    print(time.time() - t)
    t = time.time()
    try:
        print(s.getText())
    except sr.UnknownValueError:
        print("ERROR")
    finally:
        print(time.time() - t)
