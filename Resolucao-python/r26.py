frase = str(input('Digite uma frase: '))
contaA = 0
primeiroA = ultimoA = None
for x in range(0, len(frase)):
    if frase[x] == ' ':
        continue
    if frase[x].lower() == 'a':
        contaA += 1
        ultimoA = x
        if not primeiroA:
            primeiroA = x
print(f'A frase "{frase}" possui: ')
print(f'{contaA} letra "A"')
print(f'o primeiro "A" se encontra na posição {primeiroA}')
print(f'o ultimo "A" se encontra na posicao {ultimoA}')