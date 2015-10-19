from . import tau, unwarp

import numpy as np

# via http://nbviewer.ipython.org/urls/music-synthesizer-for-android.googlecode.com/git/lab/Second%20order%20sections%20in%20matrix%20form.ipynb
def svf_core(w0, Q, m, shelfA=1, gain=1):
    # TODO: implement constant gain parameter
    g = unwarp(w0)*shelfA
    a1 = 1/(1 + g*(g + 1/Q))
    a2 = g*a1
    a3 = g*a2
    A = np.array([[2*a1 - 1, -2*a2], [2*a2, 1 - 2*a3]])
    B = np.array([2*a2, 2*a3])
    v0 = np.array([1, 0, 0])
    v1 = np.array([a2, a1, -a2])
    v2 = np.array([a3, a2, 1 - a3])
    C = v0*m[0] + v1*m[1] + v2*m[2]
    return A, B, C

LP2S = lambda A, Q: (Q, [0,    0,  1], 1)
BP2S = lambda A, Q: (Q, [0,    1,  0], 1)
HP2S = lambda A, Q: (Q, [1, -1/Q, -1], 1)
#AP2S = lambda A, Q:
#BP2aS = lambda A, Q:
#BP2bS = lambda A, Q:
NO2S = lambda A, Q: (Q, [1, -1/Q,  0], 1)
PE2S = lambda A, Q: (Q*A, [1, (A*A - 1)/A/Q, 0], 1)
LS2S = lambda A, Q: (Q, [1,     (A - 1)/Q, A*A - 1], 1/np.sqrt(A))
HS2S = lambda A, Q: (Q, [A*A, (1 - A)*A/Q, 1 - A*A],   np.sqrt(A))

# actual peaking filter (not a bell?)
#PE2S = lambda A, Q: ([1, -1/Q, -2], 1)
# original uncompensated
#PE2S = lambda A, Q: (Q, [1,   (A*A - 1)/Q,       0], 1)
#LS2S = lambda A, Q: (Q, [1,     (A - 1)/Q, A*A - 1], 1/np.sqrt(A))
#HS2S = lambda A, Q: (Q, [A*A, (A - A*A)/Q, 1 - A*A], 1/np.sqrt(A))

gen_filters_svf = lambda cascade, srate: [
    svf_core(tau*f[0]/srate, *f[1], gain=10**(f[2]/20)) for f in cascade
]

def svf_run(svf, xs):
    A, B, C = svf
    result = []
    y = np.zeros(2) # filter memory
    for x in xs:
        result.append(np.dot(C, np.concatenate([[x], y])))
        y = B*x + np.dot(A, y)
    return np.array(result)

def svf_mat(svf):
    A, B, C = svf
    AA = np.dot(A, A)
    AB = np.dot(A, B)
    CA = np.dot(C[1:], A)
    cb = np.dot(C[1:], B)
    return np.array([[ C[0],    0,     C[1],     C[2]],
                     [   cb, C[0],    CA[0],    CA[1]],
                     [AB[0], B[0], AA[0][0], AA[0][1]],
                     [AB[1], B[1], AA[1][0], AA[1][1]]])

def svf_run4(mat, xs):
    assert(len(xs) % 2 == 0)
    out = np.zeros(len(xs))
    y = np.zeros(4) # filter memory
    for i in range(0, len(xs), 2):
        y[0:2] = xs[i:i+2]
        y = np.dot(mat, y)
        out[i:i+2] = y[0:2]
    return out
