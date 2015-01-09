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

# inspired by Amit Aides' pyasymp2.py, found at
# http://comments.gmane.org/gmane.comp.python.enthought.devel/31471


import numpy as np
import random
import string
import subprocess

def curve3D_to_asy(
        points,
        color = (1, 0, 0),
        arrow_on = False,
        spline_on = False):
    # vertices
    asy_txt = 'path3 p=' + str(tuple(points[0]))
    # store points
    connector = '--'
    if spline_on:
        connector = '..'
    for i in range(1, points.shape[0]):
        asy_txt += connector + str(tuple(points[i]))
    asy_txt += ';\n'
    asy_txt += ('draw(p, ' +
                'rgb{0}, '.format(str(color)))
    if arrow_on:
        asy_txt += 'arrow = Arrow3, '
    asy_txt += ('render = render(compression = High, merge = true))' +
                ';\n')
    return asy_txt

def triangulated_surface_to_plain_asy(
        points,
        triangles,
        color = (1, 0, 0)):
    # vertices
    def finite_prec_triple(values):
        return '({0:.7e},{1:.7e},{2:.7e})'.format(values[0], values[1], values[2])
    asy_txt = 'triple[] V={' + finite_prec_triple(points[0])
    for i in range(1, points.shape[0]):
        asy_txt += ',' + finite_prec_triple(points[i])
    asy_txt += '};\n'
    # triface function
    asy_txt += ('guide3 triface_(int i, int j, int k)\n' +
                '{\n' +
                'guide3 gh;\n' +
                'gh = V[i]--V[j]--V[k]--cycle;\n' +
                'return gh;\n' +
                '}\n')
    # triangles
    asy_txt += 'path3[] T={triface_' + str(tuple(triangles[0]))
    # store triangles
    for i in range(1, triangles.shape[0]):
        asy_txt += ',triface_' + str(tuple(triangles[i]))
    asy_txt += '};\n'
    asy_txt += ('draw(surface(T), ' +
                'rgb{0}, '.format(str(color)) +
                'render(compression = Low, merge = true))' +
                ';\n')
    return asy_txt

def triangulated_surface_to_obj_asy(
        points,
        triangles,
        color = (1, 0, 0),
        obj_file = None):
    # first, generate object file
    if type(obj_file == None):
        obj_file = (''.join(random.choice(string.ascii_lowercase +
                                          string.ascii_uppercase +
                                          string.digits)
                    for _ in range(8)) +
                    '.obj')
    with open(obj_file, 'w') as ofile:
        for i in range(points.shape[0]):
            ofile.write('v {0:.6f} {1:.6f} {2:.6f}\n'.format(
                                                          points[i, 0],
                                                          points[i, 1],
                                                          points[i, 2]))
        ofile.write('\n')
        triangles += 1
        for i in range(triangles.shape[0]):
            ofile.write('f {0} {1} {2}\n'.format(triangles[i, 0],
                                                 triangles[i, 1],
                                                 triangles[i, 2]))
        ofile.write('\n')
    return ('draw(obj("' + obj_file + '", ' +
            'rgb{0}))'.format(str(color)) +
            ';\n')

def triangulated_surface_to_asy(
        points,
        triangles,
        color = (1, 0, 0),
        plain_asy = True,
        obj_file = None):
    if plain_asy:
        return triangulated_surface_to_plain_asy(
                points,
                triangles,
                color)
    else:
        return triangulated_surface_to_obj_asy(
                points,
                triangles,
                color,
                obj_file)

def asy_to_pdf(
        figname = 'tst',
        asy_objects = [],
        keep_tex = False):
    with open(figname + '.asy', 'w') as outfile:
        outfile.write(
            'import three;\n' +
            'import graph3;\n' +
            'import obj;\n' +
            'size(20cm);\n' +
            '//currentprojection=perspective(250,-250,250);\n' +
            'currentlight=Viewport;\n\n')
        for obj in asy_objects:
            outfile.write(obj)
    command = 'asy -render 1 '
    if keep_tex:
        command += '-keep -tex pdflatex '
    else:
        command += '-f pdf '
    command += figname
    subprocess.Popen(
        command,
        shell=True).wait()
    return None

