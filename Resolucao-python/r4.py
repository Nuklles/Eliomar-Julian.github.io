palavra = input('Digite algo: ')
print('a variavel é do tipo ' + str(type(palavra)))
print('a frase possui ' + str(len(palavra)) + ' caracteres.')
if palavra.isnumeric():
    print(f'{palavra} é um numero.')
elif palavra.isalpha():
    print(f'{palavra} é uma string.')
