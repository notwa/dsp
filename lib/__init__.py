import numpy as np
#from IPython.display import display
from matplotlib.pylab import show

from .util import *
from .data import *
gen_filters = lambda cascade, srate: [
    s2z(*f[1], fc=f[0], srate=srate, gain=10**(f[2]/20)) for f in cascade
]
from .bq import *
from .butterworth import *
from .sweeps import *
from .smoothfft import *
from .plot import *
from .wav import *
from .planes import *
from .fft import *
from .bs import *

def analog(b, a):
    import sympy as sym
    w,s = sym.symbols('w s')
    filt_expr = sym.Poly(b, s)/sym.Poly(a, s)
    mag_expr = abs(filt_expr.subs({s: w*sym.I}))**2
    return sym.lambdify(w, mag_expr, 'numpy')

def makemag(w0, ba, gain=0):
    f = analog(*ba)
    def magf(w):
        a = f(w/w0)
        a[0] = 1e-35
        a = np.log10(a)*10 + gain
        a[0] = a[1] # safety measure
        return a
    return magf

def test_filter_raw(ba, fc=1000, gain=0, precision=4096):
    fig, ax = new_response(ymin=-24, ymax=24)
    xs = xsp(precision)
    ax.semilogx(xs, makemag(fc, ba, gain)(xs))
    show(fig)

def test_filter(ff, A=toA(12), Q=toQ(1), **kwargs):
    test_filter_raw(ff(A, Q), **kwargs)

npc = [makemag(*f) for f in cascades['raw']]
def neonpink(xs):
    print("neonpink(): DEPRECATED")
    combined = np.zeros(len(xs))
    for f in npc:
        combined += f(xs)
    return combined

def c_render(cascade, precision=4096):
    xs = xsp(precision)
    ys = np.zeros_like(xs)
    c = [makemag(*f) for f in cascade]
    for f in c:
        ys += f(xs)
    return xs, ys

def firize(xs, ys, n=4096, srate=44100, plot=None):
    import scipy.signal as sig
    if plot:
        plot.semilogx(xs, ys, label='desired')
    xf = xs/srate*2
    yg = 10**(ys/20)

    xf = np.hstack((0, xf, 1))
    yg = np.hstack((0, yg, yg[-1]))

    b = sig.firwin2(n, xf, yg, antisymmetric=True)

    if plot:
        _, ys = sig.freqz(b, worN=xs/srate*tau)
        ys = 20*np.log10(np.abs(ys))
        plot.semilogx(xs, ys, label='FIR ({} taps)'.format(n))
        plot.legend(loc=8)

    return b

def normalize_test(s, srate):
    # FIXME: where is fir3 defined?
    #rms_naive = np.sqrt(np.mean(s**2))
    filters3 = gen_filters(cascades['raw3'], srate)
    db_standard = BS1770_3(s, srate)
    db = BS1770_3(s, srate, filters=filters3)
    print('raw3 would be\t{:+6.2f} dB louder/quieter than RG2'.format(db_standard - db))
    db = BS1770_3(s, srate, filters=[fir3])
    print('fir3 would be\t{:+6.2f} dB louder/quieter than RG2'.format(db_standard - db))
    rms = 10**(db/20)
    return s/rms, rms

def tilter(xs, ys, tilt):
    """tilts a magnitude plot by some decibels, or by equalizer curve."""
    # should really just do this instead:
    # ys -= tilt(xs, 3)
    print("tilter(): DEPRECATED")
    if tilt == 'neon':
        noise = neonpink(xs)
    elif type(tilt) is str:
        noise = np.zeros(len(xs))
        c = [makemag(*f) for f in cascades[tilt]]
        for f in c:
            noise += f(xs)
    elif isinstance(tilt, int) or isinstance(tilt, float):
        noise = tilt*(np.log2(1000) - np.log2(xs))
    else:
        noise = np.zeros(xs.shape)
    return xs, ys - noise

def tilter2(xs, tilt):
    if type(tilt) is str:
        noise = np.zeros(len(xs))
        c = [makemag(*f) for f in cascades[tilt]]
        for f in c:
            noise += f(xs)
    elif isinstance(tilt, int) or isinstance(tilt, float):
        noise = tilt*(np.log2(1000) - np.log2(xs + 1e-35))
    else:
        noise = np.zeros(xs.shape)
    return noise

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

# this is similar to default behaviour of having no __all__ variable at all,
# but ours ignores modules as well. this allows for `import sys` and such
# without clobbering `from our_module import *`.
__all__ = [o for o in locals() if type(o) != 'module' and not o.startswith('_')]
