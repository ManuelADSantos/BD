#SALDOS

import psycopg2
from getpass import getpass

utilizador_atual = 1

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

#---------------------------------------------MENU SALDO CLIENTE----------------------------------------------------
def saldos_cliente():
    cliente_atual = 1

    #-----------------------------------------------MENU SALDO-----------------------------------------------------
    saldos = True

    #PEDE AO CLIENTE QUE TIPO DE PESQUISA QUER EFETUAR
    while saldos:

        print("----------------------MENU SALDO---------------------")
        print("\n O que pretende fazer? \n")

        s = input("""
                                1 - Ver Saldo
                                2 - Pedir Aumento
                                V|v - Voltar

            Resposta: """)

    #----------------------------------------- VER SALDO---------------------------------------------------------
        if s == "1":

            print("VER SALDO")

            cur.execute(f"SELECT saldo from cliente where utilizador_id = '{cliente_atual}';")

            print("Saldo: ")
            s1 = cur.fetchone()

            if s1 is None:
                print("Resultado não encontrado!")

            while s1 is not None:
                print("->", *s1, ' €')
                s1 = cur.fetchone()

        #--------------------------------------------PEDIR AUMENTO----------------------------------------------------
        elif s == "2":

            print("PEDIR AUMENTO")
            while True:
                try:
                    s2 = int(input("Quanto pretende?: "))

                    if s2 <= 0:
                        raise ValueError("TEM DE SER >0")

                    print ("-> ",s2, "€")

                    cur.execute(f"UPDATE cliente SET pedido_saldo = '{s2}' WHERE utilizador_id = '{cliente_atual}';")

                    print("PEDIDO ACEITE!")

                except ValueError or s2<'0':
                    print("INSIRA UM VALOR VÁLIDO!")
                    continue
                else:
                    break

        #Volta ao menu anterior
        elif s == "V" or s == "v":
            saldos = False

        else:
            print("Inválido")
            print("Tenta outra vez")

#---------------------------------------MENU SALDOS ADMIN-----------------------------------------------------------
def saldos_admin():

    admin_atual = 5

    # -----------------------------------------------MENU SALDO-----------------------------------------------------
    saldos = True

    # PEDE AO ADMIN QUE TIPO DE PESQUISA QUER EFETUAR
    while saldos:
        print("----------------------MENU SALDO---------------------")
        print("\n O que pretende fazer? \n")

        s = input("""
                                   1 - Ver Pedidos de Saldo
                                   V|v - Voltar

               Resposta: """)

        # ----------------------------------------- VER PEDIDOS DE SALDO------------------------------------------------
        if s == "1":

            print("VER PEDIDOS DE SALDO")

            cur.execute("SELECT * from cliente;")

            for linha in cur.fetchall():
                saldo, utilizador_id,pedido_saldo = linha
                print("SALDO:", saldo, "ID:",utilizador_id,"Pedidos de Saldo: ",pedido_saldo)


            alterar = True
            while alterar:
                r = input ("Pretende alterar saldos?: S|N \n")

                if r == "S" or r == "s":

                    cur.execute(f"UPDATE cliente set pedido_saldo = '0';")

                    cur.execute("SELECT * from cliente;")

                    for linha in cur.fetchall():
                        saldo, utilizador_id, pedido_saldo = linha
                        print("SALDO:", saldo, "ID:", utilizador_id, "Pedidos de Saldo: ", pedido_saldo)

                elif r== "N" or r == "n":
                    alterar = False
                else:
                    print("Tenta novamente!\n")

        # Volta ao menu anterior
        elif s == "V" or s == "v":
            saldos = False

        else:
            print("Inválido")
            print("Tenta outra vez")

#ADICIONAR COLUNA
#cur.execute("ALTER TABLE cliente ADD COLUMN pedido_saldo FLOAT(8) NOT NULL DEFAULT '0';")

#cur.execute("ALTER TABLE cliente ALTER COLUMN pedido_saldo DROP DEFAULT;")

#---------------------------------------ADICIONAR SALDO ADMIN-------------------------------------------------------
def alterarsaldo_admin():
    while True:
        print("------------------------------- ALTERAR SALDO -------------------------------\n")
        cur.execute("SELECT utilizador_id, nome, saldo FROM cliente, utilizador WHERE cliente.utilizador_id = utilizador.id;")
        dados = cur.fetchall()
        if len(dados) == 0:
            print("\n\t\t   Não existem clientes registados\n\n\t\t   || A VOLTAR AO MENU ||")
            break
        else:
            for ind in range(len(dados)):
                print("\t\t  ID: ", dados[ind][0], " |Nome: ", dados[ind][1], "|Saldo: ", dados[ind][2],"€")


            cliente_escolhido = input("\n\t\t\tID - Cliente a alterar o saldo\n\t\t\t     v/V - Voltar ao Menu\n\t\t\t\t       ")

            #Voltar ao menu principal
            if (cliente_escolhido == "v" or cliente_escolhido == "V"):
                print("De volta ao MENU")
                break
            try:
                #Verificar se ID existe
                teste = int(cliente_escolhido)
                if isinstance(teste, int):
                    cur.execute(f"SELECT nome, saldo FROM utilizador, cliente WHERE utilizador_id = {cliente_escolhido}")
                    verif = cur.fetchone()
                    if verif is not None:
                        saldo_atual = verif[1]
                        try:
                            valor = -1
                            while valor < 0:
                                valor = float(input("Indique o valor a aumentar no saldo: "))
                                if valor < 0:
                                    print("O valor deve ser positivo")
                                else:
                                    try:
                                        saldo_novo = saldo_atual + valor
                                        tentativas = 3
                                        while tentativas > 0:
                                            confirmar = getpass("Introduza a sua chave de administrador para confirmar a alteração do saldo:\n")
                                            cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                                            chave = cur.fetchone()[0]
                                            cur.execute(f"UPDATE cliente SET saldo = {saldo_novo} WHERE utilizador_id = {cliente_escolhido}")
                                            if confirmar == chave:
                                                print("\nSaldo alterado com sucesso")
                                                conn.commit()
                                                break
                                            else:
                                                tentativas -= 1
                                                print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                                                if tentativas == 0:
                                                    print("\nAlteração de saldo cancelada!")
                                                    conn.rollback()
                                                    break
                                    except:
                                        print("ERRO NA INSERÇÃO")
                        except ValueError:
                            print("VALOR INVÁLIDO")
                    else:
                        print("NÃO EXISTE UM CLIENTE CUJO ID É O INSERIDO")
            except:
                #Valores não numéricos não são avaliados
                print("VALOR INVÁLIDO")


#----------------------------------------CHAMADA DAS FUNÇÕES--------------------------------------------------------
#saldos_cliente()

#saldos_admin()

alterarsaldo_admin()

# Fecha a ligação à base de dados
cur.close()
conn.close()
