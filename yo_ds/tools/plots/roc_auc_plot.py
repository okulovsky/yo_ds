from ._common import *
from sklearn.metrics import roc_curve
import numpy as np


def _inner_roc_optimal_threshold(curve):
    dsts = curve[0] ** 2 + (1 - curve[1]) ** 2
    argmin = np.argmin(dsts)
    val = curve[2][argmin]
    return curve[0][argmin], curve[1][argmin], val

def roc_optimal_threshold(y_true, y_pred):
    curve = roc_curve(y_true, y_pred)
    _, __, val = _inner_roc_optimal_threshold(curve)
    return val

def roc_plot(true,predicted, name=None, number_fmt='{:.2f}',ax=None):
    ax = default_ax(ax)
    curve = roc_curve(true,predicted)
    ax.plot(curve[0], curve[1],label=name)
    ax.set_xlabel('TPR')
    ax.set_ylabel('FPR')
    x, y, val = _inner_roc_optimal_threshold(curve)
    ax.scatter(x,y)
    ax.text(x,y,number_fmt.format(val),ha='left',va='top')
