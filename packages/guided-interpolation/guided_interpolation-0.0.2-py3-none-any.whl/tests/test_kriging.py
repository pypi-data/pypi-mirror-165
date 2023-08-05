import numpy as np

from guided_interpolation.kriging import ordinary_kriging


def test_kriging():
    
    # Bulding the grid
    d = np.array([[5, 18], [15, 13], [11, 4], [1, 9]])
    values = np.array([[3.1, 3.9, 4.1, 3.2]])
    values = np.transpose(values)
    x = np.array([10, 10])

    # Kriging parameters
    xmean = 3.5
    xvar = 0.1
    l = 9
    krigmodel = 'exp'

    xsk, _ = ordinary_kriging(x, d, values, xvar, l, krigmodel)
    print(xsk)


    assert(xsk == 3.65)




