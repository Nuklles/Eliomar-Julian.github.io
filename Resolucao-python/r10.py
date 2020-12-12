valor = float(input('Quanto você tem na carteira? '))
print(
    f'Com o valor de R$ {valor:.2f} da para comprar U$ {valor / 5:.2f}.'.
    replace('.', ',')
    )