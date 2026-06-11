import tkinter as tk
from tkinter import messagebox, ttk
import pyvista as pv
from processamento import carregar_e_limpar
from visualizacao import gerar_dvr, gerar_isosuperficie, gerar_esqueleto
from metricas import calcular_metricas

class AppVisao:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho Pratico 3 - Visao Computacional")
        self.root.geometry("450x400")
        
        self.pasta = tk.StringVar(value="b0207")
        self.dados = {}
        
        self.montar_ui()
        self.processar()

    def montar_ui(self):
        f_amostra = ttk.LabelFrame(self.root, text=" Selecao de Amostra ")
        f_amostra.pack(fill="x", padx=15, pady=10)
        
        cb = ttk.Combobox(f_amostra, textvariable=self.pasta, values=["b0207", "b0309"], state="readonly")
        cb.pack(fill="x", pady=5)
        cb.bind("<<ComboboxSelected>>", lambda e: self.processar())
        
        f_acoes = ttk.LabelFrame(self.root, text=" Visualizacoes e Metricas ")
        f_acoes.pack(fill="both", expand=True, padx=15, pady=5)
        
        ttk.Button(f_acoes, text="DVR", command=self.show_dvr).pack(fill="x", pady=4)
        ttk.Button(f_acoes, text="Isosuperficie", command=self.show_iso).pack(fill="x", pady=4)
        ttk.Button(f_acoes, text="Esqueleto", command=self.show_esq).pack(fill="x", pady=4)
        ttk.Button(f_acoes, text="Janela Dividida", command=self.show_split).pack(fill="x", pady=4)
        ttk.Button(f_acoes, text="Calcular Metricas", command=self.show_metricas).pack(fill="x", pady=4)
        
        self.status = ttk.Label(self.root, text="Pronto.", relief="sunken", anchor="w")
        self.status.pack(fill="x", side="bottom", ipady=2)

    def processar(self):
        p = self.pasta.get()
        self.status.config(text=f"Processando e indexando {p}...")
        self.root.update()
        
        try:
            vol_xyz, vol_bin = carregar_e_limpar(p)
            dvr = gerar_dvr(vol_xyz)
            iso = gerar_isosuperficie(vol_xyz, dvr)
            esq, mat_esq = gerar_esqueleto(vol_bin)
            
            self.dados = {
                "dvr": dvr, "iso": iso, "esq": esq, 
                "vol_bin": vol_bin, "mat_esq": mat_esq
            }
            self.status.config(text=f"{p} carregado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.status.config(text="Erro ao carregar dados.")

    def verificar_dados(self):
        if not self.dados:
            messagebox.showwarning("Aviso", "Os dados ainda não foram processados.")
            return False
        return True

    def show_dvr(self):
        if not self.verificar_dados(): return
        p = pv.Plotter(window_size=[800, 600])
        p.set_background("black")
        p.add_volume(self.dados["dvr"], scalars="intensidades", cmap="gray", opacity="linear")
        p.add_axes()
        p.show()

    def show_iso(self):
        if not self.verificar_dados(): return
        p = pv.Plotter(window_size=[800, 600])
        p.set_background("white")
        p.add_mesh(self.dados["iso"], color="tan", smooth_shading=True)
        p.add_axes()
        p.show()

    def show_esq(self):
        if not self.verificar_dados(): return
        p = pv.Plotter(window_size=[800, 600])
        p.set_background("white")
        p.add_mesh(self.dados["esq"], color="red", smooth_shading=True)
        p.add_axes()
        p.show()

    def show_split(self):
        if not self.verificar_dados(): return
        p = pv.Plotter(shape=(1, 3), window_size=[1400, 600])
        
        p.subplot(0, 0)
        p.set_background("black")
        p.add_text("1. DVR", font_size=10)
        p.add_volume(self.dados["dvr"], scalars="intensidades", cmap="gray", opacity="linear")
        
        p.subplot(0, 1)
        p.set_background("white")
        p.add_text("2. Isosuperficie", font_size=10, color="black")
        p.add_mesh(self.dados["iso"], color="tan", smooth_shading=True)
        
        p.subplot(0, 2)
        p.set_background("white")
        p.add_text("3. Esqueleto e Isosuperficie", font_size=10, color="black")
        p.add_mesh(self.dados["iso"], color="tan", opacity=0.3, show_edges=False)
        p.add_mesh(self.dados["esq"], color="red", smooth_shading=True)
        
        p.link_views()
        p.show()

    def show_metricas(self):
        if not self.verificar_dados(): return
        m = calcular_metricas(self.dados["vol_bin"], self.dados["iso"], self.dados["mat_esq"])
        
        texto = f"Amostra: {self.pasta.get()}\n" + "-"*40 + "\n\n"
        for k, v in m.items():
            if k != "Esqueleto":
                texto += f"{k}: {v:.4f}\n" if isinstance(v, float) else f"{k}: {v}\n"
        
        texto += "\nMetricas do Esqueleto:\n"
        for k, v in m["Esqueleto"].items():
            texto += f"{k}: {v:.4f}\n" if isinstance(v, float) else f"{k}: {v}\n"
            
        messagebox.showinfo("Metricas Calculadas", texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppVisao(root)
    root.mainloop()