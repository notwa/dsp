import numpy as np
import scipy.signal as sig


def magnitudes_window_setup(s, size=8192, overlap=0.661):
    # note: the default overlap value is only
    #       optimal for a blackman-harris window.
    L = s.shape[0]
    step = np.ceil(size*(1 - overlap))
    segs = np.ceil(L/step)
    return step, segs


def magnitudes(s, size=8192):
    step, segs = magnitudes_window_setup(s, size)

    L = s.shape[0]

    # blindly pad with zeros for friendlier ffts and overlapping
    z = np.zeros(size)
    s = np.r_[s, z]

    win_size = size

    win = sig.blackmanharris(win_size)
    win /= np.sqrt(np.sum(np.square(win)))

    count = 0
    for i in range(0, L - 1, int(step)):
        windowed = s[i:i+win_size]*win
        power = np.abs(np.fft.rfft(windowed, 2 * size))**2
        # this scraps the nyquist value to get exactly 'size' outputs
        yield power[0:size]
        count += 1

    # assert(segs == count)  # this is probably no good in a generator


def averfft(s, size=8192):
    """calculates frequency magnitudes by fft and averages them together."""
    step, segs = magnitudes_window_setup(s, size)

    avg = np.zeros(size)
    for power in magnitudes(s, size):
        avg += power/segs

    avg_db = 10*np.log10(avg)
    return avg_db
