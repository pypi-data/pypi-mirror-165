import numpy as np
from matplotlib import pyplot as plt


# ----------------------------------------------------------------------
def agco(method_1, method_2, ticks, labels, sort='method_1', reference_c='C1', gain_c='C0', lose_c='C3', barwidth=6, ylabel='Accuracy [%]', xlabel='Subjects', gain_labels=['gain', 'lose'], fig=None, ax=None, size=(15, 5), dpi=90):
    """"""

    if fig is None:
        plt.figure(figsize=size, dpi=dpi)

    if ax is None:
        ax = plt.subplot(111)

    if sort == 'method_1':
        index = np.argsort(method_1)[::-1]
    elif sort == 'method_1r':
        index = np.argsort(method_1)
    if sort == 'method_2':
        index = np.argsort(method_2)[::-1]
    elif sort == 'method_2r':
        index = np.argsort(method_2)

    colors = np.array(method_2[index] -
                      method_1[index] < 0, dtype=np.object_)

    if sort.startswith('method_1'):
        p1, = plt.plot(method_1[index], color=reference_c, linestyle='--',)
        p2, = plt.plot(method_2[index], color=gain_c,
                       linestyle='--', alpha=0.3)
        colors[colors == 0] = gain_c
        colors[colors == 1] = lose_c
    elif sort.startswith('method_2'):
        p1, = plt.plot(method_2[index], color=reference_c, linestyle='--',)
        p2, = plt.plot(method_1[index], color=gain_c,
                       linestyle='--', alpha=0.3)
        colors[colors == 0] = lose_c
        colors[colors == 1] = gain_c

    p3 = plt.vlines(np.array(sorted(index))[colors == gain_c], method_1[index][colors == gain_c],
                    method_2[index][colors == gain_c], color=colors[colors == gain_c], linewidth=barwidth)
    p4 = plt.vlines(np.array(sorted(index))[colors == lose_c], method_1[index][colors == lose_c],
                    method_2[index][colors == lose_c], color=colors[colors == lose_c], linewidth=barwidth)

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(range(50), ticks[index], rotation=90)

    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)

    l1 = plt.legend([p1, p2, p3, p4], labels + gain_labels,
                    loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.13))
    plt.gca().add_artist(l1)

    return plt.gcf()
