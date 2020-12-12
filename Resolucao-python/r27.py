nome = input('digite seu nome completo: ')
espacos = []
for x in range(len(nome)):
    if nome[x] == ' ':
        espacos.append(x)
print(f'seu primeiro nome é "{nome[:espacos[0]]}"')
print(f'seu ultimo nome é "{nome[espacos[-1]:]}"')
