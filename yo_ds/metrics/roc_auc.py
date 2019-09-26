import numpy as np
from yo_fluq_ds import *
from sklearn.metrics import roc_curve
from matplotlib import pyplot as plt
from matplotlib.axes import Axes



def _inner_roc_optimal_threshold(curve):
    dsts = curve[0] ** 2 + (1 - curve[1]) ** 2
    argmin = np.argmin(dsts)
    val = curve[2][argmin]
    return curve[0][argmin], curve[1][argmin], val

def roc_optimal_threshold(y_true, y_pred):
    curve = roc_curve(y_true, y_pred)
    _, __, val = _inner_roc_optimal_threshold(curve)
    return val
