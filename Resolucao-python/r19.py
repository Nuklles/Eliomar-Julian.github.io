from random import choice
alunos = list()
for x in [1, 2, 3, 4]:
    alunos.append(input(f'Nome do {x}º aluno: '))
print('o sorteado foi ' + choice(alunos))