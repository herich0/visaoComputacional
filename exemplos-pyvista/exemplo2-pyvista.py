import pyvista as pv

# 1. SOURCE: O PyVista possui geometrias prontas que já são objetos 3D
cilindro = pv.Cylinder(resolution=50)

# 2. RENDERER / INTERACTOR: O objeto Plotter gerencia toda a janela e a câmera
plotter = pv.Plotter(window_size=[800, 600])
plotter.title = "Cilindro - PyVista"

# 3. MAPPER / ACTOR: O método add_mesh encapsula a criação do ator e materiais
plotter.add_mesh(cilindro, color="red", smooth_shading=True)

# Configura o fundo e inicia o loop
plotter.set_background(color=[0.1, 0.2, 0.4])
plotter.show()