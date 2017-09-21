import numpy as np
import scipy.signal as sig

from .util import *
from .planes import s2z


# PEP 8 fucking destroyed this file. I'm sorry.


def bq_run(bq, xs):
    return sig.lfilter(*bq, x=xs, axis=0)


def nfba(b, a):
    return (1/tau, (b, a), 0)


def nf(t, f, g, bw, mg):
    return (f, t(toA(g), toQ(bw)), mg)


def LP1(A, Q):
    return ((0, 1), (1, 1))


def HP1(A, Q):
    return ((1, 0), (1, 1))


def LS1(A, Q):
    return ((1, A), (1, 1/A))


def HS1(A, Q):
    return ((A, 1), (1/A, 1))


# patterns observed, in case some simplification could be done:
# a always gets divided by A instead of multiplied
# b1 and a1 always /= Q

def LP2(A, Q):
    return ((0, 0, 1), (1, 1/Q, 1))


def HP2(A, Q):
    return ((1, 0, 0), (1, 1/Q, 1))


def PE2(A, Q):
    return ((1, A/Q, 1), (1, 1/A/Q, 1))


def AP2(A, Q):
    return ((1, -1/Q, 1), (1, 1/Q, 1))


def BP2a(A, Q):
    return ((0, -A/Q, 0), (1, 1/A/Q, 1))


def BP2b(A, Q):
    return ((0, -A*A/Q, 0), (1, 1/Q, 1))


def NO2(A, Q):
    return ((1, 0, 1), (1, 1/Q, 1))


def LS2(A, Q):
    return ((1, np.sqrt(A)/Q, A), (1, 1/np.sqrt(A)/Q, 1/A))


def HS2(A, Q):
    return ((A, np.sqrt(A)/Q, 1), (1/A, 1/np.sqrt(A)/Q, 1))


def gen_filters(cascade, srate):
    return [
        s2z(*f[1], fc=f[0], srate=srate, gain=10**(f[2]/20)) for f in cascade
    ]
