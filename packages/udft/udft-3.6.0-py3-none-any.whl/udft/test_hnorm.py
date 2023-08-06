#!/usr/bin/env python3

import imageio
import numpy as np

import udft

sat = np.moveaxis(
    imageio.imread("/home/forieux/areas/ue/signal-dlmp/tps/saturne.png"), 2, 0
)

imshape = sat.shape[1:]
N = np.prod(imshape)
sqrtN = np.sqrt(np.prod(imshape))

satf = np.fft.fft2(sat)
satuf = udft.dft2(sat)
saturf = udft.rdft2(sat)

print("d norm:", a := np.sum(np.abs(sat) ** 2, axis=(1, 2)))
print("f norm / N:", b := np.sum(np.abs(satf) ** 2, axis=(1, 2)) / N)
print("uf norm:", b := np.sum(np.abs(satuf) ** 2, axis=(1, 2)))
print("urf norm:", udft.hnorm(saturf, imshape) ** 2)
print("d[0] norm:", a := np.sum(np.abs(sat[0]) ** 2))
print("urf[0] norm:", udft.hnorm(saturf[0], imshape) ** 2)
