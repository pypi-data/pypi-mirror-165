# coding: utf-8
# Author: Fábio Júnior
# Email = fabiojdf@id.uff.br
# License: LPGL

import numpy as np
import scipy

from utils.spatial_analysis import spatial_covariance1d


def ordinary_kriging(x, d, values, xvar, l, krigmodel='exp'):
    """
    Performing ordinary kriging.

    Parameters
    ----------
    x : array_like
        Coordinates of the location to be estimated.
    d : array_like
        Coordinates of the measurements.
    v : array_like
        Values of the measurements.
    xvar : float 
        Prior variance.
    l : float
        Correlation length.
    krigmodel : str
        Variogram model type ('exp', 'gau', 'sph').

    Returns
    -------
    xok : array_like
        Kriging estimate.
    xvarok : array_like
        Kriging variance.
    """

    nd = d.shape[0]
    
    xdtemp = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(np.vstack((x, d))))
    distvector = xdtemp[1:, 0]
    distmatrix = xdtemp[1:, 1:]

    krigmatrix = np.ones((nd + 1, nd + 1))
    krigvector = np.ones((nd + 1, 1))
    krigmatrix[-1, -1] = 0

    krigvector[0:-1, 0] = xvar * spatial_covariance1d(distvector, l, krigmodel)
    krigmatrix[0:-1, 0:-1] = xvar * spatial_covariance1d(distmatrix, l, krigmodel)

    # just to avoid numerical issues
    krigmatrix = krigmatrix + 0.000001 * xvar * np.eye(krigmatrix.shape[0])

    wkrig = np.linalg.lstsq(krigmatrix, krigvector, rcond=None)[0]

    xok = np.sum(wkrig[0:-1] * values)
    xvarok = xvar - np.sum(wkrig * krigvector)

    return xok, xvarok
    

