import numpy as np


def exponential_covariance(h, l):
    """

    """
    return np.exp(-3 * h/l)


def gaussian_covariance(h, l):
    """
    
    """
    return np.exp(-3 * h**2 / 1**2)

def spherical_covariance(h, l):
    c = np.zeros(h.shape)
    c[h <= 1] = 1 - 3 / 2 * h[h <= l] / l + 1 / 2 * h[h <= l] ** 3 / l ** 3


def spatial_covariance1d(h, l, krigmodel='exp'):
    """
    """

    if krigmodel == 'exp':
        return exponential_covariance(h, l)
    elif krigmodel == 'gau':
        return gaussian_covariance(h, l)
    elif krigmodel == 'sph':
        return spherical_covariance(h, l)
    else:
        raise NotImplementedError(f"{krigmodel} is an unsupported variogram model: Use 'exp', 'gau', or 'sph'.")
