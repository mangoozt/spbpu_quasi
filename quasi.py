import os
import numpy as np
import sys
import matplotlib.pyplot as plt

key = 101010101.


def max_length(data):
    a = np.max(data[np.where(data[:, 0] == key), 2])
    return a


def max_ydev(data):
    a = np.max(np.abs(data[np.where(data[:, 0] != key), 2:3]))
    return a


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
            print('x1: %f' % xx)
            x.append(xx)
        x.append(xx)
        print(crack)
        uppy.append(crack[-1][2])
        uppy.append(crack[-1][2])
        downy.append(crack[-1][3])
        downy.append(crack[-1][3])
        print('x2: %f' % state[2])
        x.append(state[2])
        return (x, uppy, downy)
    return False


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        quasi = np.loadtxt(f)
    print(quasi)
    width = max_length(quasi)
    print('Max length: %f' % width)
    height = max_ydev(quasi)
    print('Max dev: %f' % height)
    f = True
    s = np.where(quasi[:, 0] == key)[0]
    print(s)
    fig, (ax1) = plt.subplots(1, 1, sharex=True)
    ax1.set_xlim(right=width)
    ax1.set_ylim([-height, height])
    plt.ion()
    plt.show(block=False)
    for i in range(0, len(s)):
        print(s[i])
        if i < (len(s) - 1):
            (x, uppy, downy) = gen_state(quasi[s[i]], quasi[s[i] + 1:s[i + 1]])
        else:
            (x, uppy, downy) = gen_state(quasi[s[i]], quasi[s[i] + 1:])
        ax1.fill_between(x, uppy, downy, color='g')
        fig.canvas.draw()
        plt.draw()

    plt.show(block=True)
