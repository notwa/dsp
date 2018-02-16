import sys
import numpy as np
import scipy.signal as sig


isqrt2 = 1/np.sqrt(2)
tau = 2*np.pi


def dummy(*args, **kwargs):
    return None


def lament(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


def toLK(x):
    return -0.691 + 10*np.log10(x)


def toQ(bw):
    return isqrt2/bw


def toA(db):
    return 10**(db/40)


def unwarp(w):
    return np.tan(w/2)


def warp(w):
    return np.arctan(w)*2


def ceil2(x):
    return np.power(2, np.ceil(np.log2(x)).astype(int))


def pad2(x):
    return np.r_[x, np.zeros(ceil2(len(x)) - len(x))]


def rfft(src, size):
    return np.fft.rfft(src, size*2)


def magnitude(src, size):
    return 10*np.log10(np.abs(rfft(src, size))**2)[0:size]


# x axis for plotting above magnitude
def magnitude_x(srate, size):
    return np.arange(0, srate/2, srate/2/size)


def degrees_clamped(x):
    return ((x*180/np.pi + 180) % 360) - 180


def xsp(precision=4096):
    """
    create #precision log-spaced points from
    20 Hz (inclusive) to 20480 Hz (exclusive)
    """
    xs = np.arange(0, precision)/precision
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
    return np.apply_along_axis(
        lambda s: sig.fftconvolve(s, fir, mode), axis, s)


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
        c[~np.isfinite(c)] = 0  # -inf inf NaN
    return c
