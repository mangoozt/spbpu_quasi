import os
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from colorama import Fore, Back, Style

plt.style.use('ggplot')


def crack_xrange(data):
    a = np.max(data[np.where(data[:, 0] == key), 2])
    return [0, a]


def events_xrange(data):
    return [np.min(data[:, 0]), np.max(data[:, 0])]


def crack_yrange(data):
    c = np.abs(data[np.where(data[:, 0] != key), 2:3])
    a = np.min(c)
    b = np.max(c)
    return [a, b]


def events_yrange(data):
    return [np.min(data[:, 1]), np.max(data[:, 1])]


def gen_state_verts(state, crack):
    if len(crack) != 0:
        x = []
        uppy = []
        downy = []
        xx = 0
        for block in crack[:-1]:
            x.append(xx)
            uppy.append(block[2])
            uppy.append(block[2])
            downy.append(block[3])
            downy.append(block[3])
            xx += state[3]
            x.append(xx)
        x.append(xx)
        uppy.append(crack[-1][2])
        uppy.append(crack[-1][2])
        downy.append(crack[-1][3])
        downy.append(crack[-1][3])
        x.append(state[2])
        x = np.concatenate((x, np.flipud(x)))
        y = np.concatenate((uppy, np.flipud(downy)))
        return np.dstack((x, y))
    return False


def init():  # initialize animation
    # line.set_data([], [],[])
    title.set_text(r'')
    return particles, line, title


def animate(i):  # define amination using Euler
    global s
    if i < (len(s) - 1):
        verts = gen_state_verts(quasi[s[i]], quasi[s[i] + 1:s[i + 1]])
    else:
        verts = gen_state_verts(quasi[s[i]], quasi[s[i] + 1:])
    print(Style.BRIGHT + 'State #{}: t={}, length={}'.format(i, quasi[s[i], 1], quasi[s[i], 2]))
    print(Style.DIM + 'Verts:')
    print(verts)
    line.set_verts(verts)
    title.set_text(r"$t = {0:.2f}$".format(quasi[s[i], 1]))
    return particles, line, title


key = 101010101.
if __name__ == "__main__":
    quasi = np.loadtxt(sys.argv[1])
    if len(sys.argv) > 2:
        events = np.loadtxt(sys.argv[2], usecols=(2, 3, 6))
        ev_xrange = events_xrange(events)
        ev_yrange = events_yrange(events)
    else:
        events = [[], []]
        ev_xrange = [0, 0]
        ev_yrange = [0, 0]
    xrange = [np.minimum(crack_xrange(quasi)[0], ev_xrange[0]),
              np.maximum(crack_xrange(quasi)[1], ev_xrange[1])]
    print('xrange: {}'.format(xrange))
    yrange = [np.minimum(crack_yrange(quasi)[0], ev_yrange[0]),
              np.maximum(crack_yrange(quasi)[1], ev_yrange[1])]
    print('yrange: {}'.format(yrange))
    f = True
    s = np.where(quasi[:, 0] == key)[0]
    print(s)

    fig, _ax = plt.subplots(figsize=(7.5, 7.5))  # setup plot
    ax = plt.axes(xlim=xrange, ylim=yrange)  # draw range
    particles = ax.scatter(events[:, 0], events[:, 1], alpha=.4, s=1 + events[:, 2],
                           color='k')  # setup plot for particle
    line = ax.fill_between([], [], [], color='r')  # setup plot for trajectry
    title = ax.text(0.5, 1.05, r'', transform=ax.transAxes, va='center')  # title
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(s), interval=1, blit=True, repeat=False)  # draw animation
    plt.show()
    # anim.save('movie.mp4',fps=20,dpi=400)
