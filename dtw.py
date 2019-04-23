#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version='1.3',
description='Python DTW Module',
author='Pierre Rouanet',
author_email='pierre.rouanet@gmail.com',
url='https://github.com/pierre-rouanet/dtw',
license='GNU GENERAL PUBLIC LICENSE Version 3'

Modified by Juliette MILLET
"""

from numpy import array, zeros, argmin, inf, ndim
from scipy.spatial.distance import cdist
import numpy as np

def __kl_divergence(x, y):
    """ just the KL-div """
    pq = np.dot(x, np.log(y.transpose()))
    pp = np.tile(np.sum(x * np.log(x), axis=1).reshape(x.shape[0], 1), (1, y.shape[0]))
    return pp - pq


def kl_divergence(x, y, thresholded=True, symmetrized=True, normalize=True):
    """ Kullback-Leibler divergence 
    x and y should be 2D numpy arrays with "times" on the lines and "features" on the columns
     - thresholded=True => means we add an epsilon to all the dimensions/values
                           AND renormalize inputs.
     - symmetrized=True => uses the symmetrized KL (0.5 x->y + 0.5 y->x).
     - normalize=True => normalize the inputs so that lines sum to one.
    """
    assert (x.dtype == np.float64 and y.dtype == np.float64) or (
        x.dtype == np.float32 and y.dtype == np.float32)
    x = x.reshape(1,-1)
    y = y.reshape(1,-1)
    assert (np.all(x.sum(1) != 0.) and np.all(y.sum(1) != 0.))
    if thresholded:
        normalize = True
    if normalize:
        x /= x.sum(1).reshape(x.shape[0], 1)
        y /= y.sum(1).reshape(y.shape[0], 1)
    if thresholded:
        eps = np.finfo(x.dtype).eps
        x = x + eps
        y = y + eps
        x /= x.sum(1).reshape(x.shape[0], 1)
        y /= y.sum(1).reshape(y.shape[0], 1)
    res = __kl_divergence(x, y)
    if symmetrized:
        res = 0.5 * res + 0.5 * __kl_divergence(y, x).transpose()
    return np.float64(res)

def dtw(x, y, dist, warp=1):
    """
    Computes Dynamic Time Warping (DTW) of two sequences.
    :param array x: N1*M array
    :param array y: N2*M array
    :param func dist: distance used as cost measure
    :param int warp: how many shifts are computed.
    Returns the minimum distance, the cost matrix, the accumulated cost matrix, and the wrap path.
    """
    assert len(x)
    assert len(y)
    r, c = len(x), len(y)
    D0 = zeros((r + 1, c + 1))
    D0[0, 1:] = inf
    D0[1:, 0] = inf
    D1 = D0[1:, 1:]  # view
    for i in range(r):
        for j in range(c):
            D1[i, j] = dist(x[i], y[j])
    C = D1.copy()
    for i in range(r):
        for j in range(c):
            min_list = [D0[i, j]]
            for k in range(1, warp + 1):
                i_k = min(i + k, r - 1)
                j_k = min(j + k, c - 1)
                min_list += [D0[i_k, j], D0[i, j_k]]
            D1[i, j] += min(min_list)
    if len(x)==1:
        path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), zeros(len(x))
    else:
        path = _traceback(D0)
    return D1[-1, -1] / sum(D1.shape), C, D1, path


def accelerated_dtw(x, y, dist, warp=1):
    """
    Computes Dynamic Time Warping (DTW) of two sequences in a faster way.
    Instead of iterating through each element and calculating each distance,
    this uses the cdist function from scipy
    (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html)
    :param array x: N1*M array
    :param array y: N2*M array
    :param string or func dist: distance parameter for cdist. When string is given,
    cdist uses optimized functions for the distance metrics.
    If a string is passed, the distance function can be 'braycurtis', 'canberra',
    'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean', 'hamming',
    'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto',
    'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'wminkowski', 'yule'.
    :param int warp: how many shifts are computed.
    Returns the minimum distance, the cost matrix, the accumulated cost matrix, and the wrap path.
    """
    assert len(x)
    assert len(y)
    if ndim(x) == 1:
        x = x.reshape(-1, 1)
    if ndim(y) == 1:
        y = y.reshape(-1, 1)
    r, c = len(x), len(y)
    D0 = zeros((r + 1, c + 1))
    D0[0, 1:] = inf
    D0[1:, 0] = inf
    D1 = D0[1:, 1:]
    D0[1:, 1:] = cdist(x, y, dist)
    C = D1.copy()
    for i in range(r):
        for j in range(c):
            min_list = [D0[i, j]]
            for k in range(1, warp + 1):
                min_list += [D0[min(i + k, r - 1), j],
                             D0[i, min(j + k, c - 1)]]
            D1[i, j] += min(min_list)
    if len(x) == 1:
        path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), zeros(len(x))
    else:
        path = _traceback(D0)
    return D1[-1, -1] / sum(D1.shape), C, D1, path


def _traceback(D):
    i, j = array(D.shape) - 2
    p, q = [i], [j]
    while (i > 0) or (j > 0):
        tb = argmin((D[i, j], D[i, j+1], D[i+1, j]))
        if tb == 0:
            i -= 1
            j -= 1
        elif tb == 1:
            i -= 1
        else:  # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return array(p), array(q)
