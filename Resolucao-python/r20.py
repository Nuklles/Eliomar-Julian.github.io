from random import shuffle
lista = list()
for x in range(1, 5): lista.append(input(f'Nome {x}: '))
shuffle(lista)
print(lista)
