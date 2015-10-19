import numpy as np

def LPB(n):
    # crap ripped from https://github.com/vinniefalco/DSPFilters/blob/master/shared/DSPFilters/source
    """n-th degree butterworth low-pass filter cascade

    -3 dB at center frequency."""
    series = []
    pi2 = np.pi/2
    pairs = int(n/2)
    for i in range(pairs):
        # magnitude = 1
        theta = pi2*(1 + (2*i + 1)/n)
        real = np.cos(theta)
        imag = np.sin(theta)
        num = (0, 0, 1)
        den = (1, -2*real, real*real + imag*imag)
        series += [(num, den)]
    if n % 2:
        num = (0, 1)
        den = (1, 1)
        series += [(num, den)]
    return series

def LPC(n, ripple, type=1):
    # crap ripped from https://github.com/vinniefalco/DSPFilters/blob/master/shared/DSPFilters/source
    # FIXME: type 2 has wrong center frequency?
    """n-th degree chebyshev low-pass filter cascade

    0 dB at center frequency for type 1.
    -ripple dB at center frequency for type 2.
    when ripple=0 and type=1, acts as butterworth."""
    series = []

    ripple = np.abs(ripple)
    lin = np.exp(ripple*0.1*np.log(10))

    if ripple != 0:
        if type == 2:
            eps = np.sqrt(1/(lin - 1))
        else:
            eps = np.sqrt(lin - 1)

        v0 = np.arcsinh(1/eps)/n
    else:
        if type == 2:
            v0 = 0 # allpass?
        else:
            v0 = 1 # butterworth

    sinh_v0 = -np.sinh(v0)
    cosh_v0 = np.cosh(v0)

    fn = np.pi/(2*n)
    pairs = int(n/2)
    for i in range(pairs):
        k = 2*i + 1
        theta = (k - n)*fn
        real = sinh_v0*np.cos(theta)
        imag = cosh_v0*np.sin(theta)

        if type == 2:
            d2 = real*real + imag*imag
            im = 1/np.cos(k*fn)
            real = real/d2
            imag = imag/d2
            num = (1, 0, im*im)
        else:
            num = (0, 0, 1)

        den = (1, -2*real, real*real + imag*imag)

        # normalize such that 0 Hz is 0 dB
        den = np.array(den)
        gain = den[2]/num[2]
        den /= gain

        series += [(num, den)]
    if n % 2:
        real = sinh_v0
        if type == 2:
            real = 1/real
        num = (0, 1)
        den = (1/-real, 1)
        series += [(num, den)]
    return series

