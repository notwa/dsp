from .util import *
from .bq import *
from .data import *
from .butterworth import *
from .sweeps import *
from .smoothfft import *
from .plot import *
from .wav import *
from .planes import *
from .fft import *
from .bs import *
from .cepstrum import *

import numpy as np
from matplotlib.pylab import show

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

def test_filter(ff, A=toA(12), Q=toQ(1), **kwargs):
    test_filter_raw(ff(A, Q), **kwargs)

def neonpink(xs):
    lament("neonpink(): DEPRECATED; use tilter2(xs, 'raw') instead.")
    return tilter2(xs, 'raw')

def c_render(cascade, precision=4096):
    # TODO: deprecate in favor of tilter2
    xs = xsp(precision)
    return xs, tilter2(xs, cascade)

def c_render2(xs, cascade, phase=False):
    """c_render optimized and specifically for first/second-order filters"""
    import numexpr as ne
    j = np.complex(0, 1)
    eq2 = '(b0 + j*b1*ws - b2*ws**2)/(a0 + j*a1*ws - a2*ws**2)'
    eq1 = '(b0 + j*b1*ws)/(a0 + j*a1*ws)'
    if not phase:
        fmt = 'real(log10(abs({})**2)*10 + gain)'
    else:
        fmt = 'arctan2(imag({0}), real({0}))' # gross
    ys = np.zeros(len(xs))
    for f in cascade:
        w0, ba, gain = f
        b, a = ba
        if len(b) == 3 and len(a) == 3:
            eq = fmt.format(eq2)
            b2, b1, b0 = b
            a2, a1, a0 = a
        elif len(b) == 2 and len(a) == 2:
            eq = fmt.format(eq1)
            b1, b0 = b
            a1, a0 = a
        else:
            raise Exception("incompatible cascade; consider using c_render instead")
        ws = xs/w0
        ys += ne.evaluate(eq)
    if phase:
        ys = degrees_clamped(ys)
    return ys

def firize(xs, ys, n=4096, srate=44100, ax=None):
    import scipy.signal as sig
    if ax:
        ax.semilogx(xs, ys, label='desired')
    xf = xs/srate*2
    yg = 10**(ys/20)

    xf = np.hstack((0, xf, 1))
    yg = np.hstack((0, yg, yg[-1]))

    b = sig.firwin2(n, xf, yg, antisymmetric=True)

    if ax:
        _, ys = sig.freqz(b, worN=xs/srate*tau)
        ys = 20*np.log10(np.abs(ys))
        ax.semilogx(xs, ys, label='FIR ({} taps)'.format(n))
        ax.legend(loc=8)

    return b

def tilter(xs, ys, tilt):
    """tilts a magnitude plot by some decibels, or by equalizer curve."""
    lament("tilter(): DEPRECATED; use ys -= tilter2(xs, tilt) instead.")
    return xs, ys - tilter2(xs, tilt)

def tilter2(xs, tilt): # TODO: rename
    noise = np.zeros(xs.shape)
    if isinstance(tilt, str) and tilt in cascades:
        tilt = cascades[tilt]
    if isinstance(tilt, list):
        c = [makemag(*f) for f in tilt]
        for f in c:
            noise += f(xs)
    elif isinstance(tilt, int) or isinstance(tilt, float):
        noise = tilt*(np.log2(1000) - np.log2(xs + 1e-35))
    return noise

from .plotwav import *

# this is similar to default behaviour of having no __all__ variable at all,
# but ours ignores modules as well. this allows for `import sys` and such
# without clobbering `from our_module import *`.
__all__ = [o for o in locals() if type(o) != 'module' and not o.startswith('_')]
