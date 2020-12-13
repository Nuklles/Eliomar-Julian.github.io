r = [
    float(input('1ª reta: ')),
    float(input('2ª reta: ')),
    float(input('3ª reta: '))
]
if r[0] < (r[1] + r[2]) and r[1] < (r[0] + r[2]) and r[2] < (r[0] + r[1]):
    print('É possovel formar um triangulo')
else:
    print('NÃO é possivel formar um triangulo')