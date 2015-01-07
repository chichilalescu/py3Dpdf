# inspired by Amit Aides' pyasymp2.py, found at
# http://comments.gmane.org/gmane.comp.python.enthought.devel/31471


import numpy as np
import subprocess

def curve3D_to_asy(
        points,
        color = (1, 0, 0)):
    # vertices
    asy_txt = ('real[] x;\n' +
               'real[] y;\n' +
               'real[] z;\n')
    # store points
    for i in range(points.shape[0]):
        asy_txt += ('x[{0}] = {1};\n'.format(i, points[i, 0]) +
                    'y[{0}] = {1};\n'.format(i, points[i, 1]) +
                    'z[{0}] = {1};\n'.format(i, points[i, 2]))
    asy_txt += ('draw(graph(x,y,z), ' +
                'rgb{0}, '.format(str(color)) +
                'render(compression = High, merge = true))' +
                ';\n')
    return asy_txt

def triangulated_surface_to_asy(
        points,
        triangles,
        color = (1, 0, 0)):
    # vertices
    asy_txt = 'triple[] V;\n'
    # triface function
    asy_txt += ('guide3 triface_(int i, int j, int k)\n' +
                '{\n' +
                'guide3 gh;\n' +
                'gh = V[i]--V[j]--V[k]--cycle;\n' +
                'return gh;\n' +
                '}\n')
    # triangles
    asy_txt += 'path3[] T;\n'
    # store points
    for i in range(points.shape[0]):
        asy_txt += 'V[{0}] = {1};\n'.format(i, str(tuple(points[i])))
    # store triangles
    for i in range(triangles.shape[0]):
        asy_txt += 'T[{0}] = triface_{1};\n'.format(i, str(tuple(triangles[i])))
    asy_txt += ('draw(surface(T), ' +
                'rgb{0}, '.format(str(color)) +
                'render(compression = High, merge = true))' +
                ';\n')
    return asy_txt

def asy_to_pdf(
        figname = 'tst',
        asy_objects = []):
    with open(figname + '.asy', 'w') as outfile:
        outfile.write(
            "import three;\n" +
            "import graph3;\n" +
            "size(20cm);\n" +
            "//currentprojection=perspective(250,-250,250);\n" +
            "currentlight=Viewport;\n\n")
        for obj in asy_objects:
            outfile.write(obj)
    subprocess.Popen(
        'asy -render 1 -f pdf ' + figname,
        shell=True).wait()
    return None

