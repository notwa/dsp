from . import xsp
import numpy as np

def smoothfft(xs, ys, bw=1, precision=512):
    """performs log-lin smoothing on magnitude data,
    generally from the output of averfft."""
    # TODO: option to extrapolate (pad) fft data
    xs2 = xsp(precision)
    ys2 = np.zeros(precision)
    log_xs = np.log(xs)
    for i, x in enumerate(xs2):
        dist = np.exp(np.abs(log_xs - np.log(x + 1e-35)))
        window = np.maximum(0, 1 - (dist - bw))
        # at this point you could probably
        # normalize our *triangular* window to 0-1
        # and transform it into *another* windowing function
        wsum = np.sum(window)
        ys2[i] = np.sum(ys*window/wsum)
    return xs2, ys2

def smoothfft2(xs, ys, bw=1, precision=512, compensate=True):
    """performs log-lin smoothing on magnitude data,
    generally from the output of averfft."""
    xs2 = xsp(precision)
    ys2 = np.zeros(precision)
    log2_xs2 = np.log2(xs2)
    for i, x in enumerate(xs):
        #dist = np.abs(np.log2(xs2/(x + 1e-35)))/bw
        dist = np.abs(log2_xs2 - np.log2(x + 1e-35))/bw
        #window = np.maximum(0, 1 - dist) # triangle window
        window = np.exp(-dist**2/(0.5/2)) # gaussian function (non-truncated)
        ys2 += ys[i]*window
    if compensate:
        _, temp = smoothfft2(xs, np.ones(len(xs)), bw=bw, precision=precision, compensate=False)
        ys2 /= temp
    return xs2, ys2

def smoothfft3(xs, ys, bw=1, precision=1024):
    # actually this will never work...
    # you need to go back to smoothfft2,
    # which technically works as-designed,
    # and fix the compensation to work with widely-spaced data.
    raise Exception("smoothfft3 is broken.")
    xs2 = xsp(precision)
    ys2 = np.zeros(precision)
    step = (xs[1] - xs[0])
    if True:
        for i, x in enumerate(xs):
            dist = np.abs(xs2 - x)
            bw2 = x*bw/2
            window = np.maximum(0, 1 - dist/bw2)
            #window = np.minimum(1, np.maximum(0, 1 - (dist - bw)))
            ys2 += ys[i]*window
    else:
        for i, x2 in enumerate(xs2):
            dist = np.abs(xs - x2)
            window = np.maximum(0, 1 - (dist/step/bw))
            wsum = np.sum(window)
            ys2[i] = np.sum(ys*window/wsum)
    return xs2, ys2
