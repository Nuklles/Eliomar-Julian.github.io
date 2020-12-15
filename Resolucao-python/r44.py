from time import sleep

cadastrados = {'admin': '1234', 'user': 'admin'}
while True:
    print(
        f'''
        {'=' * 30}
        [1] Cadastrar usuario{' '*7} |
        [2] Ver Cadastro{' '*12} |
        [3] Entrar{' '*18} |
        [4] Sair{' '*20} |
        {'=' * 30}
        '''
    )
    opc = int(input('>>> '))
    if opc == 1:
        nome = str(input('Nome: '))
        senha = str(input('senha: '))
        cadastrados[nome] = senha
        continue
    elif opc == 2:
        for x in cadastrados.keys():
            print(x)
        sleep(1.5)
    elif opc == 3:
        nome = str(input('Nome: '))
        senha = str(input('Senha: '))
        try:
            cadastrados[nome]
        except:
            print('Usuario invalido')
            sleep(1)
            continue
        if senha != cadastrados[nome]:
            print('Senha invalida')
            sleep(1)
        else:
            print('Seja bem vindo ' + nome)
    elif opc == 4:
        break
    else:
        print('escolha uma opção valida')
        continue

