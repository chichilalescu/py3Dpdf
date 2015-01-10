import numpy as np

def get_turbulent_scalar(
        n = 32,
        kmax = None,
        box = [[-np.pi,np.pi],
               [-np.pi,np.pi],
               [-np.pi,np.pi]]):
    if type(kmax) == type(None):
        kmax = int(n/16)
    z, y, x = np.mgrid[
        box[0][0]:box[0][1]:n*1j,
        box[1][0]:box[1][1]:n*1j,
        box[2][0]:box[2][1]:n*1j]
    a = np.random.randn(2*kmax+1, 2*kmax+1, kmax+1)
    b = np.random.randn(2*kmax+1, 2*kmax+1, kmax+1)
    a[0, 0, 0] = 0.0
    f = np.zeros(x.shape, x.dtype)
    for k in range(2*kmax+1):
        for j in range(2*kmax+1):
            for i in range(kmax+1):
                f += ((a[k, j, i]*np.cos(i*x + (j-kmax)*y + (k-kmax)*z) +
                       b[k, j, i]*np.sin(i*x + (j-kmax)*y + (k-kmax)*z)) /
                      (i**2 + j**2 + k**2 + 1)**.75)
    return (x, y, z, f)

