#!/bin/bash
# visivel somente em terminais compativeis como os terminais do linux
# terminais padroes do windows não sao compativeis
# use git-bash no vscode para ter a experiencia

espaco = 30
for x in range(0, 15):
    if x == 0:
        print('\n\n')
        print(' ' * (espaco // 2 - 1) + '☆', end='')
    print('\033[32;40m ' * (espaco // 2)+ '**' * x)
    espaco -= 2
for x in range(0, 5):
    print(f'\033[33m{"*"* 5:>17}')
print('\033[31m/\\' * 18)