import sys
import tkinter as tk
from tkinter import Tk, Text, font
import subprocess
import time
import asyncio
import threading


class Console(Tk):
    '''
    Funciona bem se voce tiver o git-bash configurando como prompt padrao
    do vscode
    '''
    listaLimpar = ['cls', 'clear', 'reset']
    def __init__(self):
        Tk.__init__(self)
        self.title('Meu console personalizado...')
        self.bind('<Return>', self.entradaComando)
        self.fonte = font.Font(family='Consolas', size=11, slant='roman')
        self.entrada = Text(
            self, width=100, height=20, bg='#000', fg='#fff',
            insertbackground='#fff', font=self.fonte
        )
        self.entrada.focus_force()
        self.entrada.pack(fill=tk.X, expand=tk.TRUE)
        self.linhaComando()
    
    def linhaComando(self):
        linha = str(self.entrada.index('end-1c'))
        indice = None
        try:
            indice = linha.index('.')
        except:
            pass
        self.entrada.insert(f'{linha[:indice]}.0', '>>> ')
        self.entrada.tag_add(
            'indicador', f'{linha[:indice]}.0', f'{linha[:indice]}.3'
        )
        self.entrada.tag_config('indicador', foreground='orange')

    def entradaComando(self, comando):
        self.linhaAtual = float(self.entrada.index('insert'))
        self.comando = self.entrada.get((self.linhaAtual - 1) + 0.4, tk.END)
        threading.Thread(target=self.rodando, daemon=True).start()

    def rodando(self):
        asyncio.run(self.comandos())

    async def comandos(self):
        self.comando_ = (self.comando.strip())
        self.processo = await asyncio.create_subprocess_shell(
            self.comando_, 
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await self.processo.communicate()
        if self.processo.returncode == 0:
            try:
                saida = stdout
                self.entrada.insert(tk.END, saida)
            except UnicodeDecodeError as err:
                self.entrada.insert(tk.END, str(err) + '\n')
        else:
            try:
                saida = stderr
                self.entrada.insert(tk.END, saida)
            except UnicodeDecodeError as err:
                self.entrada.insert(tk.END, str(err) + '\n')
        self.linhaComando()



if __name__ == "__main__":
    Console().mainloop()
