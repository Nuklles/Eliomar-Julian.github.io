sal = float(input('Qual o salario do funcionario? '))
sal = sal + (sal * 15 / 100)
print(f'o salario reajustado em 15% fica R$ {sal:.2f}'.
      replace('.', ',')
    )