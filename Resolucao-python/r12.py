valor = float(input('Digite um preço: '))
print(f'o valor R$ {valor:.2f} com 5% de desconto'.replace('.', ',') +
      f' fica por R$ {valor - (valor * 5 / 100):.2f}'.replace('.', ',')
    )