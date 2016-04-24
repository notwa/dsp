from .util import *
from .bq import *

import numpy as np

# as calculated by LPB in nsf.py
_bq2a = 1/.76536686473017945
_bq2b = 1/1.8477590650225735
_bq2a_bw = isqrt2/_bq2a
_bq2b_bw = isqrt2/_bq2b

cascades = {
    '1770': [
        (1501,      HS2(toA(4), toQ(1)),    0),
        (38.135457, HP2(0, 0.5003268), np.log10(1.004995)*20),
    ],
    # "neon pink"
    'raw': [
        nf(LP1,    20,    0,    1,   29),
        nf(HS1,   800,   12,    1,    0),
        # i don't use the exact _bq2 coeffecients here for legacy reasons
        (   45,   HP2(    0, 1.32), 0.5), # roughly estimates
        (   45,   HP2(    0, 0.54), 0.5), # a 4-pole butterworth highpass
        nf(LP2, 14000,    0, 1.33,    0),
    ],
    # like neon pink but for feeding into RMS
    'raw2': [
        (10000, HP1(0,0),                  26),
        (  750, HS2(toA(-10), toQ(1.33)),   0),
        (   45, HP2(0,             1.32), 0.5),
        (   45, HP2(0,             0.54), 0.5),
        (14000, LP2(0,        toQ(1.33)),   0),
        (  250, PE2(toA(3),   toQ(1.33)),  -1),
        ( 4000, PE2(toA(3),   toQ(1.33)),  -1),
    ],
    # loosely based on the equal loudness contour at 60dB or something
    'raw_ELC': [
        (   40, HP2(0,        toQ(1.33)),   0),
        (  400, HP1(0,0),                   6),
        ( 1400, PE2(toA(-3),  toQ(1.33)),   1),
        ( 4000, PE2(toA(5),   toQ(1.00)),-1.5),
        ( 4000, LP2(0,        toQ(1.33)), 1.5),
    ],
    # here's the ideas written out:
    # low (<40) freqs dont contribute much to ears (feel doesnt count.)
    # high (>14000) freqs are mostly unheard.
    # 750 Hz isn't too painful to the ears, but cutting them would give
    # overly-produced songs not enough gain to hear vocals, so keep it flat.
    # we're supposedly less sensitive to 1400 Hz, but i need to
    # boost high freqs so the RMS even catches it, so keep that flat too.
    'raw3': [
        (   40, HP2(0,        toQ(1.33)), 0.0),
        (  400, HP1(0,                0), 4.5),
        ( 1400, PE2(toA(-2),  toQ(1.33)), 0.0),
        ( 8000, PE2(toA(3),   toQ(1.00)), 0.0),
        (10000, LP2(0,        toQ(0.50)),-0.5),
    ],
    'tilt_test': [
        (10000, HP1(0,0),                  30),
        ( 1000, HS1(toA(-16),         0), 1.5),

        (   40, HP2(0,        toQ(1.00)), 0.0),
        (10000, LP1(0,                0), 0.0),
    ],
    # average curve of my 227 favorite songs
    'np2': [
        nf(LP1,    20,    0,    1,   32),
        nf(HS1,   800,    9,    1, -4.5),
        nf(LP2, 14000,    0, 1.33,    0),
        nf(LP2, 14000,    0, 0.90,    0),
        nf(HP2,    77,    0, 1.00,    0),
        nf(LS2,    38,   -9, 1.00,    0),
        nf(PE2,    64,  4.5, 1.20,    0),
    ],
    # same but for the side channel
    'np2s': [
        nf(LP1,    20,    0,    1,   32),
        nf(HS1,   800,    9,    1, -4.5),
        nf(LP2, 14000,    0, 1.33,    0),
        nf(HP2,    90,    0, 1.11,    0),
        nf(PE2,    30, -9.5, 1.00,    0),
        #(17500, LP2(0,            _bq2a),   0),
        #(17500, LP2(0,            _bq2b),   0),
    ],
}
