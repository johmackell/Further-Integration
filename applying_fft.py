from matplotlib import pyplot as plt
from scipy.fft import rfft, rfftfreq, irfft
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

# Filtering the Signal
# Looking at the frequency domain graph, we can remove the high-pitched noise 

points_per_freq = len(xf) / (SAMPLE_RATE / 2)
target_idx = int(points_per_freq * 4000)

yf[target_idx - 1 : target_idx + 2] = 0

plt.plot(xf, np.abs(yf))
plt.show()



# Applying the Inverse Fast Fourier Transform (IFFT)

new_sig = irfft(yf)

plt.plot(new_sig[:1000])
plt.show()

norm_new_sig = np.int16(new_sig/new_sig.max() * 32767)
write("clean.wav", SAMPLE_RATE, norm_new_sig)

