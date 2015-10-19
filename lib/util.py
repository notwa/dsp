import sys
import numpy as np
import scipy.signal as sig

dummy = lambda *args, **kwargs: None
lament = lambda *args, **kwargs: print(*args, file=sys.stderr, **kwargs)

toLK = lambda x: -0.691 + 10*np.log10(x)
isqrt2 = 1/np.sqrt(2)
toQ = lambda bw: isqrt2/bw
toA = lambda db: 10**(db/40)

tau = 2*np.pi
unwarp = lambda w: np.tan(w/2)
warp = lambda w: np.arctan(w)*2

rfft = lambda src, size: np.fft.rfft(src, size*2)
magnitude = lambda src, size: 10*np.log10(np.abs(rfft(src, size))**2)[0:size]

def xsp(precision=4096):
    """create #precision log-spaced points from 20 to 20480 Hz"""
    # i opt not to use steps or linspace here,
    # as the current method is less error-prone for me.
    xs = np.arange(0,precision)/precision
    return 20*1024**xs

def blocks(a, step, size=None):
    """break an iterable into chunks"""
    if size is None:
        size = step
    for start in range(0, len(a), step):
        end = start + size
        if end > len(a):
            break
        yield a[start:end]

def convolve_each(s, fir, mode=None, axis=0):
    return np.apply_along_axis(lambda s: sig.fftconvolve(s, fir, mode), axis, s)

def count_channels(s):
    if len(s.shape) < 2:
        return 1
    return s.shape[1]

def monoize(s):
    """mixes an n-channel signal down to one channel.
    technically, it averages a 2D array to be 1D.
    existing mono signals are passed through unmodified."""
    channels = count_channels(s)
    if channels != 1:
        s = np.sum(s, 1)
        s /= channels
    return s
