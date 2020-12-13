numeros = [
    int(input('Digite um numero: ')),
    int(input('Digite outro numero: ')),
    int(input('Digite mais um numero: '))
]
maior = menor = cont = 0
for x in numeros:
    if (cont == 0):
        maior = menor = x
    else:
        if (x > maior): maior = x
        if (x < menor): menor = x
    cont += 1
print(f'o maior: {maior}')
print(f'o menor: {menor}')