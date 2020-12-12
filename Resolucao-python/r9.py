numero = int(input('Digite um numero para ver sua tabuada: '))
for x in range(1, 11):
    print(f'{numero} X {x:^4} {"=":>2} {numero * x:^5}')