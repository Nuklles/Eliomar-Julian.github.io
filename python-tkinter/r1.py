from tkinter import Tk, Frame, Label, Entry, Button
from tkinter import messagebox


class App(Tk):
    CAD = {'admin': '1234'}

    def __init__(self):
        Tk.__init__(self)
        self.geometry('300x200+100+100')
        self.fr1 = Frame(self)
        self.fr2 = Frame(self)
        self.lNome = Label(self.fr1, text='Nome ')
        self.eNome = Entry(self.fr1)
        self.lSenha = Label(self.fr2, text='Senha ')
        self.eSenha = Entry(self.fr2, show='*')
        self.lNome.pack(side='left')
        self.eNome.pack(side='left')
        self.lSenha.pack(side='left')
        self.eSenha.pack(side='left')
        self.bt = Button(self, text='ok', command=self.validar)
        self.fr1.pack(fill='x', expand=True)
        self.fr2.pack(fill='x', expand=True)
        self.bt.pack(pady=10)
    
    def validar(self):
        nome = self.eNome.get()
        senha = self.eSenha.get()
        try:
            self.CAD[nome]
        except:
            messagebox.showwarning('Erro', 'usuario ou senha incorreto')
            return
        if senha == self.CAD[nome]:
            messagebox.showinfo('Aceito', 'Bem vindo %s' %nome)
        


if __name__ == '__main__':
    App().mainloop()