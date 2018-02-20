from . import xsp, lament
import numpy as np


def smoothfft(xs, ys, bw=1, precision=512):
    """performs log-lin smoothing on magnitude data,
    generally from the output of averfft."""
    lament("smoothfft(): DEPRECATED; use smoothfft2 instead.")
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
    # this is probably implementable with FFTs now that i think about it
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


def smoothfft3(ys, bw=1, precision=512):
    """performs log-lin smoothing on magnitude data"""
    size = len(ys)
    xs = np.arange(0, 1, 1/size)

    xs2 = np.logspace(-np.log2(size), 0, precision, base=2)
    ys2 = np.zeros(precision)
    comp = np.zeros(precision)

    log2_xs2 = np.log2(xs2)
    for i, x in enumerate(xs):
        dist = np.abs(log2_xs2 - np.log2(x + 1e-35)) / bw
        window = np.exp(-dist**2 * 4)  # gaussian (untruncated)
        comp += window
        ys2 += ys[i] * window

    return xs2, ys2 / comp
