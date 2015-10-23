from . import tau

import numpy as np
import sympy as sym

# implements the modified bilinear transform:
# s <- 1/tan(w0/2)*(1 - z^-1)/(1 + z^-1)
# this requires the s-plane coefficients to be frequency-normalized,
# and the center frequency to be passed as a transformation parameter.

def zcgen_py(n, d):
    zcs = np.zeros(d + 1)

    # expanded from the equation in zcgen_sym
    zcs[0] = 1
    for _ in range(n):
        for i in range(d, 0, -1):
            zcs[i] -= zcs[i - 1]
    for _ in range(d - n):
        for i in range(d, 0, -1):
            zcs[i] += zcs[i - 1]
    return zcs

def zcgen_sym(n, d):
    z = sym.symbols('z')
    expr = sym.expand((1 - z**-1)**n*(1 + z**-1)**(d - n))
    coeffs = expr.equals(1) and [1] or expr.as_poly().all_coeffs()
    return coeffs[::-1]

def s2z_two(b, a, fc, srate, gain=1):
    """
    converts s-plane coefficients to z-plane for digital usage.
    hard-coded for 3 coefficients.
    """
    if len(b) == 2:
        b = (b[0], b[1], 0)
    if len(a) == 2:
        a = (a[0], a[1], 0)
    w0 = tau*fc/srate
    cw = np.cos(w0)
    sw = np.sin(w0)
    zb = np.array((
           b[2]*(1 - cw) + b[0]*(1 + cw) + b[1]*sw,
        2*(b[2]*(1 - cw) - b[0]*(1 + cw)),
           b[2]*(1 - cw) + b[0]*(1 + cw) - b[1]*sw,
    ))
    za = np.array((
           a[2]*(1 - cw) + a[0]*(1 + cw) + a[1]*sw,
        2*(a[2]*(1 - cw) - a[0]*(1 + cw)),
           a[2]*(1 - cw) + a[0]*(1 + cw) - a[1]*sw,
    ))
    return zb*gain, za

def s2z1(w0, s, d):
    """
    s: array of s-plane coefficients (num OR den, not both)
    d: degree (array length - 1)
    returns output array of size d + 1
    """
    y = np.zeros(d + 1)
    sw = np.sin(w0)
    cw = np.cos(w0)
    for n in range(d + 1):
        zcs = zcgen(d - n, d)
        trig = sw**n/(cw + 1)**(n - 1)
        for i in range(d + 1):
            y[i] += trig*zcs[i]*s[n]
    return y

def s2z_any(b, a, fc, srate, gain=1, d=-1):
    """
    converts s-plane coefficients to z-plane for digital usage.
    supports any number of coefficients; b or a will be padded accordingly.
    additional padding can be specified with d.
    """
    cs = max(len(b), len(a), d + 1)
    sb = np.zeros(cs)
    sa = np.zeros(cs)
    sb[:len(b)] = b
    sa[:len(a)] = a
    w0 = tau*fc/srate
    zb = s2z1(w0, sb, cs - 1)
    za = s2z1(w0, sa, cs - 1)
    return zb*gain, za

# set our preference. zcgen_py is 1000+ times faster than zcgen_sym
zcgen = zcgen_py

# s2z_any is only ~2.4 times slower than s2z_two and allows for filters of any degree
s2z = s2z_any
