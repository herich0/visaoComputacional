import pyvista as pv
from pyvista import examples

# 1. CARREGAMENTO (O Dado Bruto)
# Gera um volume 3D (ImageData) com valores escalares espalhados.
volume = pv.Wavelet()
#volume = examples.download_full_head()

# 2. LIMIARIZAÇÃO (.threshold)
# Remove o "ruído" do fundo.
# Mantém apenas dados com valor de densidade entre 120 e 255.
# (Transforma o ImageData em um UnstructuredGrid)
volume_limpo = volume.threshold([120, 255])

# 3. EXTRAÇÃO DA SUPERFÍCIE (.contour)
# (O resultado passa a ser um PolyData - uma malha de triângulos)
malha_bruta = volume_limpo.contour(isosurfaces=[150])

# 4. COMPRESSÃO GEOMÉTRICA (.decimate)
# Removendo 80% (0.8) dos triângulos da malha bruta.
malha_leve = malha_bruta.decimate(target_reduction=0.8)

# 5. SUAVIZAÇÃO (.smooth vs .smooth_taubin)
malha_smooth_comum = malha_leve.smooth(n_iter=200)
malha_taubin = malha_leve.smooth_taubin(n_iter=200)

# 6. INSPEÇÃO INTERNA (.clip)
# Pegamos a malha final (Taubin) e fatiamos no eixo X.
# 'normal=-x' significa que cortamos fora o lado negativo do eixo.
malha_fatiada = malha_taubin.clip(normal='-x')

# 7. RENDERIZAÇÃO COMPARATIVA
# Vamos criar uma tela dividida em 4 quadrantes (2x2)
plotter = pv.Plotter(shape=(2, 2), window_size=[1200, 800])

# Quadrante 1 (Topo-Esquerda): A malha bruta recém extraída
plotter.subplot(0, 0)
plotter.add_text("1. Contour (Malha Bruta)", font_size=11)
plotter.add_mesh(malha_bruta, color="tan", show_edges=True)

# Quadrante 2 (Topo-Direita): A malha ideal (Leve e com volume correto)
plotter.subplot(0, 1)
plotter.add_text("2. Decimate + Taubin\n(Liso, leve e com volume preservado)", font_size=11)
plotter.add_mesh(malha_taubin, color="tan", show_edges=True)

# Quadrante 3 (Base-Esquerda): O perigo do Smooth comum
plotter.subplot(1, 0)
plotter.add_text("3. Smooth Laplaciano Comum\n(O objeto encolheu!)", font_size=11)
plotter.add_mesh(malha_smooth_comum, color="tan", show_edges=True)

# Quadrante 4 (Base-Direita): A inspeção interna com o corte
plotter.subplot(1, 1)
plotter.add_text("4. Clip (Inspecao Interna)", font_size=11)
# Aqui desliguei as arestas (show_edges=False) para vermos o interior sólido
plotter.add_mesh(malha_fatiada, color="tan", show_edges=False)

# O link_views() trava a câmera das 4 janelas juntas. Se você girar uma, gira todas!
plotter.link_views()

plotter.show()