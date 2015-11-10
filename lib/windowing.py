import numpy as np

def _deco_win(f):
    # gives scipy compatibility
    def deco(N, *args, sym=True, **kwargs):
        if N < 1:
            return np.array([])
        if N == 1:
            return np.ones(1)
        odd = N % 2
        if not sym and not odd:
            N = N + 1

        w = f(N, *args, **kwargs)

        if not sym and not odd:
            return w[:-1]
        return w
    return deco

def _gen_hamming(*a):
    L = len(a)
    a += (0, 0, 0, 0, 0) # pad so orders definition doesn't error
    orders = [
        lambda fac: 0,
        lambda fac: a[0],
        lambda fac: a[0] - a[1]*np.cos(fac),
        lambda fac: a[0] - a[1]*np.cos(fac) + a[2]*np.cos(2*fac),
        lambda fac: a[0] - a[1]*np.cos(fac) + a[2]*np.cos(2*fac) - a[3]*np.cos(3*fac),
        lambda fac: a[0] - a[1]*np.cos(fac) + a[2]*np.cos(2*fac) - a[3]*np.cos(3*fac) + a[4]*np.cos(4*fac),
    ]
    f = orders[L]
    return lambda N: f(np.arange(0, N)*2*np.pi/(N - 1))

def _normalize(*args):
    a = np.asfarray(args)
    return a/np.sum(a)

_h = lambda *args: _deco_win(_gen_hamming(*args))
blackman_inexact = _h(0.42, 0.5, 0.08)
blackman = _h(0.42659, 0.49656, 0.076849)
blackman_nuttall = _h(0.3635819, 0.4891775, 0.1365995, 0.0106411)
blackman_harris = _h(0.35875, 0.48829, 0.14128, 0.01168)
nuttall = _h(0.355768, 0.487396, 0.144232, 0.012604)
flattop        = _h(*_normalize(1, 1.93, 1.29, 0.388, 0.028)) # FTSRS
#flattop_weird = _h(_normalize(1, 1.93, 1.29, 0.388, 0.032)) # ??? wtf
flattop_weird = _h(0.2156, 0.4160, 0.2781, 0.0836, 0.0069) # ??? scipy crap
hann = _h(0.5, 0.5)
hamming_inexact = _h(0.54, 0.46)
hamming = _h(0.53836, 0.46164)

@_deco_win
def triangular(N):
    if N % 2 == 0:
        return 1 - np.abs((2*np.arange(N) + 1)/N - 1)
    else:
        return 1 - np.abs(2*(np.arange(N) + 1)/(N + 1) - 1)

@_deco_win
def parzen(N):
    odd = N % 2
    n = np.arange(N/2)
    if not odd:
        n += 0.5
    center = 1 - 6*(2*n/N)**2*(1 - 2*n/N)
    outer = 2*(1 - 2*n/N)**3
    center = center[:len(center)//2]
    outer = outer[len(outer)//2:]
    if not odd:
        return np.r_[outer[::-1], center[::-1], center, outer]
    else:
        return np.r_[outer[::-1], center[::-1], center[1:], outer]

@_deco_win
def cosine(N):
    return np.sin(np.pi*(np.arange(N) + 0.5)/N)

@_deco_win
def welch(N):
    return 1 - (2*np.arange(N)/(N - 1) - 1)**2

# TODO: rename or something
@_deco_win
def sinc(N):
    return np.sinc((np.arange(N) - (N - 1)/2)/2)

winmod = lambda f: lambda N: f(N + 2)[1:-1]
