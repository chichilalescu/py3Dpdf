#! /usr/bin/env python2
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

import numpy as np
import py3Dpdf
import py3Dpdf.tvtk_tools

from base import get_turbulent_scalar

def main():
    fx = get_turbulent_scalar()[3]
    fy = get_turbulent_scalar()[3]
    x, y, z, fz = get_turbulent_scalar()
    fx /= 10
    fy /= 10
    fz /= 10
    #fx[:] = 0
    #fy[:] = x
    #fz[:] = 0
    grid1D = np.linspace(
        -np.pi, np.pi,
        fx.shape[0],
        endpoint = False)
    data = py3Dpdf.tvtk_tools.get_isosurface_data(
        field = fx,
        x1Dgrid = grid1D,
        y1Dgrid = grid1D,
        z1Dgrid = grid1D,
        values = [0.0])
    if py3Dpdf.found_mathgl:
        # first, vector field
        gr = py3Dpdf.npGraph()
        gr.set_limits(
            points = {'x': grid1D,
                      'y': grid1D,
                      'z': grid1D})
        mglgrid = py3Dpdf.array_to_mglData(grid1D)
        ffx = py3Dpdf.array_to_mglData(fx)
        ffy = py3Dpdf.array_to_mglData(fy)
        ffz = py3Dpdf.array_to_mglData(fz)
        gr.Axis('xyz')
        gr.Box()
        gr.Label('x', 'x', 0)
        gr.Label('y', 'y', 0)
        gr.Label('z', 'z', 0)
        gr.Vect(mglgrid,
                mglgrid,
                mglgrid,
                ffx,
                ffy,
                ffz,
                '<',
                "value 1; meshnum 8")
        gr.Legend()
        gr.WritePNG('mgl_vect_test.png')
        gr.WritePRC('mgl_vect_test.prc')
        # second, isosurface with normals
        gr.Clf()
        gr.triangulated_surface(
            points = data[0]['points'],
            triangles = data[0]['triangles'])
        mglcx   = py3Dpdf.array_to_mglData(data[0]['centers'][:, 0])
        mglcy   = py3Dpdf.array_to_mglData(data[0]['centers'][:, 1])
        mglcz   = py3Dpdf.array_to_mglData(data[0]['centers'][:, 2])
        mglgx   = py3Dpdf.array_to_mglData(data[0]['gradients'][:, 0])
        mglgy   = py3Dpdf.array_to_mglData(data[0]['gradients'][:, 1])
        mglgz   = py3Dpdf.array_to_mglData(data[0]['gradients'][:, 2])
        gr.Traj(
            mglcx, mglcy, mglcz,
            mglgx, mglgy, mglgz,
            '<',
            "value 0.1")
        gr.WritePNG('mgl_traj_test.png')
        gr.WritePRC('mgl_traj_test.prc')
    return None

if __name__ == '__main__':
    main()

