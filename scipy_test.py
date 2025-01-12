import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import numpy as np

# Number of sample points
n = 1500
# Sample spacing
# t = 1.0 / 2000.0
max_x = 30

f1 = lambda x: np.sin(2*np.pi*2.62*x)
f2 = lambda x: np.sin(2*np.pi*3.30*x)
f3 = lambda x: np.sin(2*np.pi*10*x)

x = np.linspace(0, max_x, n)
y = f1(x) + f2(x) + f3(x)

plt.plot(x, y)
plt.grid()
plt.show()

xf = fftfreq(n, max_x/n)[:n//2]
yf = fft(y)

plt.plot(xf, 2/n*np.abs(yf[0:n//2]))
plt.grid()
plt.show()

'''
f1 = 5
f2 = 8

x = np.linspace(0, n*t, n, endpoint=False)
y = np.sin(f1*2*np.pi*x) + 0.5*np.sin(f2*2*np.pi*x)

plt.plot(x, y)
plt.grid()
plt.show()

yf = fft(y)
xf = fftfreq(n, t)[:n//2]

plt.plot(xf, 2/n*np.abs(yf[0:n//2]))
plt.grid()
plt.show()
'''
