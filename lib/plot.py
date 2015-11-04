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

def phase_response_setup(ax, div=12, yL=ticker.AutoMinorLocator(2)):
    ax.set_xlim(20, 20000)
    ax.set_ylim(-180, 180)
    ax.set_yticks(tuple(range(-180, 180 + 1, int(360/div))))
    ax.yaxis.set_minor_locator(yL)
    ax.grid(True, 'both')
    ax.set_xlabel('frequency (Hz)')
    ax.set_ylabel('phase (degrees)')

def cleanplot():
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.set_position([0,0,1,1])
    return fig, ax

def new_response(*args, **kwargs):
    fig = plt.figure()
    ax = fig.gca()
    response_setup(ax, *args, **kwargs)
    return fig, ax

def new_phase_response(*args, **kwargs):
    fig = plt.figure()
    ax = fig.gca()
    phase_response_setup(ax, *args, **kwargs)
    return fig, ax

def new_bode(magnitude_offset=0):
    fig = plt.figure()
    ax1 = fig.gca()
    ax2 = ax1.twinx()
    ymin = -24 + magnitude_offset
    ymax = 24 + magnitude_offset
    response_setup(ax1, ymin, ymax)
    phase_response_setup(ax2)

    cc = plt.style.library['ggplot']['axes.color_cycle']
    ax1.set_ylabel(ax1.get_ylabel(), color=cc[0])
    ax2.set_ylabel(ax2.get_ylabel(), color=cc[1])
    for tl in ax1.get_yticklabels():
        tl.set_color(cc[0])
    for tl in ax2.get_yticklabels():
        tl.set_color(cc[1])

    #ax1.hlines(0,    20,    40, linewidth=0.5, color=cc[0])
    #ax2.hlines(0, 10000, 20000, linewidth=0.5, color=cc[1])

    # ax1 will use the initial color, so tell ax2 to iterate to the second
    next(ax2._get_lines.color_cycle)

    # ax1 and ax2 should have identical grids;
    # disable ax2's so it doesn't overlap ax1's plot lines.
    ax2.grid(False, which='both')
    return fig, ax1, ax2
