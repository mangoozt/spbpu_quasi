import os
import numpy as np
import sys
import matplotlib.pyplot as plt

key = 101010101.


def crack_xrange(data):
    a = np.max(data[np.where(data[:, 0] == key), 2])
    return [0, a]


def events_xrange(data):
    return [np.min(data[:, 2]), np.max(data[:, 2])]


def crack_yrange(data):
    c = np.abs(data[np.where(data[:, 0] != key), 2:3])
    a = np.min(c)
    b = np.max(c)
    return [a, b]


def events_yrange(data):
    return [np.min(data[:, 3]), np.max(data[:, 3])]


def gen_state(state, crack):
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
        print(crack)
        uppy.append(crack[-1][2])
        uppy.append(crack[-1][2])
        downy.append(crack[-1][3])
        downy.append(crack[-1][3])
        x.append(state[2])
        return (x, uppy, downy)
    return False


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        quasi = np.loadtxt(f)
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            events = np.loadtxt(f)
        ev_xrange = events_xrange(events)
        ev_yrange = events_yrange(events)
    else:
        ev_xrange = [0, 0]
        ev_yrange = [0, 0]
    xrange = [np.minimum(crack_xrange(quasi)[0], ev_xrange[0]),
              np.maximum(crack_xrange(quasi)[1], ev_xrange[1])]
    print('max crack x: {}'.format(xrange))
    yrange = [np.minimum(crack_yrange(quasi)[0], ev_yrange[0]),
              np.maximum(crack_yrange(quasi)[1], ev_yrange[1])]
    print('Max crack y dev: {}'.format(yrange))
    f = True
    s = np.where(quasi[:, 0] == key)[0]
    print(s)
    fig, (ax1) = plt.subplots(1, 1, sharex=True)
    #    ax1.set_xlim(xrange)
    #    ax1.set_ylim(yrange)
    plt.ion()
    plt.show(block=False)
    t = 0
    for i in range(0, len(s)):
        ax1.clear()
        ax1.set_xlim(xrange)
        ax1.set_ylim(yrange)
        print(s[i])
        if i < (len(s) - 1):
            (x, uppy, downy) = gen_state(quasi[s[i]], quasi[s[i] + 1:s[i + 1]])
        else:
            (x, uppy, downy) = gen_state(quasi[s[i]], quasi[s[i] + 1:])
        ax1.fill_between(x, uppy, downy, color='r')
        if len(sys.argv) > 2:
            ax1.scatter(events[:, 2], events[:, 3], alpha=.4, s=1 + events[:, 6], color='k')
        fig.canvas.draw()
        plt.draw()
        plt.pause((quasi[s[i], 1] - t) / 1000)
        t = quasi[s[i], 1]

    plt.show(block=True)
