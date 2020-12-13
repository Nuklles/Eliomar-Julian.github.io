numero = int(input('Digite um numero para a conversão: '))
for x in ['[1] binario', '[2] hexadecimal', '[3] octal']:
    print(x)
opcao = int(input(''))
if (opcao == 1):
    print(bin(numero))
elif (opcao == 2):
    print(hex(numero))
elif (opcao == 3):
    print(oct(numero))