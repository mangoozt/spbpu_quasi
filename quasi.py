import os
import numpy as np
import sys
import matplotlib.pyplot as plt


def last_length(f):
    """Read last N lines from file fname."""
    former_pos = f.tell()
    BUFSIZ = 128
    # True if open() was overridden and file was opened in text
    # mode. In that case readlines() will return unicode strings
    # instead of bytes.
    encoded = getattr(f, 'encoding', False)
    CR = '\n' if encoded else b'\n'
    key = '\n101010101' if encoded else b'\n101010101'
    f.seek(0, os.SEEK_END)
    fsize = f.tell()
    block = -1
    pos = BUFSIZ
    exit = False
    while not exit:
        f.seek(fsize - pos)
        if abs(pos) >= fsize:
            f.seek(0)
            break
        else:
            f.seek(fsize - pos)
            string = f.read(BUFSIZ)
            newline = string.find(CR)
            keypos = string.find(key, newline)
            if keypos is not -1:
                f.seek(fsize - pos + keypos + len(CR))
                break
            else:
                pos += -newline + BUFSIZ

    f.readline()

    a = np.fromstring(f.readline(), dtype="float", count=4, sep=' ')[2]
    f.seek(former_pos, os.SEEK_SET)
    return a


def gen_state(state, crack):
    if len(crack) != 0:
        x = []
        uppy = []
        downy = []
        xx=0
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
        width = last_length(f)
        print('Last length: %f' % width)
        print(f.tell())
        state = np.array(4)
        crack = []
        for line in f:
            if line[:9] == '101010101':
                if len(crack) != 0:
                    (x, uppy, downy) = gen_state(state, crack)
                    fig, (ax1) = plt.subplots(1, 1, sharex=True)
                    ax1.set_xlim(right=width)
                    ax1.fill_between(x, uppy, downy)
                    plt.show()
                    crack = []
                print('New state!')
                state = np.fromstring(line, sep=' ')
                print(state)
            else:
                crack.append(np.fromstring(line, sep=' '))
        (x, uppy, downy) = gen_state(state, crack)
        fig, (ax1) = plt.subplots(1, 1, sharex=True)
        ax1.set_xlim(right=width)
        ax1.fill_between(x, uppy, downy)
        plt.show()