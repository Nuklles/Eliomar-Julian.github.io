nome = str(input('Digite seu nome completo: ')).strip()
print('Maiusculo: ' + nome.upper())
print('Minusculo: ' + nome.lower())
cont = contNome = 0
for tot in nome:
    if tot != ' ':
        cont += 1
try: 
    i = nome.index(' ')
    print('seu primeiro nome tem %s letras' % str(len(nome[:i])))
except:
    pass
print(f'{nome} possui {cont} letras.')

