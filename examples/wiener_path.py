import numpy as np
import py2asy

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
        asy_curves.append(py2asy.curve3D_to_asy(W[:, i], arrow_on = True))
    py2asy.asy_to_pdf(asy_objects = asy_curves)
    return None

if __name__ == '__main__':
    main()

