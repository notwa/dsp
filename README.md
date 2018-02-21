# random dsp code

it's a bunch of half-baked python code that's kinda handy.

don't expect commits, docs, or comments to be any verbose.

feel free to modify and adapt the [autoupdate](autoupdate)
shell script for your own repos like this!

## the stuff

* a basic BS.1770-3 normalization implementation
— [bs.py](/lib/bs.py)

* biquad butterworth/chebyshev filters
  [(via DSPFilters)][dspf]
— [nsf.py](/lib/nsf.py)

* modified bilinear transformation: s-plane to z-plane
— [planes.py](/lib/planes.py)

* various functions for biquad filters
— [bq.py](/lib/bq.py)

* some functions for state-variable filters
  [(via Raph Levien)][svf]
— [svf.py](/lib/svf.py)

* sine sweeps, and the Optimized Aoshima's Time-Stretched Pulse
  [(via here)][sweeps]
— [sweeps.py](/lib/sweeps.py)

* basic [cepstrum][cep] utilities like minimum-phase reconstruction
  [(via Julius Smith)][jos3]
— [cepstrum.py](/lib/cepstrum.py)

* utilities for magnitude plotting, including tilting and smoothing
— [fft.py](/lib/fft.py) [smoothfft.py](/lib/smoothfft.py) [mag.py](/lib/mag.py)

* a couple hard-coded polyphase halfband IIRs for nonlinear-phase resampling
  or approximating hilbert transforms
  (read more: [Olli Niemitalo][olli])
— [piir.py](/lib/piir.py)

* a dozen windowing functions and utility functions for constructing them
— [windowing.py](/lib/windowing.py)

* ad-hoc experiments with psychoacoustic equalization
  ("neon pink" and other crap before i realized
   "grey noise" was the term i was looking for)
— [data.py](/lib/data.py)

* miscellaneous matplotlib stuff
— [plot.py](/lib/plot.py)

* miscellaneous utility functions
— [util.py](/lib/util.py) [wav.py](/lib/wav.py)

[dspf]: //github.com/vinniefalco/DSPFilters/
[svf]: http://nbviewer.jupyter.org/github/google/music-synthesizer-for-android/blob/master/lab/Second%20order%20sections%20in%20matrix%20form.ipynb
[sweeps]: http://www.sound.sie.dendai.ac.jp/dsp/e-21.html
[cep]: //en.wikipedia.org/wiki/Cepstrum
[jos3]: //ccrma.stanford.edu/~jos/fp/
[olli]: http://yehar.com/blog/?p=368

all wrapped up in a inconveniently named "lib" module!

## dependencies

python 3.5+

numpy scipy sympy matplotlib ewave

usually run in an ipython environment.
