print(
    '''
    Coversor de medidas digite um valor
    em metros abaixo para converter-mos.
    '''
    )
medida = float(input('>>> '))
print(f'Centimetros: {medida * 100:.2f}')
print(f'Milimetros: {medida * 1000:.2f}')
print(f'Decimetro: {medida * 10:.2f}')
print(f'Nanometros: {medida / 10**-9:.2f}')
print(f'Polegadas: {medida / 2.5:.2f}')