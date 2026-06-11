import pyvista as pv
import numpy as np
from skimage.morphology import skeletonize
from scipy.spatial import KDTree

def gerar_dvr(dados_volume):
    grade = pv.ImageData()
    grade.dimensions = dados_volume.shape
    grade.spacing = (1.0, 1.0, 1.0)
    grade.origin = (0.0, 0.0, 0.0)
    grade.point_data["intensidades"] = dados_volume.flatten(order="F")
    return grade

def gerar_isosuperficie(dados_volume, grade=None):
    if grade is None:
        grade = gerar_dvr(dados_volume)
    
    malha = (grade.contour(isosurfaces=[60])
                  .extract_largest()
                  .decimate(target_reduction=0.7)
                  .smooth_taubin(n_iter=100))
    return malha

def gerar_esqueleto(volume_binario):
    matriz_esqueleto = skeletonize(volume_binario)
    coordenadas = np.argwhere(matriz_esqueleto).astype(np.float32)
    
    if len(coordenadas) == 0:
        return pv.PolyData(), matriz_esqueleto
        
    arvore = KDTree(coordenadas)
    pares = arvore.query_pairs(r=1.8)
    
    linhas = []
    for a, b in pares:
        linhas.extend([2, a, b])
        
    grafo = pv.PolyData(coordenadas)
    if linhas:
        grafo.lines = np.array(linhas)
        
    tubos = grafo.tube(radius=1.0)
    return tubos, matriz_esqueleto