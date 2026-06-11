import pyvista as pv

volume = pv.Wavelet()

malha = (volume.threshold([120, 255])
               .contour(isosurfaces=[150])
               .decimate(target_reduction=0.8)
               .smooth_taubin(n_iter=200)
               .clip(normal='-x'))

plotter = pv.Plotter(window_size=[800, 600])
plotter.title = "PyVista"
plotter.add_mesh(malha, color="tan", show_edges=True)
plotter.show()