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
        data.append(ip)
    return data

