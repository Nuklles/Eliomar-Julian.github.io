import random
import time
player = int(input('Digite um numero entre 0 e 5: '))
n = random.randint(0, 5)
if player == n:
    print('PARABENS voce advinhou')
else:
    print('ERROU')