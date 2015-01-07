import numpy as np
from mayavi import mlab
import py2asy

def get_isosurface_data(
        field,
        xgrid = None,
        ygrid = None,
        zgrid = None,
        value = None):
    """
    got the idea from
    http://enthought-dev.117412.n3.nabble.com/Accessing-the-triangle-data-of-a-mayavi-isosurface-td4025879.html
    """
    ## we need to use the transpose when plotting, because of reasons
    ## (no, I don't understand and I don't want to understand. it's stupid)
    if type(value) == type(None):
        value = np.average(field)
    if type(xgrid) == type(None):
        zgrid, ygrid, xgrid = np.mgrid[
                0:field.shape[0]-1:field.shape[0]*1j,
                0:field.shape[1]-1:field.shape[1]*1j,
                0:field.shape[2]-1:field.shape[2]*1j]
        bla = mlab.contour3d(
                field.T,
                contours = [value],
                transparent = True)
    else:
        bla = mlab.contour3d(
                xgrid.T,
                ygrid.T,
                zgrid.T,
                field.T,
                contours = [value],
                transparent = True)

    my_actor = bla.actor.actors[0]
    poly_data_object = my_actor.mapper.input
    points = np.array(poly_data_object.points)

    the_cells  = np.reshape(poly_data_object.polys.data.to_array(), [-1,4])
    triangles = the_cells[:, 1:].copy()
    del the_cells

    # points are stored as single precision, since I may feed them to getData
    data = {'points'    : points.astype(np.float32),
            'triangles' : triangles}
    return data

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
    data = get_isosurface_data(
        f,
        xgrid = x,
        ygrid = y,
        zgrid = z,
        value = 0.0)
    asy_txt = py2asy.triangulated_surface_to_asy(
        data['points'],
        data['triangles'])
    py2asy.asy_to_pdf(asy_objects = [asy_txt])
    return None

if __name__ == '__main__':
    main()

