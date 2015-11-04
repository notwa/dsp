import numpy as np
import scipy.signal as sig

from .util import *
from .planes import s2z

bq_run = lambda bq, xs: sig.lfilter(*bq, x=xs, axis=0)

nfba = lambda b, a: (1/tau, (b, a), 0)
nf = lambda t, f, g, bw, mg: (f, t(toA(g), toQ(bw)), mg)

LP1 = lambda A, Q: ((0,1),(1,1))
HP1 = lambda A, Q: ((1,0),(1,1))
LS1 = lambda A, Q: ((1,A),(1,1/A))
HS1 = lambda A, Q: ((A,1),(1/A,1))

# patterns observed, in case some simplification could be done:
# a always gets divided by A instead of multiplied
# b1 and a1 always /= Q

LP2 = lambda A, Q: ((0,     0, 1),
                    (1,   1/Q, 1))
HP2 = lambda A, Q: ((1,     0, 0),
                    (1,   1/Q, 1))
PE2 = lambda A, Q: ((1,   A/Q, 1),
                    (1, 1/A/Q, 1))
AP2 = lambda A, Q: ((1,   1/Q, 1),
                    (1,   1/Q, 1))
BP2a= lambda A, Q: ((0,  -A/Q, 0),
                    (1, 1/A/Q, 1))
BP2b= lambda A, Q: ((0,-A*A/Q, 0),
                    (1,   1/Q, 1))
NO2 = lambda A, Q: ((1,     0, 1),
                    (1,   1/Q, 1))
LS2 = lambda A, Q: ((1,     np.sqrt(A)/Q,   A),
                    (1,   1/np.sqrt(A)/Q, 1/A))
HS2 = lambda A, Q: ((A,     np.sqrt(A)/Q,   1),
                    (1/A, 1/np.sqrt(A)/Q,   1))

gen_filters = lambda cascade, srate: [
    s2z(*f[1], fc=f[0], srate=srate, gain=10**(f[2]/20)) for f in cascade
]
