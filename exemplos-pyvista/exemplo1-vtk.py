import vtk

# 1. SOURCE: Cria a geometria matemática (O Dado)
cylinder = vtk.vtkCylinderSource()
cylinder.SetResolution(50)
cylinder.Update()

# 2. MAPPER: Traduz a geometria matemática para primitivas gráficas
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(cylinder.GetOutput())

# 3. ACTOR: A entidade física na cena (adiciona cor, posição, rotação)
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Cor vermelha (RGB de 0.0 a 1.0)

# 4. RENDERER: O motor visual que gerencia a cena, luzes e câmera
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)  # Fundo azul escuro

# 5. RENDER WINDOW: A janela do sistema operacional
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)
render_window.SetWindowName("Cilindro - VTK")

# 6. INTERACTOR: Captura eventos de mouse e teclado para girar a câmera
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Inicia o loop de renderização
render_window.Render()
interactor.Start()