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

ceil2 = lambda x: np.power(2, np.ceil(np.log2(x)))
pad2 = lambda x: np.r_[x, np.zeros(ceil2(len(x)) - len(x))]

rfft = lambda src, size: np.fft.rfft(src, size*2)
magnitude = lambda src, size: 10*np.log10(np.abs(rfft(src, size))**2)[0:size]
# x axis for plotting above magnitude
magnitude_x = lambda srate, size: np.arange(0, srate/2, srate/2/size)

degrees_clamped = lambda x: ((x*180/np.pi + 180) % 360) - 180

def xsp(precision=4096):
    """create #precision log-spaced points from 20 Hz (inclusive) to 20480 Hz (exclusive)"""
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

def convolve_each(s, fir, mode='same', axis=0):
    return np.apply_along_axis(lambda s: sig.fftconvolve(s, fir, mode), axis, s)

def count_channels(s):
    if s.ndim < 2:
        return 1
    return s.shape[1]

def monoize(s):
    """mixes an n-channel signal down to one channel.
    technically, it averages a 2D array to be 1D.
    existing mono signals are passed through unmodified."""
    channels = count_channels(s)
    if channels != 1:
        s = np.average(s, axis=1)
    return s

def div0(a, b):
    """division, whereby division by zero equals zero"""
    # http://stackoverflow.com/a/35696047
    a = np.asanyarray(a)
    b = np.asanyarray(b)
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide(a, b)
        c[~np.isfinite(c)] = 0 # -inf inf NaN
    return c
