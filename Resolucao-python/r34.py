salario = float(input('Salario atual: '))
if salario >= 1250:
    salario = salario + ((salario * 10) / 100)
    print(f'salario reajustado a 10% R$ {salario:.2f}'.replace('.', ','))
else:
    salario = salario + ((salario * 15) / 100)
    print(f'salario reajustado a 15% R$ {salario:.2f}'.replace('.', ','))