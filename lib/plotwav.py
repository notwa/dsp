# this is a bunch of crap that should really be reduced to one or two functions

from . import wav_read, normalize, averfft, tilter2, smoothfft2, firize
from . import new_response, show, convolve_each, monoize, count_channels

import numpy as np

def plotwavsmooth(fn, ax, tilt=None, bw=1, size=8192, raw=False, fix=False, smoother=smoothfft2, **kwargs):
    s, srate = wav_read(fn)

    s, rms = normalize(s, srate)
    sm = monoize(s)
    ss = monoize(s*np.array((1, -1)))

    xs_raw = np.arange(0, srate/2, srate/2/size)
    ys_raw = averfft(sm, size=size)

    # tilting beforehand is negligible besides lowest frequencies, but eh
    if tilt is not None:
        ys_raw -= tilter2(xs_raw, tilt)

    xs, ys = smoother(xs_raw, ys_raw, bw=bw)

    if not 'label' in kwargs:
        kwargs['label'] = fn

    if raw:
        ax.semilogx(xs_raw, ys_raw, **kwargs)
    ax.semilogx(xs, ys, **kwargs)

    if not fix: return

    fno = fn[:-4]+"-proc.wav"
    fir = firize(xs, -ys, srate=srate)
    sf = convolve_each(s/8, fir, mode='same')

    import ewave
    with ewave.open(fno, 'w', sampling_rate=srate, nchannels=count_channels(sf)) as f:
        f.write(sf)
    print('wrote '+fno)

def plotfftsmooth(s, srate, ax, bw=1, tilt=None, size=8192, window=0, raw=False, **kwargs):
    sm = monoize(s)

    xs_raw = np.arange(0, srate/2, srate/2/size)
    ys_raw = averfft(sm, size=size, mode=window)

    ys_raw -= tilter2(xs_raw, tilt)

    xs, ys = smoothfft(xs_raw, ys_raw, bw=bw)

    if raw: ax.semilogx(xs_raw, ys_raw, **kwargs)
    ax.semilogx(xs, ys, **kwargs)

    return xs, ys

def plotwav2(fn, ax, bw=1, size=8192, raw=False, fix=False,
             smoother=smoothfft2, side_compensate=9, **kwargs):
    s, srate = wav_read(fn)

    s, rms = normalize(s, srate)
    sm = monoize(s)
    ss = monoize(s*np.array((1, -1)))

    xs_raw = np.arange(0, srate/2, srate/2/size)
    ys_raw = averfft(sm, size=size)
    ys_raw_side = averfft(ss, size=size)

    # tilting beforehand is negligible besides lowest frequencies, but eh
    ys_raw -= tilter2(xs_raw, 'np2')
    ys_raw_side -= tilter2(xs_raw, 'np2s')

    xs, ys = smoother(xs_raw, ys_raw, bw=bw)
    xs, ys_side = smoother(xs_raw, ys_raw_side, bw=bw)

    if not 'label' in kwargs:
        kwargs['label'] = fn

    if raw:
        ax.semilogx(xs_raw, ys_raw, **kwargs)
        ax.semilogx(xs_raw, ys_raw_side + side_compensate, **kwargs)
    ax.semilogx(xs, ys, **kwargs)
    ax.semilogx(xs, ys_side + side_compensate, **kwargs)

    side_gain = np.average(ys_raw_side) - np.average(ys_raw)
    print("side gain:", side_gain)

    if not fix: return
    fno = fn[:-4]+"-proc.wav"

    fir = firize(xs, -ys, srate=srate)
    smf = convolve_each(sm/8, fir, mode='same')
    fir = firize(xs, -ys_side, srate=srate)
    ssf = convolve_each(ss/8, fir, mode='same')
    ssf *= 10**(side_gain/20)
    sf = np.array((smf + ssf, smf - ssf)).T

    import ewave
    with ewave.open(fno, 'w', sampling_rate=srate, nchannels=count_channels(sf)) as f:
        f.write(sf)
    print('wrote '+fno)

def pw(fn, ax, **kwargs):
    plotwavsmooth(fn, ax, tilt='np2', bw=1/6, **kwargs)

def pwc(fn, **kwargs):
    fig, ax = new_response(-18, 18)
    ax.set_title('averaged magnitudes of normalized songs with tilt and smoothing')

    pw(fn, ax, fix=True, **kwargs)
    fno = fn[:-4]+"-proc.wav"
    pw(fno, ax, fix=False, **kwargs)

    ax.legend(loc=8)
    show(fig)

def pw2(fn, **kwargs):
    fig, ax = new_response(-18, 18)
    ax.set_title('averaged magnitudes of normalized songs with tilt and smoothing')

    plotwav2(fn, ax, fix=True, bw=1/6, **kwargs)
    fno = fn[:-4]+"-proc.wav"
    plotwav2(fno, ax, fix=False, bw=1/6, **kwargs)

    ax.legend(loc=8)
    show(fig)
