vel = int(input('Qual a velocidade do veiculo? '))
if vel > 80:
    multa = float((vel - 80) * 7)
    print(f'veiculo multado em R$ {multa:.2f}'.replace('.', ','))
else:
    print('Veiculo dentro dos limites de velocidade.')