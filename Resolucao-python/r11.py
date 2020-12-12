area = [
    float(input('Largura: ')),
    float(input('Altura: '))
    ]
print(f'sua parede tem {area[0] * area[1]:.2f}' + 
      f' m² e precisara de {(area[0] * area[1]) / 2}' + 
      ' litros de tinta.'
    )