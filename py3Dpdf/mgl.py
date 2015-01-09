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

def nparray_to_mglData(a):
    aa = mathgl.mglData(a.size)
    b = a.reshape(-1)
    for i in range(b.size):
        aa[i] = b[i]
    if len(a.shape) > 1:
        #  I'm not sure this makes sense for many dimensions,
        # but this is what I need to do for the triangles, so
        # I'll worry about the general case later.
        aa.Rearrange(*a.shape[::-1])
    return aa

def rgb_to_mglColor(rgb = (1, 0, 0)):
    # see http://mathgl.sourceforge.net/doc_en/Line-styles.html#index-Arrows for details
    return '{{x{0:0>2x}{1:0>2x}{2:0>2x}}}'.format(int(rgb[0]*255),int(rgb[1]*255), int(rgb[2]*255))

class npGraph(mathgl.mglGraph):
    def __init__(self):
        super(npGraph, self).__init__()
        self.empty = True
        return None
    def triangulated_surface(
            self,
            points = None,
            triangles = None,
            style = 'r'):
        uu = nparray_to_mglData(points[:, 0])
        vv = nparray_to_mglData(points[:, 1])
        ww = nparray_to_mglData(points[:, 2])
        tt = nparray_to_mglData(triangles)
        self.set_limits({'x': uu,
                         'y': vv,
                         'z': ww})
        self.empty = False
        return self.TriPlot(tt, uu, vv, ww, style)
    def curve(
            self,
            points = None,
            style = 'r'):
        u = nparray_to_mglData(points[:, 0])
        v = nparray_to_mglData(points[:, 1])
        w = nparray_to_mglData(points[:, 2])
        self.set_limits({'x': u,
                         'y': v,
                         'z': w})
        self.empty = False
        return self.Plot(u, v, w, style)
    def set_limits(
            self,
            points = {}):
        for coord in points.keys():
            self.SetRange(coord, points[coord], not self.empty)
        return None

