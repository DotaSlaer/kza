import os
import ctypes as ct
import numpy as np
import matplotlib.pyplot as plt

libkza_path = os.getcwd() + "/libkza.so"

libkza = ct.CDLL(libkza_path)
libkza.kz.argtypes = [
    ct.POINTER(ct.c_double), 
    ct.c_int, 
    ct.POINTER(ct.c_int), 
    ct.POINTER(ct.c_int), 
    ct.c_int
]
libkza.kz.restype = None

def kz1d(x, m, k = 3):
    xp = (ct.c_double * len(x))(*x)
    dim = 1
    size = (ct.c_int)(len(x))
    window = (ct.c_int)(m)
    libkza.kz(xp, dim, ct.byref(size), ct.byref(window), k)
    return list(xp)

# Example
np.random.seed(1)
yrs = 20
m = 365
t = np.linspace(0, yrs, yrs*m)
e = np.random.normal(loc=0, scale=1.0, size=len(t))
trend = np.linspace(0, -1, len(t))

bkpt = 3452
brk = np.empty(len(t))
brk[:bkpt] = 0
brk[bkpt:] = 0.5

signal = trend + brk

y = np.sin(2*np.pi*t) + signal + e

z = kz1d(y, 20, 3)
print(z[len(z)-10:])

plt.subplot(211)
plt.title("y = sin(2*pi*t) + noise")
plt.plot(t, signal)
plt.ylim([-5, 5])

plt.subplot(212)
plt.title("KZ filter")
plt.plot(t, z)
plt.plot(t, signal)
#plt.plot(t, np.sin(2*np.pi*t))
plt.ylim([-5, 5])
plt.show()
exit(0)

# Example
np.random.seed(1)
t = np.linspace(0, 20, 20*365)
e = np.random.normal(loc=0, scale=2.0, size=len(t))
y = np.sin(3*np.pi*t) + e
z = kz1d(y, 30)

plt.subplot(211)
plt.title("y = sin(3*pi*t) + noise")
plt.plot(t, y)
plt.ylim([-5, 5])

plt.subplot(212)
plt.title("KZ filter")
plt.plot(t, z)
plt.plot(t, np.sin(3*np.pi*t))
plt.ylim([-5, 5])
plt.show()