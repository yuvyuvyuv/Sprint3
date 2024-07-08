import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
# Parameters
Fs = 44000  # Sampling frequency (Hz)
T = 1       # Duration of signal (seconds)
t = np.linspace(0, T, int(T * Fs), endpoint=False)  # Time vector
f0 = 1000   # Frequency for binary 0 (Hz)
f1 = 2000   # Frequency for binary 1 (Hz)
A = 1       # Amplitude of the signal

# Binary sequence (example)
binary_data = np.random.randint(0, 2, int(T * Fs))
print(binary_data)
def data_to_signal(binary_data):
    # BFSK modulation
    modulated_signal = np.zeros(len(t))
    for i, bit in enumerate(binary_data): 
        if bit == 0:
            modulated_signal[i] = A * np.sin(2 * np.pi * f0 * t[i])
        else:
            modulated_signal[i] = A * np.sin(2 * np.pi * f1 * t[i])
    return modulated_signal

def signal_to_data(signal):
    # BFSK demodulation
    demodulated_signal = np.zeros(len(t))
    threshold = A / 2  # Decision threshold (half of the maximum amplitude)

    for i in range(len(t)):
        if signal[i] > threshold:
            demodulated_signal[i] = 1  # Detected binary 1
        else:
            demodulated_signal[i] = 0  # Detected binary 0

    return demodulated_signal



sd.play(data_to_signal(binary_data), Fs)

# Wait until the audio is done playing
sd.wait()