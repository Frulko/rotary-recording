import math
import numpy as np

class DTMFDetector:
    def __init__(self):
        self.sample_counter = 0
        self.current_samples = b""
        self.sample_count = 0.02 / 0.000125  # 20ms à 8000 Hz
        self.dtmf_frequencies = {
            '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
            '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
            '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
            '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
        }
        self.last_detected_tone = None

    def add_sample_and_detect_dtmf(self, chunk):
        self.current_samples += chunk
        self.sample_counter += len(chunk)

        print('hello')

        if self.sample_counter >= self.sample_count:
            dtmf_tone = self._detect_dtmf()
            self.current_samples = self.current_samples[len(chunk):]
            self.sample_counter -= len(chunk)
            return dtmf_tone

        return None

    def _detect_dtmf(self):
        samples = np.frombuffer(self.current_samples, dtype=np.uint8)
        samples = np.array([mu_law_linear_to_sample(s) for s in samples])

        fft = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(samples), 1/8000)

        detected_tone = None
        max_magnitude = 0

        for tone, (f1, f2) in self.dtmf_frequencies.items():
            magnitude1 = np.abs(fft[np.argmin(np.abs(freqs - f1))])
            magnitude2 = np.abs(fft[np.argmin(np.abs(freqs - f2))])
            
            if magnitude1 > max_magnitude and magnitude2 > max_magnitude:
                max_magnitude = min(magnitude1, magnitude2)
                detected_tone = tone

        if detected_tone and detected_tone != self.last_detected_tone:
            self.last_detected_tone = detected_tone
            return detected_tone

        return None

# Le reste du code (mu_law_linear_to_sample, etc.) reste inchangé