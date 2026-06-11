import pyvista as pv
import numpy as np

# 1. CRIAÇÃO DA GEOMETRIA
# Resolução 10x10 significa 100 células e 121 pontos
malha = pv.Plane(i_resolution=10, j_resolution=10)

# 2. INJEÇÃO DE DADOS NOS VÉRTICES (POINT DATA)
# Vamos pegar a coordenada X de cada vértice para criar um gradiente perfeito.
# Como a variável é contínua, o PyVista fará a interpolação.
coordenadas_x = malha.points[:, 0] # Coluna 0 (X)   Coluna 1 (Y)   Coluna 2 (Z)
malha.point_data["Meu_Gradiente_Continuo"] = coordenadas_x

# 3. INJEÇÃO DE DADOS NAS CÉLULAS (CELL DATA)
# Vamos simular uma segmentação (ex: 4 materiais diferentes identificados pelo algoritmo).
# Geramos 100 números inteiros aleatórios (de 0 a 3), um para cada face.
classes_aleatorias = np.random.randint(0, 4, malha.n_cells)
malha.cell_data["Minhas_Classes_Discretas"] = classes_aleatorias

# 4. RENDERIZAÇÃO LADO A LADO (SUBPLOTS)
plotter = pv.Plotter(shape=(1, 2), window_size=[1000, 500])

# --- Janela da Esquerda (Point Data) ---
plotter.subplot(0, 0)
plotter.add_text("Point Data\n(Interpolacao Suave entre Vertices)", font_size=12)
# O PyVista detecta automaticamente que a string abaixo está no dicionário point_data
plotter.add_mesh(malha, scalars="Meu_Gradiente_Continuo", cmap="viridis", show_edges=True)
plotter.camera_position = 'xy' # Trava a câmera olhando de cima para baixo

# --- Janela da Direita (Cell Data) ---
plotter.subplot(0, 1)
plotter.add_text("Cell Data\n(Valor Chapado por Face)", font_size=12)
# O PyVista detecta automaticamente que a string abaixo está no dicionário cell_data
# Usamos o mapa de cores 'Set1', que é ideal para categorias discretas
plotter.add_mesh(malha, scalars="Minhas_Classes_Discretas", cmap="Set1", show_edges=True)
plotter.camera_position = 'xy'

# Exibe o resultado final
plotter.show()