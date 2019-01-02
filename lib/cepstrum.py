import numpy as np
from .util import pad2


def fcs(s):  # fast cepstrum
    return np.fft.ifft(np.log(np.fft.fft(s)))


def ifcs(s):  # inverted fast cepstrum
    return np.fft.fft(np.exp(np.fft.ifft(s)))


def mcs(s):  # magnitude (actually power)
    return (np.abs(np.fft.ifft(np.log(np.abs(np.fft.fft(s))**2)))**2
            )[:len(s)//2]


def clipdb(s, cutoff=-100):
    as_ = np.abs(s)
    mas = np.max(as_)
    if mas == 0 or cutoff >= 0:
        return s
    thresh = mas*10**(cutoff/20)
    return np.where(as_ < thresh, thresh, s)


def fold(r):
    # via https://ccrma.stanford.edu/~jos/fp/Matlab_listing_fold_m.html
    # Fold left wing of vector in "FFT buffer format" onto right wing
    # J.O. Smith, 1982-2002
    n = len(r)
    if n < 3:
        rw = r
    elif n % 2 == 1:
        nt = (n + 1)//2
        rf = r[1:nt] + np.conj(r[-1:nt-1:-1])
        rw = np.r_[r[0], rf, np.zeros(n-nt)]
    else:
        nt = n//2
        rf = np.r_[r[1:nt], 0] + np.conj(r[-1:nt-1:-1])
        rw = np.r_[r[0], rf, np.zeros(n-nt-1)]
    return rw


def minphase(s, pad=True):
    # via https://ccrma.stanford.edu/~jos/fp/Matlab_listing_mps_m.html
    # TODO: oversampling
    if pad:
        s = pad2(s)
    cepstrum = np.fft.ifft(np.log(clipdb(np.fft.fft(s), -100)))
    signal = np.real(np.fft.ifft(np.exp(np.fft.fft(fold(cepstrum)))))
    return signal
