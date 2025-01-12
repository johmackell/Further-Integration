from matplotlib import pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 44100 # Hertz
DURATION = 5 # Seconds

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate*duration, endpoint=False)
    frequencies = x*freq
    y = np.sin(2*np.pi*frequencies)
    return x, y

# Create a signal at 400 Hz with distortion 4000 Hz

_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)
noise_tone = noise_tone * 0.3
mixed_tone = nice_tone + noise_tone

normalised_tone = np.int16(mixed_tone/mixed_tone.max() * 32767)

plt.plot(normalised_tone[:1000])
plt.show()

#write("mysinewave.wav", SAMPLE_RATE, normalised_tone)


# Using the Fast Fourier Transform (FFT)
# Now, we use the FFT to remove the noise from the signal

# Number of samples in normalized_tone
n = SAMPLE_RATE * DURATION

yf = rfft(normalised_tone)
xf = rfftfreq(n, 1/SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()

