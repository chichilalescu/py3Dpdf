from tvtk.api import tvtk
import numpy as np

def get_isosurface_data(
        x1Dgrid = None,
        y1Dgrid = None,
        z1Dgrid = None,
        field = None,
        values = []):
    data = []
    r = tvtk.RectilinearGrid()
    if field.flags['C_CONTIGUOUS']:
        r.point_data.scalars = field.T.ravel()
        r.dimensions = field.T.shape
    else:
        r.point_data.scalars = field.ravel()
        r.dimensions = field.shape
    r.x_coordinates = x1Dgrid
    r.y_coordinates = y1Dgrid
    r.z_coordinates = z1Dgrid
    iso = tvtk.ContourFilter(input = r)
    for val in values:
        iso.set_value(0, val)
        iso.update()
        ip = {'points' : np.array(
                      iso.output.points),
              'triangles' : np.reshape(
                      iso.output.polys.data.to_array(),
                      (-1, 4))[:, 1:].copy()}
        data.append(ip)
    return data

