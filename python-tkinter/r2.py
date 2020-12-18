from tkinter import Text, Tk, Listbox, Label, filedialog


class Texto(Text):
    def __init__(self, parent):
        self.mastere = parent
        Text.__init__(self, master=self.mastere)
        self.config(insertbackground='#fff')
        self.bind('<Control_L><Shift_L><S>', self.saveAs)
        self.bind('<Control_L><s>', self.save)

    def saveAs(self, save):
        types = [
            ('Todos', '*.*'),
            ('Python', ('*.py', '*.pyw')),
            ('Texto', '*.txt')
        ]
        self.nome = filedialog.asksaveasfile(
            mode='w', title='salvar como', filetypes=types
        )
        self.nome.write(self.get(0.1, 'end'))

    def save(self):
        with open(self.nome.name, 'w', encoding='utf-8') as file:
            file.write(self.get(0.1, 'end'))       


# janela ====================================================

class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.state('zoomed')
        self.config(bg='#282a36')
        self.bind('<KeyPress>', self.manipula)
        self.tx = Texto(self)
        self.tx.bind('<Tab>', self.tabSpace)
        self.linhas = Listbox(
            self, width=10, bg='#21222c', fg='#ffffff', bd=0
        )
        self.status = Label(
            self, text='coluna: 1  linha: 1  arquivo: ',
            bg='#21222c', fg='#fff'
        )
        self.tx.config(
            width=170, height=42, bg='#282a36', fg='#fffffe', bd=0
        )
        
        self.linhas.pack(side='left', fill='y')
        self.tx.pack(expand=True, anchor='ne')
        self.status.pack(expand=True, fill='x', anchor='se')

    def manipula(self, keypress):
        print(keypress)
        self.linha = float(self.tx.index('end-1c')) *1
        self.linha = str(self.linha)
        self.indice = self.linha.index('.')
        coluna = f' Cl: {self.linha[self.indice + 1:]}'
        linha = f' Ln: {self.linha[:self.indice]}'
        self.status['text'] =  f'{coluna} {linha} {" " * 10}{__file__[10:-1]}'
        self.linhas.insert(
            int(self.linha[:self.indice]),
            str(self.linha[:self.indice])
        )
        self.removeLines()
        self.tecla = keypress

    def tabSpace(self, tab):
        self.tx.insert('end', f' ' * 4)
        return 'break'

    def removeLines(self):
        pos = str(self.tx.index('end'))
        ind = pos.index('.')
        pos = int(pos[:ind])
        self.linhas.delete(pos - 1, 'end')


Window().mainloop()