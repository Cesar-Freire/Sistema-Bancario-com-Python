import textwrap

def menu():
    menu = """\n
    ===============     MENU    ===============
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário
    [s] Sair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito:\nR$ {valor:.2f}\n'
        print('===== Depósito realizado com sucesso! =====\n')
    else:
        print('\nxXXXx Operação falhou! O valor informado é inválido> xXXXx')
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print('\n xXXXx Operação falhou! Você não tem saldo sufucuente. xXXXx')

    elif excedeu_limite:
        print('\n xXXXx Operação falhou! O valor do saque excede o limite. xXXXx')

    elif excedeu_saques:
        print('\n xXXXx Operação falhou! Número áximo de saques excedido. xXXXx')

    elif valor > 0:
        saldo -= valor
        extrato += f'Saque:\tR$ {valor:.2f}\n'
        numero_saques += 1
        print('\n ===== Saque realizado com sucesso! =====')

    else:
        print('\n xXXXx Operação falhou! O valor informado é inválido. xXXXx')

    return saldo, extrato
    
def exibir_extrato(saldo,/, *, extrato):
    print('\n===============    EXTRATO   ===============')
    print('Não foram realizando movimentação.' if not extrato else extrato)
    print (f'\nSaldo:\tR$ {saldo:.2f}')

def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente número): ')
    usuarios = filtrar_usuario(cpf, usuarios)

    if usuarios:
        print('\n xXXXx Já existe usuário com esse CPF! xXXXx')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o enderenço (logradouro, nro - bairro - cidade/sigla estado)')

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print('===== Usáio criado com sucesso! =====')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n ===== Conta criada com sucesso" =====')
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print('\n xXXXx Usuário não encontrado, fluxo de criação de conta encerrado! xXXXx')
    return None
    
def lista_contas(contas):
    for conta in contas:
        linhas = f"""\
            Agência:\t{conta['agencia']}
            C/C\t{conta['numero_conta']}
            Titular:\t{conta['usurio']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linhas))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = ''
    numeros_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input('Informe o valor do deposito: '))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == '2':
            valor = float(input('Informe o valor do saque: '))

            saldo, extrato = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numeros_saques,
                limite_saques = limite,
            )

        elif opcao == '3':
            exibir_extrato(saldo, extrato = extrato)

        elif opcao == 'nu':
            criar_usuario(usuarios)

        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 's':
            break

        else:
            print('Operação inválida, por favor selecionar novamente a operação desejada.')
    
main()