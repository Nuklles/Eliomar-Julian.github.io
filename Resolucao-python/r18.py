import math
s = float(input('Digite um angulo para seno: '))
c = float(input('Digite um angulo para cosseno: '))
t = float(input('Digite um angulo para tangente: '))
seno = math.sin(math.radians(s))
cosseno = math.cos(math.radians(c))
tangente = math.tan(math.radians(t))
print(f'seno: {seno:.2f}\ncosseno: {cosseno:.2f}\ntangente: {tangente:.2f}')
