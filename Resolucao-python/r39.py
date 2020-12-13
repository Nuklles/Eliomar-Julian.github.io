num = list()
soma = 0
for x in range(6):
    num.append(int(input(f'Digite o {x + 1} numero: ')))
for y in num:
    if y % 2 == 0:
        soma += y
print(f'A soma dos numeros pares é {soma}')