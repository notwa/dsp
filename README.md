# random dsp code

it's a bunch of half-baked python code that's kinda handy.

don't expect commits, docs, or comments to be any verbose.

## the stuff

* a basic BS.1770-3 normalization implementation
— [bs.py](/lib/bs.py)

* biquad butterworth/chebyshev filters [(via DSPFilters)][dspf]
— [butterworth.py](/lib/butterworth.py)

* s-plane to z-plane conversion
— [planes.py](/lib/planes.py)

* various functions for biquad filters
— [bq.py](/lib/bq.py) [\_\_init\_\_.py](/lib/__init__.py)

* some functions for state-variable filters [(via Raph Levien)][svf]
— [svf.py](/lib/svf.py)

* sine sweeps, and the Optimized Aoshima's Time-Stretched Pulse [(via here)][sweeps]
— [sweeps.py](/lib/sweeps.py)

* a lot of stuff for magnitude plotting like tilting and smoothing
— [fft.py](/lib/fft.py) [smoothfft.py](/lib/smoothfft.py) [\_\_init\_\_.py](/lib/__init__.py)

* rough experiments with psychoacoustic equalization ("neon pink" and other crap)
— [data.py](/lib/data.py) [\_\_init\_\_.py](/lib/__init__.py)

* miscellaneous matplotlib stuff
— [plot.py](/lib/plot.py)

* miscellaneous utility functions
— [util.py](/lib/util.py) [wav.py](/lib/wav.py)

[dspf]: https://github.com/vinniefalco/DSPFilters/
[sweeps]: http://www.sound.sie.dendai.ac.jp/dsp/e-21.html
[svf]: http://nbviewer.ipython.org/urls/music-synthesizer-for-android.googlecode.com/git/lab/Second%20order%20sections%20in%20matrix%20form.ipynb

all wrapped up in a inconveniently generic "lib" module!

## dependencies

python 3.4+

numpy scipy sympy matplotlib ewave

usually run in an ipython environment.
