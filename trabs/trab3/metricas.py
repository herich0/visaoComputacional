import numpy as np
import scipy.ndimage as ndi
from skimage.measure import label, regionprops

def calcular_metricas(volume_binario, malha_isosuperficie, matriz_esqueleto):
    volume_malha = malha_isosuperficie.volume
    area_superficie = malha_isosuperficie.area
    
    compacidade = (area_superficie ** 1.5) / volume_malha if volume_malha > 0 else 0
    
    volume_rotulado = label(volume_binario)
    propriedades = regionprops(volume_rotulado)
    
    if propriedades:
        maior_regiao = max(propriedades, key=lambda r: r.area)
        L1, L2, L3 = maior_regiao.inertia_tensor_eigvals
        excentricidade = np.sqrt(1 - (L3 / L1)) if L1 > 0 else 0
    else:
        excentricidade = 0

    kernel = np.ones((3, 3, 3), dtype=int)
    convolucao = ndi.convolve(matriz_esqueleto.astype(int), kernel, mode='constant', cval=0)
    vizinhos = (convolucao * matriz_esqueleto) - matriz_esqueleto
    
    esqueleto_voxels = np.sum(matriz_esqueleto)
    terminacoes = np.sum(vizinhos == 1)
    caminhos = np.sum(vizinhos == 2)
    bifurcacoes = np.sum(vizinhos > 2)
    
    voxels_objeto = np.sum(volume_binario)
    densidade = (esqueleto_voxels / voxels_objeto) * 100 if voxels_objeto > 0 else 0

    metricas_esqueleto = {
        "Comprimento Total (Voxels)": esqueleto_voxels,
        "Terminacoes": terminacoes,
        "Nos de Bifurcacao": bifurcacoes,
        "Voxels de Conexao": caminhos,
        "Taxa de Compactacao (%)": densidade
    }

    return {
        "Volume da Malha": volume_malha,
        "Area de Superficie": area_superficie,
        "Compacidade": compacidade,
        "Excentricidade": excentricidade,
        "Esqueleto": metricas_esqueleto
    }