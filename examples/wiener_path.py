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

#! /usr/bin/env python2

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
    asy_curves = []
    for i in range(W.shape[1]):
        asy_curves.append(py3Dpdf.curve3D_to_asy(W[:, i], arrow_on = True))
    py3Dpdf.asy_to_pdf(asy_objects = asy_curves)
    return None

if __name__ == '__main__':
    main()

