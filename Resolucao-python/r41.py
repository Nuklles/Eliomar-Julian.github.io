frase = str(input('Deigite uma frase para a analize: '))
invertido = str()
sem_espaco = str()

for letras in range(-len(frase) + 1, 1):
    if frase[letras * -1] != ' ':
        invertido = invertido + frase[letras * -1]

for sE in range(len(frase)):
    if frase[sE] != ' ':
        sem_espaco = sem_espaco + frase[sE]

if sem_espaco == invertido:
    print('A frase digitaada é palindromo')
else:
    print('Não é palindromo')