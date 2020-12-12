cid = input('Digite o nome da cidade: ') + '\n'
cid = cid.lower()
indice = 0
for x in range(0, len(cid)):
    if cid[x] == ' ' or cid[x] == '\n':
        indice = x
        break
print(cid[:indice])
if 'santo' in cid[:indice]:
    print('A cidade começa com santo')
else:
    print('A cidade não começa com santo')
    