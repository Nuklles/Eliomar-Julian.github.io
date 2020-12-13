casa = float(input('valor do imovel: '))
salario = float(input('salario do interessado: '))
parcelas = int(input('parcelas: '))
valorParcelas = casa / parcelas
porcentagem = salario * 30 / 100
if valorParcelas <= porcentagem:
    print('Emprestimo aprovado.')
else:
    print('Emprestimo negado.')