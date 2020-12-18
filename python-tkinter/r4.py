from tkinter import Tk, Text, Menu, BooleanVar, Label, font


class MyApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Notepad')
        self.geometry('700x500+200+100')
        self.tx = Text(self, font=('Consolas', 11, 'roman'))
        self.menuBar()
        self.statusBar()

    def menuBar(self):
        self.menu = Menu(self)
        self.arquivo = Menu(self.menu, tearoff=0)
        self.arquivo.add_command(label='Novo', accelerator='Ctrl+N')
        self.arquivo.add_command(label='Nova Janela', accelerator='Ctrl+Shift+N')
        self.arquivo.add_command(label='Abrir', accelerator='Ctrl+O')
        self.arquivo.add_command(label='Salvar', accelerator='Ctrl+S')
        self.arquivo.add_command(label='Salvar Como', accelerator='Ctrl+Shift+S')
        self.arquivo.add_separator()
        self.arquivo.add_command(label='Configurar pagina')
        self.arquivo.add_command(label='Imprimir', accelerator='Ctrl+P')
        self.menu.add_cascade(label='Arquivo', menu=self.arquivo)
        self.editar = Menu(self.menu, tearoff=0)
        self.editar.add_command(label='Desfazer', accelerator='Ctrl+Z')
        self.editar.add_separator()
        self.editar.add_command(label='Recortar', accelerator='Ctrl+X')
        self.editar.add_command(label='Copiar', accelerator='Ctrl+C')
        self.editar.add_command(label='Colar', accelerator='Ctrl+V')
        self.editar.add_command(label='Excluir', accelerator='Del')
        self.editar.add_separator()
        self.editar.add_command(label='Buscar com o Bing', accelerator='Ctrl+E')
        self.editar.add_command(label='Localizar', accelerator='Ctrl+F')
        self.editar.add_command(label='Localizarf Próxima', accelerator='F3')
        self.editar.add_command(label='Localizar anterior', accelerator='Shift+F3')
        self.editar.add_command(label='Substituir', accelerator='Ctrl+H')
        self.editar.add_command(label='Ir para', accelerator='Ctrl+G')
        self.editar.add_separator()
        self.editar.add_command(label='Selecionar tudo', accelerator='Ctrl+A')
        self.editar.add_command(label='Hora/Data', accelerator='F5')
        self.menu.add_cascade(label='Editar', menu=self.editar)
        self.formatar = Menu(self.menu, tearoff=0)
        self.formatar.add_command(label='Quebra automatica de linha')
        self.formatar.add_command(label='Fonte...')
        self.menu.add_cascade(label='Formatar', menu=self.formatar)
        self.exibir = Menu(self.menu, tearoff=0)
        self.subExibir = Menu(self.exibir, tearoff=0)
        self.subExibir.add_command(label='Ampliar')
        self.subExibir.add_command(label='Reduzir')
        self.subExibir.add_command(label='Restaura zoom padrão')
        self.exibir.add_cascade(label='Zoom', menu=self.subExibir)
        var = BooleanVar()
        var.set(1)
        self.exibir.add_checkbutton(
            label='Barra de status', onvalue=1, offvalue=0, variable=var
        )
        self.menu.add_cascade(label='Exibir', menu=self.exibir)
        self.ajuda = Menu(self.menu, tearoff=0)
        self.ajuda.add_command(label='Exibir ajuda')
        self.ajuda.add_command(label='Enviar comentarios')
        self.ajuda.add_separator()
        self.ajuda.add_command(label='Sobre o bloco de notas')
        self.menu.add_cascade(label='Ajuda', menu=self.ajuda)
        self.config(menu=self.menu)
        self.tx.pack(expand=True, fill='both')

    def statusBar(self):
        self.statusBar_ = Label(
            self,
            text=f'{" "*20} |Ln 1, Col 1 {" "*5}| 100% |{" "*5} Windows (CRLF) |{" "*5} UTF-8', 
            font=('Consolas', 11)
        )
        self.statusBar_.pack(side='bottom')

MyApp().mainloop()