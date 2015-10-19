import matplotlib.pyplot as plt
from matplotlib import ticker

def response_setup(ax, ymin=-24, ymax=24, yL=ticker.AutoMinorLocator(3)):
    ax.set_xlim(20, 20000)
    ax.set_ylim(ymin, ymax)
    ax.set_yticks(tuple(range(ymin, ymax + 1, 6)))
    ax.yaxis.set_minor_locator(yL)
    ax.grid(True, 'both')
    ax.set_xlabel('frequency (Hz)')
    ax.set_ylabel('magnitude (dB)')

def cleanplot():
    fig, ax = plt.subplots()
    fig.set_size_inches((16, 16))
    ax.set_axis_off()
    ax.set_position([0,0,1,1])
    return fig, ax

def new_response(*args, **kwargs):
    #fig, ax = plt.subplots()
    fig = plt.figure()
    ax = fig.gca()
    response_setup(ax, *args, **kwargs)
    fig.set_size_inches(10, 6)
    return fig, ax
