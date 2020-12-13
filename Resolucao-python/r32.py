from datetime import date
ano = int(input('Ano a analizar: '))
if (ano % 4 == 0) and (ano % 100 != 0) or (ano % 400 == 0):
    print('%s é bissexto.' % ano)
else:
    print('%s NÃO é bissexto.' % ano)