import numpy as np
import py2asy
import py2asy.tvtk_tools

def main(
        n = 32,
        kmax = None):
    z, y, x = np.mgrid[
        -np.pi:np.pi:n*1j,
        -np.pi:np.pi:n*1j,
        -np.pi:np.pi:n*1j]
    if type(kmax) == type(None):
        kmax = int(n/16)
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
    grid1D = np.linspace(-np.pi, np.pi, n, endpoint = False)
    data = py2asy.tvtk_tools.get_isosurface_data(
        field = f,
        x1Dgrid = grid1D,
        y1Dgrid = grid1D,
        z1Dgrid = grid1D,
        values = [0.0])
    asy_txt = py2asy.triangulated_surface_to_asy(
        data[0]['points'],
        data[0]['triangles'])
    py2asy.asy_to_pdf(
        asy_objects = [asy_txt],
        keep_tex = True)
    return None

if __name__ == '__main__':
    main()

