import numpy as np

# fast cepstrum and inverted fast cepstrum
fcs  = lambda s: np.fft.ifft(np.log(np.fft.fft(s)))
ifcs = lambda s: np.fft.fft(np.exp(np.fft.ifft(s)))

# magnitude
mcs = lambda s: (np.abs(np.fft.ifft(np.log(np.abs(np.fft.fft(s))**2)))**2)[:len(s)//2]

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
        rf = r[1:nt] + conj(r[-1:nt-1:-1])
        rw = np.hstack((r[0], rf, np.zeros(n-nt)))
    else:
        nt = n//2
        rf = np.hstack((r[1:nt], 0)) + np.conj(r[-1:nt-1:-1])
        rw = np.hstack((r[0], rf, np.zeros(n-nt-1)))
    return rw

def minphase(s, os=True):
    # via https://ccrma.stanford.edu/~jos/fp/Matlab_listing_mps_m.html
    if os:
        s = np.hstack((s, np.zeros(len(s))))
    cepstrum = np.fft.ifft(np.log(clipdb(np.fft.fft(s), -100)))
    signal = np.real(np.fft.ifft(np.exp(np.fft.fft(fold(cepstrum)))))
    if os:
        signal = signal[:len(signal)//2]
    return signal
