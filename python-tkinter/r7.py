from tkinter import Label, Frame, Tk, Button, PhotoImage, Listbox
from tkinter import filedialog, Toplevel, Spinbox
from PIL import Image, ImageTk
from functools import partial


class EditorImagem(Tk):
    primeiro = None
    rotacio = None
    coordenadas = list()
    pontos = list()

    def __init__(self):
        Tk.__init__(self)
        self.geometry('600x600')
        self.painelFerramentas()
        self.quadroImagem()

    def painelFerramentas(self):
        self.frameL = Frame(self, width=40, bg='gray')
        self.frameL.pack(side='left', fill='y')
        self.disket = PhotoImage(file='../images/diskette.png').subsample(3)
        self.rotate = PhotoImage(file='../images/rotacionar.png').subsample(3)
        self.dimensao = PhotoImage(file='../images/dimension.png').subsample(3)
        self.recorte = PhotoImage(file='../images/recorte.png').subsample(3)
        self.cursor = PhotoImage(file='../images/cursor.png').subsample(3)
        self.open_ = PhotoImage(file='../images/open-folder-with-document.png').subsample(3)
        self.bt_disket = Button(
            self.frameL, image=self.disket, relief='flat',
            bg='gray', command=partial(self.salvar)
        )
        self.bt_rotate = Button(
            self.frameL, image=self.rotate, relief='flat',
            bg='gray', command=partial(self.checaModo, 'rotacionar')
        )
        self.bt_dimensao = Button(
            self.frameL, image=self.dimensao, relief='flat',
            bg='gray', command=partial(self.checaModo, 'dimensionar')
        )
        self.bt_recorte = Button(
            self.frameL, image=self.recorte, relief='flat', 
            bg='gray', command=partial(self.checaModo, 'recorte')
        )
        self.bt_cursor = Button(
            self.frameL, image=self.cursor, relief='flat', 
            bg='gray', command=partial(self.checaModo, 'normal')
        )
        self.bt_open = Button(
            self.frameL, image=self.open_, relief='flat', 
            bg='gray', command=partial(self.abrirImagem)
        )
        self.bt_disket.pack(pady=5, expand=True, fill='y')
        self.bt_open.pack(pady=5, expand=True, fill='y')
        self.bt_cursor.pack(pady=5, expand=True, fill='y')
        self.bt_rotate.pack(pady=5, expand=True, fill='y')
        self.bt_recorte.pack(pady=5, expand=True, fill='y')
        self.bt_dimensao.pack(pady=5, expand=True, fill='y')

    def checaModo(self, modo):
        if modo == 'rotacionar':
            self.rotacionar()
        elif modo == 'dimensionar':
            self.dimensionar()
        elif modo == 'recorte':
            self.recortar()

    def recortar(self):
        def pegaCoordenadas(coordenadas):
            if len(self.coordenadas) < 1:
                self.coordenadas.append(coordenadas.x)
            elif len(self.coordenadas) == 1:
                self.coordenadas.append(coordenadas.y)
            elif len(self.coordenadas) == 2:
                self.coordenadas.append(coordenadas.x)
            elif len(self.coordenadas) == 3:
                self.coordenadas.append(coordenadas.y)
            
            if len(self.coordenadas) == 4:                
                print(self.coordenadas)
                self.foto = self.foto.crop(self.coordenadas)
                self.img = ImageTk.PhotoImage(self.foto)
                self.quadro.config(image=self.img)
                self.quadro.unbind('<Button-1>')
                self.coordenadas.clear()
                return
        
        self.quadro.bind('<Button-1>', pegaCoordenadas)

    def dimensionar(self):
        def dimensionando():
            w = self.largura.get()
            h = self.altura.get()
            self.foto = self.foto.resize((int(w), int(h)))
            self.img = ImageTk.PhotoImage(self.foto)
            self.quadro.config(image=self.img)
            dim.destroy()

        dim = Toplevel(self.quadro)
        dim.geometry('200x100')
        self.largura = Spinbox(dim)
        self.altura = Spinbox(dim)
        self.bt = Button(dim, text='ok', command=dimensionando)
        self.bt.pack(pady=10)
        self.largura.pack()
        self.altura.pack()
        dim.mainloop()

    def rotacionar(self):
        if not self.rotacio:
            self.rotacionado = self.foto.transpose(Image.ROTATE_90)
            self.rotacio = True
        else:
            self.rotacionado = self.rotacionado.transpose(Image.ROTATE_90)
        self.img = ImageTk.PhotoImage(self.rotacionado)
        self.quadro.config(image=self.img)
        self.foto = self.rotacionado
        return


    def salvar(self):
        fp = filedialog.asksaveasfile(mode='w', defaultextension='.jpg', initialdir='~/')
        self.foto.save(fp)

    def quadroImagem(self):
        self.quadro = Label(self, bg='black')
        self.quadro.pack(expand=True, fill='both')

    def abrirImagem(self):
        self.infos = Label(self.quadro, fg='#fff', bg='#000')
        self.arquivo = filedialog.askopenfilename()
        self.quadro.update_idletasks()
        XX, YY = self.quadro.winfo_width(), self.quadro.winfo_height()
        self.foto = Image.open(self.arquivo)
        self.foto =self.foto.resize((XX, YY))
        infos = f'dim: {self.foto.size} form: {self.foto.format} modo: {self.foto.mode}'
        self.img = ImageTk.PhotoImage(self.foto)
        self.quadro.config(image=self.img)
        self.infos.config(text=infos)
        self.infos.pack(anchor='s', fill='x', expand=True)


app = EditorImagem()
app.mainloop()
