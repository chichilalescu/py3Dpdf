#######################################################################
#                                                                     #
#  Copyright 2014 Cristian C Lalescu                                  #
#                                                                     #
#  This file is part of py3Dpdf.                                      #
#                                                                     #
#  py3Dpdf is free software: you can redistribute it and/or modify    #
#  it under the terms of the GNU General Public License as published  #
#  by the Free Software Foundation, either version 3 of the License,  #
#  or (at your option) any later version.                             #
#                                                                     #
#  py3Dpdf is distributed in the hope that it will be useful,         #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the      #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with py3Dpdf.  If not, see <http://www.gnu.org/licenses/>    #
#                                                                     #
#######################################################################

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
        ### this gets the centers of the faces
        rx = np.average(ip['points'][ip['triangles'], 0], axis = 1)
        ry = np.average(ip['points'][ip['triangles'], 1], axis = 1)
        rz = np.average(ip['points'][ip['triangles'], 2], axis = 1)

        ip['centers'] = np.vstack([rx, ry, rz]).T.copy()
        del rx, ry, rz
        ### now get normals
        ###
        # compute area of triangles
        ###

        edge1 = (ip['points'][ip['triangles'][:, 1], :] -
                 ip['points'][ip['triangles'][:, 0], :])
        edge2 = (ip['points'][ip['triangles'][:, 2], :] -
                 ip['points'][ip['triangles'][:, 0], :])

        NF = edge1.copy()

        #cross product
        NF[:, 0] = edge1[:, 1]*edge2[:, 2] - edge1[:, 2]*edge2[:, 1]
        NF[:, 1] = edge1[:, 2]*edge2[:, 0] - edge1[:, 0]*edge2[:, 2]
        NF[:, 2] = edge1[:, 0]*edge2[:, 1] - edge1[:, 1]*edge2[:, 0]

        dA = (np.sum(NF**2, axis = 1)**.5)
        NF /= dA[:, None]
        ip['areas'] = dA/2

        NF[np.where(np.isnan(NF))] = 0.0
        # gradients are supposed to point towards increasing values.
        # TODO: make sure the following line is always correct.
        ip['gradients'] = -NF
        data.append(ip)
    return data

def get_neighbours(
        data,
        function = None):
    ## apparently there is a get_cell_neighbors defined in vtk,
    ## but I have no idea how to use it
    if type(function) == type(None):
        function = [True for c in range(data['centers'].shape[0])]
    good_centers = np.where(function)[0]
    data['neighbours'] = [set([])
                          for c in range(data['centers'].shape[0])]
    point_triangles = [set([]) for p in range(data['points'].shape[0])]
    for c in good_centers:
        for p in data['triangles'][c]:
            point_triangles[p].add(c)
    for c in good_centers:
        for p in data['triangles'][c]:
            data['neighbours'][c].update(point_triangles[p])
        data['neighbours'][c].remove(c)
    return None

