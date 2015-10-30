from . import tau
import numpy as np

def gen_hamm(a0, a1=0, a2=0, a3=0, a4=0):
    form = lambda x: a0 - a1*np.cos(x) + a2*np.cos(2*x) - a3*np.cos(3*x) + a4*np.cos(4*x)
    dc = form(np.pi)
    def f(N):
        a = tau*np.arange(N)/(N - 1)
        return form(a)/dc
    return f

# TODO: rename or something
sinc = lambda N: np.sinc((np.arange(N) - (N - 1)/2)/2)

triangular = lambda N: 1 - np.abs(2*np.arange(N)/(N - 1) - 1)
welch = lambda N: 1 - (2*np.arange(N)/(N - 1) - 1)**2
cosine = lambda N: np.sin(np.pi*np.arange(N)/(N - 1))

hann = gen_hamm(0.5, 0.5)
hamming = gen_hamm(0.53836, 0.46164)
blackman = gen_hamm(0.42659, 0.49656, 0.076849)
blackman_harris = gen_hamm(0.35875, 0.48829, 0.14128, 0.01168)
blackman_nutall = gen_hamm(0.3635819, 0.4891775, 0.1365995, 0.0106411)
nutall = gen_hamm(0.355768, 0.487396, 0.144232, 0.012604)
# specifically the Stanford Research flat-top window (FTSRS)
flattop = gen_hamm(1, 1.93, 1.29, 0.388, 0.028)

def parzen(N):
    # TODO: verify this is accurate. the code here is kinda sketchy
    n = np.arange(N/2)
    center = 1 - 6*(2*n/N)**2*(1 - 2*n/N)
    outer = 2*(1 - 2*n/N)**3
    center = center[:len(center)//2]
    outer = outer[len(outer)//2:]
    if N % 2 == 0:
        return np.hstack((outer[::-1], center[::-1], center, outer))
    else:
        return np.hstack((outer[::-1], center[::-1], center[1:], outer))

# some windows reach 0 at either side, so this can avoid that
winmod = lambda f: lambda N: f(N + 2)[1:-1]
