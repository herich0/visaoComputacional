import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os, datetime

# Importa as novas funções
from funcoes.panorama import gerar_panoramica
from funcoes.gestos import ControladorGestos

class AppVisaoComputacional:
    def __init__(self, master):
        self.master = master
        master.title("Trabalho Prático - Visão Computacional")
        master.geometry("1200x720")
        master.configure(bg="#222")

        # Variáveis da Panorâmica
        self.caminho_img1 = None
        self.caminho_img2 = None
        self.img_resultado = None

        # Variáveis de Vídeo
        self.cap = None
        self.feed_active = False
        self.controlador_gestos = ControladorGestos()

        self.construir_interface()

    def construir_interface(self):
        main_frame = Frame(self.master, bg="#222")
        main_frame.pack(fill=BOTH, expand=True)

        # Painel Esquerdo (Controles)
        left_panel = Frame(main_frame, width=320, bg="#222")
        left_panel.pack(side=LEFT, fill=Y, padx=10, pady=10)
        left_panel.pack_propagate(False)

        # Abas
        notebook = ttk.Notebook(left_panel)
        notebook.pack(fill=BOTH, expand=True)

        self.tab_panorama = Frame(notebook, bg="#111")
        self.tab_gestos = Frame(notebook, bg="#111")

        notebook.add(self.tab_panorama, text="Panorâmica (Req 3a)")
        notebook.add(self.tab_gestos, text="Gestos (Req 3b)")

        self.construir_aba_panorama()
        self.construir_aba_gestos()

        # Painel Direito (Exibição de Imagens/Vídeo)
        right_panel = Frame(main_frame, bg="#333")
        right_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        self.label_tempo = Label(right_panel, text="Tempo de Processamento: -- s", bg="#333", fg="#0f0", font=("Arial", 12, "bold"))
        self.label_tempo.pack(pady=5)

        self.canvas_exibicao = Label(right_panel, bg="#000")
        self.canvas_exibicao.pack(expand=True, fill=BOTH, padx=5, pady=5)

    def construir_aba_panorama(self):
        f = self.tab_panorama
        
        # Botões para carregar imagens
        Label(f, text="Imagens de Entrada", bg="#111", fg="#fff", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.lbl_img1 = Label(f, text="Imagem 1: Nenhuma", bg="#111", fg="#ccc")
        self.lbl_img1.pack()
        Button(f, text="Carregar Imagem 1", width=25, command=lambda: self.carregar_imagem(1)).pack(pady=5)

        self.lbl_img2 = Label(f, text="Imagem 2: Nenhuma", bg="#111", fg="#ccc")
        self.lbl_img2.pack()
        Button(f, text="Carregar Imagem 2", width=25, command=lambda: self.carregar_imagem(2)).pack(pady=5)

        ttk.Separator(f, orient=HORIZONTAL).pack(fill=X, pady=15)

        # Seleção de Algoritmos
        Label(f, text="Configuração de Algoritmos", bg="#111", fg="#fff", font=("Arial", 12, "bold")).pack(pady=5)
        
        Label(f, text="Encontrar Pontos (Detector):", bg="#111", fg="#fff").pack()
        self.cb_detector = ttk.Combobox(f, values=["ORB", "SIFT"], state="readonly")
        self.cb_detector.current(0)
        self.cb_detector.pack(pady=5)

        Label(f, text="Correspondência (Matcher):", bg="#111", fg="#fff").pack()
        self.cb_matcher = ttk.Combobox(f, values=["BF", "FLANN"], state="readonly")
        self.cb_matcher.current(0)
        self.cb_matcher.pack(pady=5)

        ttk.Separator(f, orient=HORIZONTAL).pack(fill=X, pady=15)

        Button(f, text=" GERAR PANORÂMICA", width=25, bg="#007bff", fg="white", font=("Arial", 10, "bold"), command=self.executar_panorama).pack(pady=10)
        Button(f, text=" Salvar Resultado", width=25, command=self.salvar_resultado).pack(pady=5)

    def construir_aba_gestos(self):
        f = self.tab_gestos
        Label(f, text="Controle de Slides", bg="#111", fg="#fff", font=("Arial", 12, "bold")).pack(pady=10)
        
        Label(f, text="1. Abra uma apresentação (ex: PowerPoint)\n2. Ative a câmera abaixo\n3. Coloque a mão no quadrado azul\n4. Mova rápido para Direita/Esquerda", bg="#111", fg="#ccc", justify=LEFT).pack(pady=10)

        Button(f, text=" Iniciar Câmera / Gestos", width=25, bg="#28a745", fg="white", command=self.iniciar_camera).pack(pady=10)
        Button(f, text=" Parar Câmera", width=25, bg="#dc3545", fg="white", command=self.parar_camera).pack(pady=5)

    # --- Lógica Panorâmica ---
    def carregar_imagem(self, num):
        self.parar_camera()
        filepath = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
        if filepath:
            if num == 1:
                self.caminho_img1 = filepath
                self.lbl_img1.config(text=f"Imagem 1: {os.path.basename(filepath)}")
            else:
                self.caminho_img2 = filepath
                self.lbl_img2.config(text=f"Imagem 2: {os.path.basename(filepath)}")
            messagebox.showinfo("Sucesso", f"Imagem {num} carregada com sucesso!")

    def executar_panorama(self):
        if not self.caminho_img1 or not self.caminho_img2:
            messagebox.showwarning("Aviso", "Carregue as DUAS imagens primeiro!")
            return

        self.parar_camera()
        det = self.cb_detector.get()
        mat = self.cb_matcher.get()

        try:
            resultado, tempo = gerar_panoramica(self.caminho_img1, self.caminho_img2, det, mat)
            self.img_resultado = resultado
            
            # Atualiza UI
            self.label_tempo.config(text=f"Tempo de Processamento ({det}+{mat}): {tempo:.4f} s")
            self.exibir_imagem(resultado)

        except Exception as e:
            messagebox.showerror("Erro na Panorâmica", str(e))

    def salvar_resultado(self):
        if self.img_resultado is None:
            messagebox.showwarning("Aviso", "Nenhum resultado para salvar!")
            return
        os.makedirs("resultados", exist_ok=True)
        filename = f"panorama_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        path = os.path.join("resultados", filename)
        cv2.imwrite(path, self.img_resultado)
        messagebox.showinfo("Salvo", f"Imagem salva em:\n{path}")

    # --- Lógica de Câmera / Gestos ---
    def iniciar_camera(self):
        self.parar_camera()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a webcam.")
            return
        
        self.feed_active = True
        self.label_tempo.config(text="Controle Gestual Ativo (Lucas-Kanade)")
        self.atualizar_frame()

    def parar_camera(self):
        self.feed_active = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def atualizar_frame(self):
        if not self.feed_active or not self.cap:
            return

        ret, frame = self.cap.read()
        if ret:
            # Passa o frame para o controlador de gestos analisar
            frame_processado = self.controlador_gestos.processar_frame(frame)
            self.exibir_imagem(frame_processado)

        # Loop do Tkinter
        self.master.after(30, self.atualizar_frame)

    # --- Utilitário de Exibição ---
    def exibir_imagem(self, img_cv):
        try:
            # Converte BGR para RGB para o PIL
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            
            # Redimensiona mantendo proporção para caber na tela
            h_tela = self.canvas_exibicao.winfo_height() or 600
            w_tela = self.canvas_exibicao.winfo_width() or 800
            
            h_img, w_img = img_rgb.shape[:2]
            ratio = min(w_tela / w_img, h_tela / h_img)
            new_size = (int(w_img * ratio), int(h_img * ratio))
            
            img_resized = cv2.resize(img_rgb, new_size, interpolation=cv2.INTER_AREA)
            
            # Atualiza Canvas
            im_pil = Image.fromarray(img_resized)
            self.tk_img = ImageTk.PhotoImage(image=im_pil)
            self.canvas_exibicao.config(image=self.tk_img)
            self.canvas_exibicao.image = self.tk_img
        except Exception as e:
            print("Erro ao exibir imagem:", e)

if __name__ == "__main__":
    root = Tk()
    app = AppVisaoComputacional(root)
    root.mainloop()