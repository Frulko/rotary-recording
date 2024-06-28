import wave
from datetime import datetime

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.wav_file = None

    def start_recording(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"call_{timestamp}.wav"
        self.wav_file = wave.open(filename, 'wb')
        self.wav_file.setnchannels(1)
        self.wav_file.setsampwidth(1)  # 8-bit audio
        self.wav_file.setframerate(8000)  # 8kHz sample rate
        self.recording = True

    def write_audio(self, audio_data):
        if self.recording:
            self.wav_file.writeframes(audio_data)

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.wav_file.close()