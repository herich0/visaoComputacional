import os
import glob
import numpy as np
import imageio.v3 as iio
from scipy.ndimage import gaussian_filter

def carregar_e_limpar(caminho_pasta):
    padrao = os.path.join(caminho_pasta, '*.png')
    arquivos = sorted(glob.glob(padrao))
    
    if not arquivos:
        padrao = os.path.join(caminho_pasta, '*.tif*')
        arquivos = sorted(glob.glob(padrao))

    img_teste = iio.imread(arquivos[0])
    cy, cx = img_teste.shape[0] // 2, img_teste.shape[1] // 2
    Y, X = np.ogrid[:img_teste.shape[0], :img_teste.shape[1]]
    distancia = np.sqrt((X - cx)**2 + (Y - cy)**2)
    raio = min(cx, cy) * 0.85

    fatias = []
    for arq in arquivos:
        img = iio.imread(arq)
        if img.ndim == 3:
            img = img[:, :, 0]
        
        if img[0, 0] > 127:
            img = np.max(img) - img
            
        img[distancia > raio] = 0
        img[img < 45] = 0
        fatias.append(img)

    volume = np.array(fatias)
    volume[:5, :, :] = 0
    volume[-5:, :, :] = 0

    volume_suave = gaussian_filter(volume, sigma=1.5)
    volume_xyz = np.transpose(volume_suave, (2, 1, 0))
    
    volume_binario = volume_xyz > 60
    
    return volume_xyz, volume_binario