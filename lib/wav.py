import numpy as np
from . import lament

# TODO: don't use wavfile, it breaks on perfectly good files
import scipy.io.wavfile as wav
import ewave

def wav_smart_read(fn):
    lament('wav_smart_read(): DEPRECATED; use wav_read instead.')
    srate, s = wav.read(fn)
    if s.dtype != np.float64:
        bits = s.dtype.itemsize*8
        s = np.asfarray(s)/2**(bits - 1)
    return srate, s

def wav_smart_write(fn, srate, s):
    lament('wav_smart_write(): DEPRECATED; use ewave instead.')
    si = np.zeros_like(s, dtype='int16')
    bits = si.dtype.itemsize*8
    si += np.clip(s*2**(bits - 1), -32768, 32767)
    wav.write(fn, srate, si)

def wav_read(fn):
    with ewave.open(fn) as f:
        s = f.read()
        srate = f.sampling_rate
    if s.dtype == np.float32:
        s = np.asfarray(s)
    elif s.dtype != np.float64:
        bits = s.dtype.itemsize*8
        s = np.asfarray(s)/2**(bits - 1)
    return s, srate
