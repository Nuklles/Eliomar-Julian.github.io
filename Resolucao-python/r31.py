kms = float(input('Qual a distancia da viagem? '))
if kms <= 200:
    print(f'a passagem custara R$ {kms * 0.50:.2f}'.replace('.', ','))
else:
    print(f'a passagem custara R$ {kms * 0.45:.2f}'.replace('.', ','))