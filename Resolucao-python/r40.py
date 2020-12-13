def primos(num):
    for x in range(2, num // 2):
        if num % x == 0:
            return False
    return True

n = int(input('Digite um  numero: ')) 
if primos(n) == True:
    print('PRIMO')
else:
    print('Não é primo')