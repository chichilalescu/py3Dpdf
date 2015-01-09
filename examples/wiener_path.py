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

def get_wiener_paths(
        nsteps = 2**7,
        ntraj = 2**4):
    dW = np.random.randn(nsteps, ntraj, 3)
    W = np.zeros((nsteps+1, ntraj, 3), dtype = dW.dtype)
    W[1:] = np.cumsum(dW, axis = 0)
    return W

def main():
    W = get_wiener_paths()
    if py3Dpdf.found_asymptote:
        asy_curves = []
    if py3Dpdf.found_mathgl:
        g = py3Dpdf.npGraph()
        g.set_limits(points = {'x': [W[..., 0].min(), W[..., 0].max()],
                               'y': [W[..., 1].min(), W[..., 1].max()],
                               'z': [W[..., 2].min(), W[..., 2].max()]})
    for i in range(W.shape[1]):
        if py3Dpdf.found_asymptote:
            asy_curves.append(py3Dpdf.curve3D_to_asy(W[:, i], arrow_on = True))
        if py3Dpdf.found_mathgl:
            g.curve(
                W[:, i],
                style = (py3Dpdf.rgb_to_mglColor(0.3, 0.1, 0.9) +
                         'A'))
    if py3Dpdf.found_asymptote:
        py3Dpdf.asy_to_pdf(
            asy_objects = asy_curves,
            figname = 'asy_wp_test')
    if py3Dpdf.found_mathgl:
        g.WritePNG('mgl_wp_test.png')
        g.WritePRC('mgl_wp_test.prc')
    return None

if __name__ == '__main__':
    main()

