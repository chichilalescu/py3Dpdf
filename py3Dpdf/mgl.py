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

import mathgl
import numpy as np

def triangulated_surface_to_mglGraph(
        graph = None,
        points = None,
        triangles = None,
        color = 'r'):
    npoints = points.shape[0]
    ntriangles = triangles.shape[0]
    uu = mathgl.mglData(npoints)
    vv = mathgl.mglData(npoints)
    ww = mathgl.mglData(npoints)
    for i in range(npoints):
        uu[i] = points[i, 0]
        vv[i] = points[i, 1]
        ww[i] = points[i, 2]
    tt = mathgl.mglData(ntriangles*3)
    for i in range(ntriangles):
        for j in range(3):
            tt[i*3 + j] = triangles[i, j]
    tt.Rearrange(3, ntriangles)
    graph.SetRange('x', uu, True)
    graph.SetRange('y', vv, True)
    graph.SetRange('z', ww, True)
    graph.TriPlot(tt, uu, vv, ww, color)
    return None

