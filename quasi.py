import os
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from colorama import Fore, Back, Style


# dy=np.max(quasi[:,])
def makeverts(state):
    l = state[0, 2]
    h = state[0, 3]
    print(state)
    yy = np.concatenate((np.repeat(state[1:, 2], 2), np.repeat(np.flipud(state[1:, 3]), 2)))
    xx = [h * k for k in range(1, len(state))]
    xx = np.concatenate((xx, np.flipud(xx)[1:]))
    xx = np.concatenate(([0], xx.repeat(2), [0]))
    xx[xx > l] = l
    return np.dstack((xx, yy))


def init():  # initialize animation
    # line.set_data([], [],[])
    title.set_text(r'')
    return particles, line, title


def animate(i):  # define amination using Euler
    global quasi
    verts = makeverts(quasi[i])
    print(Style.BRIGHT + 'State #{}: t={}, length={}'.format(i, quasi[i][0, 1], quasi[i][0, 2]))
    print(Style.DIM + 'Verts:')
    print(verts)
    line.set_verts(verts)
    title.set_text(r"$t = {0:.2f}$".format(quasi[i][0, 1]))
    return particles, line, title


key = 101010101.
if __name__ == "__main__":
    quasi = np.loadtxt(sys.argv[1])

    xrange = (0, np.max(quasi[:, 2]))
    keys = np.where(quasi[:, 0] == key)[0]
    c_y_max = np.max(np.abs(quasi[~keys, 2:3]))
    print(c_y_max)
    quasi = np.split(quasi, keys)[1:]

    if len(sys.argv) > 2:
        events = np.loadtxt(sys.argv[2], usecols=(2, 3, 6))
    else:
        events = [[], []]
    print('xrange: {}'.format(xrange))

    ev_yrange = [np.min(events[:, 1]), np.max(events[:, 1])]
    yrange = [np.minimum(-c_y_max, ev_yrange[0]),
              np.maximum(c_y_max, ev_yrange[1])]
    print('yrange: {}'.format(yrange))

    fig, _ax = plt.subplots(figsize=(7.5, 7.5))  # setup plot
    ax = plt.axes(xlim=xrange, ylim=yrange)  # draw range
    ax.set_aspect('equal', 'box')
    particles = ax.scatter(events[:, 0], events[:, 1], alpha=.8,
                           s=np.interp(events[:, 2], (np.min(events[:, 2]), np.max(events[:, 2])), (.1, 2)),
                           color='k')  # setup plot for particle
    line = ax.fill_between([], [], [], color='r')  # setup plot for trajectry
    title = ax.text(0.5, 1.05, r'', transform=ax.transAxes, va='center')  # title
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(quasi), interval=1, blit=True, repeat=False)  # draw animation
    plt.show()
    # anim.save('movie.mp4',fps=20,dpi=400)
