km = float(input('Km rodados do veiculo: '))
dias = float(input('Dias rodando: '))
print(
    'o valor a ser pago é de R$ %s' %((60 * dias) + (0.15 * km))
)