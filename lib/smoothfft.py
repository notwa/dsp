from . import xsp, lament, ceil2
import numpy as np


def smoothfft(xs, ys, bw=1, precision=512):
    """performs log-lin smoothing on magnitude data,
    generally from the output of averfft."""
    lament("smoothfft(): DEPRECATED; use smoothfft4 instead.")
    xs2 = xsp(precision)
    ys2 = np.zeros(precision)
    log_xs = np.log(xs)
    for i, x in enumerate(xs2):
        dist = np.exp(np.abs(log_xs - np.log(x + 1e-35)))
        window = np.maximum(0, 1 - (dist - bw))
        # at this point we could probably
        # normalize our *triangular* window to 0-1
        # and transform it into *another* windowing function
        wsum = np.sum(window)
        ys2[i] = np.sum(ys*window/wsum)
    return xs2, ys2


def smoothfft2(xs, ys, bw=1, precision=512, compensate=True):
    """performs log-lin smoothing on magnitude data,
    generally from the output of averfft."""
    lament('smoothfft2: DEPRECATED; use smoothfft4 instead.')
    xs2 = xsp(precision)
    ys2 = np.zeros(precision)
    log2_xs2 = np.log2(xs2)
    for i, x in enumerate(xs):
        # before optimizations: dist = np.abs(np.log2(xs2/(x + 1e-35)))/bw
        dist = np.abs(log2_xs2 - np.log2(x + 1e-35))/bw
        # window = np.maximum(0, 1 - dist) # triangular
        window = np.exp(-dist**2/(0.5/2))  # gaussian (untruncated)
        ys2 += ys[i]*window
    if compensate:
        _, temp = smoothfft2(xs, np.ones(len(xs)),
                             bw=bw, precision=precision, compensate=False)
        ys2 /= temp
    return xs2, ys2


def smoothfft_setup(size, precision=512, bw=1/6):
    lament('smoothfft_setup(): DEPRECATED; use smoothfft_setup2 instead.')
    dotme = np.zeros((size, precision))

    xs = np.arange(0, 1, 1/size)
    xs2 = np.logspace(-np.log2(size), 0, precision, base=2)
    comp = np.zeros(precision)

    log2_xs2 = np.log2(xs2)
    for i, x in enumerate(xs):
        dist = np.abs(log2_xs2 - np.log2(x + 1e-35)) / bw
        window = np.exp(-dist**2 * 4)  # gaussian (untruncated)
        comp += window
        dotme[i] = window

    dotme /= comp

    return xs2, dotme


def smoothfft3(ys, bw=1, precision=512, srate=None):
    """performs log-lin smoothing on magnitude data"""
    lament('smoothfft3(): DEPRECATED; use smoothfft4 instead.')
    xs2, dotme = smoothfft_setup(len(ys), precision, bw)
    if srate is None:
        return xs2, ys @ dotme
    else:
        return xs2 * (srate / 2), ys @ dotme


def smoothfft_setup2(size, precision=512, bw=1/6):
    # tweaked/fixed to drop 0 Hz
    size -= size % 2
    assert size == ceil2(size), size

    dotme = np.zeros((size, precision))
    xs = np.arange(1, size + 1) / size
    xs2 = np.logspace(-np.log2(size), 0, precision, base=2)
    comp = np.zeros(precision)

    log2_xs2 = np.log2(xs2)
    for i, x in enumerate(xs):
        dist = np.abs(log2_xs2 - np.log2(x)) / bw
        window = np.exp(-dist**2 * 4)  # gaussian (untruncated)
        comp += window
        dotme[i] = window

    dotme /= comp
    return xs2, dotme


def smoothfft4(ys, bw=1, precision=512, srate=None):
    # tweaked/fixed to drop 0 Hz
    if len(ys) % 2 == 1:
        ys = ys[1:]
    xs2, dotme = smoothfft_setup2(len(ys), precision, bw)
    if srate is None:
        return xs2, ys @ dotme
    else:
        return xs2 * (srate / 2), ys @ dotme
