numero = str(input('Digite um numero: '))
try:
    i = numero.index('.')
    print(f'A porção interira de {numero} é {numero[:i]}')
except:
    if numero.isnumeric():
        print('inteiro ' + numero)
    else:
        print(numero + ' não é numero...')