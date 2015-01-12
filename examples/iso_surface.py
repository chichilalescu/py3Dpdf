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

from scipy.interpolate import interpn

from base import get_turbulent_scalar

def main(
        n = 32,
        kmax = None):
    x, y, z, f = get_turbulent_scalar(n = n)
    s = get_turbulent_scalar(n = n)[3]
    grid1D = np.linspace(-np.pi, np.pi, n, endpoint = False)
    data = py3Dpdf.tvtk_tools.get_isosurface_data(
        field = f,
        x1Dgrid = grid1D,
        y1Dgrid = grid1D,
        z1Dgrid = grid1D,
        values = [0.0])
    scals = interpn(
        (grid1D, grid1D, grid1D),
        s,
        data[0]['points'],
        bounds_error = False,
        fill_value = 0.0)
    if py3Dpdf.found_asymptote:
        asy_txt = py3Dpdf.triangulated_surface_to_asy(
            data[0]['points'],
            data[0]['triangles'])
        py3Dpdf.asy_to_pdf(
            asy_objects = [asy_txt],
            figname = 'asy_iso_test')
    if py3Dpdf.found_mathgl:
        gr = py3Dpdf.npGraph()
        gr.set_limits(
            points = {'x': grid1D,
                      'y': grid1D,
                      'z': grid1D})
        gr.Light(True)
        gr.triangulated_surface(
            points = data[0]['points'],
            triangles = data[0]['triangles'],
            scalars = scals,
            values = np.linspace(scals.min(), scals.max(), 20),
            style = '')
        gr.WritePNG('mgl_iso_test.png')
        gr.WritePRC('mgl_iso_test.prc')
    return None

if __name__ == '__main__':
    main()

