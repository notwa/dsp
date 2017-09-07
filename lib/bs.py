from . import blocks, convolve_each, gen_filters, cascades, bq_run, toLK

import numpy as np
import matplotlib.pyplot as plt

def BS1770_3(s, srate, filters=None, window=0.4, overlap=0.75,
             gate=10, absolute_gate=70, detail=False):
    if filters is None:
        filters = gen_filters(cascades['1770'], srate)

    sf = np.copy(s)
    for f in filters:
        if len(f) is 2: # dumb but effective
            sf = bq_run(f, sf)
        else:
            sf = convolve_each(sf, f, 'same')

    stepsize = round(window*srate*(1 - overlap))
    blocksize = int(stepsize/(1 - overlap))

    means = np.array([
        np.sum(np.mean(b**2, axis=0)) for b in blocks(sf, stepsize, blocksize)
    ])
    LKs = toLK(means)

    gated = LKs > -absolute_gate
    means_g70 = means[gated]
    avg_g70 = np.average(means_g70)
    threshold = toLK(avg_g70) - gate
    means_g10 = means[gated | (LKs > threshold)]
    avg_g10 = np.average(means_g10)

    if detail is False:
        return toLK(avg_g10)
    else:
        return toLK(avg_g10), toLK(avg_g70), LKs, threshold

def BS_plot(ys, g10=None, g70=None, threshold=None, fig=None, ax=None):
    if g10:
        center = np.round(g10)
        bins = np.arange(center - 10, center + 10.01, 0.25)
    else:
        bins = np.arange(-70, 0.1, 1)

    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.gca()

    if False: # histogram
        ax.hist(ys, bins=bins, normed=True, facecolor='g', alpha=0.5)
        ax.xlim(bins[0], bins[-1])
        ax.ylim(0, 1)
        ax.grid(True, 'both')
        ax.xlabel('loudness (LKFS)')
        ax.ylabel('probability')
        fig.set_size_inches(10,4)

    xs = np.arange(len(ys))
    #ax.plot(xs, ys, color='#066ACF', linestyle=':', marker='d', markersize=2)
    ax.plot(xs, ys, color='#1459E0')
    ax.set_xlim(xs[0], xs[-1])
    ax.set_ylim(-70, 0)
    ax.grid(True, 'both', 'y')
    ax.set_xlabel('bin')
    ax.set_ylabel('loudness (LKFS)')
    fig.set_size_inches(12,5)
    #_, _, ymin, _ = ax.axis()
    if threshold:
        ax.axhspan(-70, threshold, facecolor='r', alpha=1/5)
    if g10:
        ax.axhline(g10, color='g')
    if g70:
        ax.axhline(g70, color='0.3')

    return fig, ax

def normalize(s, srate):
    """performs BS.1770-3 normalization and returns inverted gain."""
    db = BS1770_3(s, srate)
    rms = 10**(db/20)
    return s/rms, rms
