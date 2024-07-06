import pyaudio
import wave
import threading


class Recorder:
    def __init__(self, filename, rate=16000, chunk=1024, channels=1, format=pyaudio.paInt16):
        self.filename = filename
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.format = format

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
        self.paused = threading.Event()

    def start_recording(self):
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
        self.frames = []
        self.recording = True
        self.paused.clear()
        print("Start recording...")

        threading.Thread(target=self._record).start()

    def _record(self):
        while self.recording:
            if self.paused.is_set():
                continue

            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def pause_recording(self):
        if not self.paused.is_set():
            print("Recording pause...")
            self.paused.set()

    def resume_recording(self):
        if self.paused.is_set():
            print("Recording resume...")
            self.paused.clear()

    def stop_recording(self):
        self.recording = False
        self.paused.set()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Record over.")

        
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

def record_main(filename):
     
    recorder = Recorder(filename)

    
    recorder.start_recording()

    while True:
        command = input("Input and press enter.\n 'p' to pause, 'r' to resume, 's' to stop:").strip().lower()

        if command == "p":
            recorder.pause_recording()
        elif command == "r":
            recorder.resume_recording()
        elif command == "s":
            recorder.stop_recording()
            break
    
    
if __name__ == "__main__":
    record_main("record.wav")
