from tkinter import *
import threading
import random
import time

class MyGame(Tk):
    directionX  = 0
    bulletMove  = 450
    listBullet  = list()
    coord       = list()
    levelSpeed  = 5000
    level       = 1
    
    def __init__(self):
        super(MyGame, self).__init__()
        self.geometry('500x600+400+20')
        self.config(bg='black')
        self.title('StarWar')
        self.bind('<KeyPress>', self.moveSpaceShip)
        self.bind('<Button-1>', self.fireGun)
        self.spaceShip()
        self.enemy()

    def spaceShip(self):
        self.conteiner_ = Frame(self)
        self.conteiner_.config(bg='#000')
        self.baseShip = Frame(
            self.conteiner_, width=30, height=20, bg='teal'
        )
        self.topShip = Frame(
            self.conteiner_, width=10, height=10, bg='teal'
        )
        self.conteiner_.place(x=0, y=560)
        self.topShip.pack()
        self.baseShip.pack()

    def bullet(self):
        self.bala = Frame(self, width=10, height=10, bg='red')
        threading.Thread(
            target=self.bulletSpeed, daemon=True).start()

    def destroyed(self):
        for x in self.listEnemies:
            self.update()
            try:
                indice = self.coord.index(self.directionX + 10)
                self.listEnemies[indice]['bg'] = 'black'
                self.update()
            except:
                ...
        clear_ = self.clearEnemy()
        if clear_:
            self.listEnemies.clear()
            self.enemy()

    def bulletSpeed(self):
        while self.bulletMove > 0:
            self.bala.place(x=self.directionX + 10, y=self.bulletMove)
            self.bulletMove -= 1
        self.bulletMove = 450
        self.bala.destroy()
        
    def moveSpaceShip(self, key):
        self.key = key.keysym
        self.slideHorizontal()

    def slideHorizontal(self):
        if self.key == 'a':
            self.directionX -= 10
        if self.key == 'd':
            self.directionX += 10
        self.conteiner_.place(x=self.directionX, y=560)

    def fireGun(self, key):
        self.bullet()
        self.destroyed()

    def enemy(self):
        self.levelSpeed -= 500
        self.listEnemies = list()
        for widget in range(0, 480, 10):
            self.listEnemies.append(
                Frame(self, width=15, height=15, bg='green')
            )
            self.coord.append(widget)
        cont = 0
        for widget in self.coord:
            self.listEnemies[cont].place(
                x=random.choice(self.coord), y=random.randint(0, 100)
            )
            cont += 1
        self.enemyMove()

    def enemyMove(self):
        cont = 0
        for widget in self.coord:
            self.update()
            try:
                YY = self.listEnemies[cont].winfo_rooty()
                YY += self.level
                self.listEnemies[cont].place(x=widget, y=YY)
                cont += 1
            except:
                ...
        self.after(self.levelSpeed, self.enemyMove)
        self.gameOver()

    def clearEnemy(self):
        lis = []
        try:
            for x in self.listEnemies:
                lis.append(x['bg'])
            if 'green' in lis:
                return False
            for x in self.listEnemies:
                x.destroy()
            return True
        except:
            ...

    def gameOver(self):
        if self.listEnemies[-1].winfo_rooty() > 560:
            self.listEnemies.clear()
            txt = Label(
                self, text="Game Over", font=('Arial', 50, 'bold'), fg='red'
            )
            txt.place(x=20, y=200)
            
            



game = MyGame()
game.mainloop()