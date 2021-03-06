# this is a bunch of crap that should really be reduced to one or two functions

from . import wav_read, wav_write
from . import normalize, averfft, tilter2, smoothfft4, firize
from . import new_response, magnitude_x, convolve_each, monoize, count_channels

import numpy as np


def plotfftsmooth(s, srate, ax=None, bw=1, tilt=None, size=8192,
                  window=0, raw=False, **kwargs):
    sm = monoize(s)

    xs_raw = magnitude_x(srate, size)
    ys_raw = averfft(sm, size=size, mode=window)
    ys_raw -= tilter2(xs_raw, tilt)
    xs, ys = smoothfft4(ys_raw, bw)

    if ax:
        if raw:
            ax.semilogx(xs_raw, ys_raw, **kwargs)
        ax.semilogx(xs, ys, **kwargs)

    return xs, ys


def plotwavinternal(sm, ss, srate, bw=1, size=8192):
    xs_raw = magnitude_x(srate, size)
    ys_raw_m = averfft(sm, size=size)
    ys_raw_s = averfft(ss, size=size)

    # tilting beforehand is negligible besides lowest frequencies, but eh
    ys_raw_m -= tilter2(xs_raw, 'np2')
    ys_raw_s -= tilter2(xs_raw, 'np2s')

    if bw <= 0:
        return xs_raw, xs_raw_m, xs_raw_s

    xs, ys_m = smoothfft4(ys_raw_m, bw=bw, srate=srate)
    xs, ys_s = smoothfft4(ys_raw_s, bw=bw, srate=srate)

    return xs, ys_m, ys_s


def plotwav2(fn, bw=1, size=8192, fix=False, **kwargs):
    s, srate = wav_read(fn)

    s, rms = normalize(s, srate)
    sm = monoize(s)
    if s.ndim > 1 and s.shape[1] == 2:
        ss = monoize(s*np.array((1, -1)))
    else:
        ss = np.zeros(len(s))

    xs, ys_m, ys_s = plotwavinternal(sm, ss, srate, bw, size)

    side_gain = np.average(ys_s) - np.average(ys_m)

    if fix:
        fno = fn[:-4]+"-proc.wav"

        fir_m = firize(xs, -ys_m, srate=srate)
        fir_s = firize(xs, -ys_s, srate=srate)
        smf = convolve_each(sm/8, fir_m, mode='same')
        ssf = convolve_each(ss/8, fir_s, mode='same')
        ssf *= 10**(side_gain/20)
        sf = np.c_[smf + ssf, smf - ssf]

        wav_write(fno, sf, srate, dtype='f')
        print('wrote '+fno)

    return xs, ys_m, ys_s


def pw2(fn, label=None, bw=1/6, **kwargs):
    fno = fn[:-4]+"-proc.wav"
    xs, ys_m, ys_s = plotwav2(fn,  fix=True,  bw=bw, **kwargs)
    xs, ys_m, ys_s = plotwav2(fno, fix=False, bw=bw, **kwargs)

    fig, ax = new_response(-18, 18)
    ax.set_title(
        'averaged magnitudes of normalized songs with tilt and smoothing')
    label = label or fn
    ax.semilogx(xs, ys_m + 0, label=label+' (mid)')
    ax.semilogx(xs, ys_s + 9, label=label+' (side)')
    ax.legend(loc=8)
    return fig, ax
