from . import tau, ceil2

import numpy as np


def sweep(amp, length, begin=20, end=20480, method='linear'):
    method = method or 'linear'
    xs = np.arange(length)/length
    if method in ('linear', 'quadratic', 'logarithmic', 'hyperbolic'):
        ys = amp*sig.chirp(xs, begin, 1, end, method=method)
    elif method is 'sinesweep':
        # because xs ranges from 0:1, length is 1 and has been simplified out
        domain = np.log((tau * end)/(tau * begin))
        ys = amp*np.sin((tau * begin)/domain*(np.exp(xs*domain) - 1))
    return ys


def tsp(N, m=0.5):
    """
        OATSP(Optimized Aoshima's Time-Stretched Pulse) generator
        x = tsp( N, m )
        N : length of the time-stretched pulse
        m : ratio of the swept sine  (0 < m < 1)

        Author(s): Seigo UTO 8-23-95

        Reference:
           Yoiti SUZUKI, Futoshi ASANO, Hack-Yoon KIM and Toshio SONE,
           "Considerations on the Design of Time-Stretched Pulses,"
               Techical Report of IEICE, EA92-86(1992-12)
    """
    # http://www.sound.sie.dendai.ac.jp/dsp/e-21.html

    if m < 0 or m > 1:
        raise Exception("what are you doinggg")

    if N < 0:
        raise Exception("The number of length must be the positive number")

    NN = ceil2(N)
    NN2 = NN // 2
    M = int(np.round(NN2 * m))

    # this has been tweaked to prevent overflow:
    s = np.square(np.arange(NN2 + 1) / NN)

    H = np.exp(4j * M * np.pi * s)
    H2 = np.r_[H, np.conj(H[1:NN2][::-1])]

    x = np.fft.ifft(H2)
    x = np.r_[x[NN2 - M:NN + 1], x[0:NN2 - M + 1]]
    x = np.r_[x.real, np.zeros(N - NN)]

    return x
