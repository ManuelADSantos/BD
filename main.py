import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass
import os
import datetime

#==========================================================================================================================
# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

#==========================================================================================================================
#Variáveis globais
utilizador_atual = 0    #Utilizador com login efetuado

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                             ECRÃ INICIAL
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Início/Ecrã inicial
def inicio():
    while True:
        try:
            print("""\n----------------------------Início--------------------------------
                         ____      __
                        |    \    |  |
                        |     \   |  |
                        |  |\  \  |  |
                        |  | \  \ |  |
                        |  |  \  \|  |
                        |  |   \     |
                        |__|    \____|
                """)
            print("""\n\t\t     Bem vind@ ao NETFLOX\n
                          1 - Login\n
                        2 - Registar\n
                          3 - Sair\n\n
                          ESCOLHA""")

            #Escolha da ação a tomar
            inicio_escolha = int(input("\n\t\t\t     "))
            if (inicio_escolha == 1):       #Login
                login()
                #Diferenciar entre admin e cliente
                cur.execute(f"SELECT * FROM administrador where utilizador_id = {utilizador_atual}")
                ser_admin = cur.fetchone()
                if ser_admin is not None:       #ADMIN
                    menu_admin()
                elif ser_admin is None:         #CLIENTE
                    menu_cliente()

            elif(inicio_escolha == 2):      #Registo
                registo()
            elif(inicio_escolha == 3):      #Sair
                return
            else:
                print("")
        #Se não for introduzido um número
        except ValueError:
            print("")


#==========================================================================================================================
#Login
def login():
    print("\n----------------------------Login--------------------------------")
    while True:
        email = input("\n\t\t\t || Email ||\n\t\t ")
        cur.execute(f"SELECT COUNT(email) FROM utilizador WHERE email LIKE '%{email}' AND email LIKE '{email}%'")
        email_verif = cur.fetchone()
        if (email_verif[0]==1):
            while True:
                password = getpass("\n\t\t        || Password ||\n\t\t\t     ")
                cur.execute(f"SELECT password FROM utilizador WHERE email LIKE '%{email}' AND email LIKE '{email}%'")
                password_verif = cur.fetchone()
                if(sha256_crypt.verify(password ,password_verif[0])):
                    print("\nInicio de sessão bem sucedida\n")
                    cur.execute(f"SELECT id FROM utilizador WHERE email LIKE '%{email}' AND email LIKE '{email}%'")
                    global utilizador_atual
                    utilizador_atual = cur.fetchone()[0]
                    break
                else:
                    print(f"\nPassword errada")
            break
        else:
            print("\nEndereço de email inválido")

    return


#==========================================================================================================================
#Registo
def registo():
    while True:
        #Registo do Email
        print("\n----------------------------Registo--------------------------------")
        while True:
            email = input("\nInsira o seu endereço de email\n    ")
            cur.execute(f"SELECT COUNT(email) FROM utilizador WHERE email LIKE '%{email}' AND email LIKE '{email}%'")
            email_verif = cur.fetchone()
            if ("@" in email and email_verif[0]==0 and ' ' not in email and email[0]!= '@' and email[len(email)-1]!='@' and '.' in email):
                print(f"Email inserido\n    {email}")
                break
            else:
                print("\nEndereço de email inválido")

        #Registo da Password
        while(True):
            password = getpass("\n\nInsira a sua password\n    ")
            password_encriptada = sha256_crypt.hash(password)
            password_verif = getpass("Confirme a sua password\n    ")
            if(sha256_crypt.verify(password_verif ,password_encriptada)):
                print("Password aceite\n")
                break
            else:
                print("Passwords não correspondem")

        #Registo do nome
        nickname = input("\n\nInsira o seu nome\n    ")
        print(f"Nome inserido\n    {nickname}")

        #Guardar dados na base de dados
        try:
            cur.execute(f"INSERT INTO utilizador(id, email, password, nome) VALUES (DEFAULT, '{email}', '{password_encriptada}', '{nickname}') RETURNING id;")
            id = cur.fetchone()[0]
            cur.execute(f"INSERT INTO cliente(utilizador_id, saldo) VALUES ({id}, 15);")
            #Confirmar mudanças
            conn.commit()
            #De volta ao início
            print("BEM VIND@ À FAMÍLIA NETFLOX")
            return
        except:
            conn.rollback()
            print("Dados não válidos")


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                               CLIENTE
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#==========================================================================================================================
#Menu CLIENTE
def menu_cliente():
    while True:
        print("\n-------------------------------------MENU CLIENTE-----------------------------------------------\n")

        escolha_admin = input("""
                              1 - Ver Saldo
                              2 - Pesquisa
                              V|v- Logout

        Ver: """)

        if escolha_admin == "1":
            saldos_cliente()

        if escolha_admin == "2":
            saldos_cliente()

        elif escolha_admin == "V" or escolha_admin== "v":
            print("LOGOUT")
            return

        else:
            print("Inválido\nTenta outra vez")


#==========================================================================================================================
#Menu CLIENTE - Saldo
def saldos_cliente():
    #-----------------------------------------------MENU SALDO-----------------------------------------------------
    saldos = True

    #PEDE AO CLIENTE QUE TIPO DE PESQUISA QUER EFETUAR
    while saldos:

        print("----------------------MENU SALDO---------------------\n")

        cur.execute(f"SELECT saldo from cliente where utilizador_id = '{utilizador_atual}';")

        s1 = cur.fetchone()

        if s1 is None:
            print("Resultado não encontrado!")

        while s1 is not None:
            print("\t\t    Saldo ->", *s1, '€')
            s1 = cur.fetchone()

        s = input("\n\t\t      V|v - Voltar\n\t\t\t   ")

        #Volta ao menu anterior
        if s == "V" or s == "v":
            saldos = False

        else:
            print("Inválido")
            print("Tenta outra vez")


#==========================================================================================================================
#Menu CLIENTE - Mensagens



#==========================================================================================================================
#Menu CLIENTE - PESQUISAR
def menu_pesquisar():

    pesquisarmenu = True

    #PEDE AO CLIENTE QUE TIPO DE PESQUISA QUER EFETUAR
    while pesquisarmenu:
        print("----------------------MENU PESQUISA---------------------")
        print("\n Onde pretende pesquisar? \n")

        pesquisar = input("""
                            1 - Pesquisa a todos os artigos do Sistema
                            2 - Pesquisa Artigos Alugados
                            V|v - Voltar MENU CLIENTE

        Resposta: """)

        # 1 - Pesquisa a todos os artigos do Sistema -> Funcao pesquisa_geral
        if pesquisar == "1":
            pesquisa_geral()

        # 2 - Pesquisa Artigos Alugados - > Funcao pesquisa_user
        elif pesquisar == "2":
            pesquisa_user()

        #Volta ao menu anterior
        elif pesquisar == "V" or pesquisar == "v":
            pesquisarmenu = False

        else:
            print("Inválido")
            print("Tenta outra vez")


# -----------------------------------------------Pesquisa a todos os artigos do sistema---------------------------------------------
def pesquisa_geral():
    pesquisageral = True
    ordenar = False
    # Pergunta ao cliente que tipo de pesquisa quer fazer
    while pesquisageral:
        print(
            "-------------------------------Pesquisa a todos os artigos do sistema:-----------------------------------------------")
        print("\n Como pretende pesquisar? \n")
        pesquisa = input("""
                                  1 - Tipo
                                  2 - Titulo
                                  3 - Ator
                                  4 - Realizador
                                  5 - Produtor
                                  6 - Ano
                                  V|v - Voltar MENU PESQUISA

            Pesquisa por: """)

        if pesquisa == "V" or pesquisa == "v":
            print("\n Voltar ao MENU PESQUISA")
            pesquisageral = False
            ordenar = False

        elif pesquisa == "1" or pesquisa == "2" or pesquisa == "3" or pesquisa == "4" or pesquisa == "5" or pesquisa == "6":
            ordenar = True

        else:
            ordenar = False
            print("\n Inválido! \n Tenta outra vez")


        # especificar critérios de ordenação dos resultados
        if ordenar == True:

            while True:
                try:

                    ordem = int(input(""" Ordenação dos resultados:
                                           1 - ordem crescente
                                           2 - ordem decrescente
                     ORDEM(1|2): """))

                    if ordem != 1 and ordem != 2:
                        raise ValueError("ERRO")
                except ValueError:
                    print("ERRO")
                    continue
                else:
                    break

            if ordem == 1:
                ordem = "ASC"
            elif ordem == 2:
                ordem = "DESC"

        print("\n")

        # --------------------------------------------PESQUISA POR TIPO-------------------------------------------------
        if pesquisa == "1":

            titulo1 = input("Pesquisa por tipo : \n")

            cur.execute(f"SELECT titulo from artigo where tipo like '%{titulo1}' ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_tipo = cur.fetchone()

            if p_tipo is None:
                print("Resultado não encontrado!")

            while p_tipo is not None:
                print("-> ", *p_tipo)
                p_tipo = cur.fetchone()

        # --------------------------------------------PESQUISA POR TITULO-------------------------------------------------
        elif pesquisa == "2":

            titulo2 = input("Pesquisa por título: \n")

            cur.execute(f"SELECT titulo FROM artigo WHERE titulo like '%{titulo2}' ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_titulo = cur.fetchone()

            if p_titulo is None:
                print("Resultado não encontrado!")

            while p_titulo is not None:
                print("->", *p_titulo)
                p_titulo = cur.fetchone()

        # --------------------------------------------PESQUISA POR ATOR--------------------------------------------------
        elif pesquisa == "3":

            titulo3 = input("Pesquisa por Ator: \n")

            cur.execute(
                f"SELECT artigo.titulo from artigo join artigo_atores on artigo.id = artigo_atores.artigo_id join atores on atores.id= artigo_atores.atores_id where atores.nome like '%{titulo3}' ORDER BY titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_atores = cur.fetchone()

            if p_atores is None:
                print("Resultado não encontrado!")

            while p_atores is not None:
                print("->", *p_atores)
                p_atores = cur.fetchone()

        # --------------------------------------------PESQUISA POR REALIZADOR-------------------------------------------------
        elif pesquisa == "4":

            titulo4 = input("Pesquisa por realizador: \n")

            cur.execute(f"SELECT titulo from artigo where realizador like '%{titulo4}' ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_realizador = cur.fetchone()

            if p_realizador is None:
                print("Resultado não encontrado!")

            while p_realizador is not None:
                print("->", *p_realizador)
                p_realizador = cur.fetchone()


        # --------------------------------------------PESQUISA POR PRODUTOR-------------------------------------------------
        elif pesquisa == "5":

            titulo5 = input("Pesquisa por produtor: \n")

            cur.execute(f"SELECT titulo from artigo where produtor like '%{titulo5}' ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")
            p_produtor = cur.fetchone()

            if p_produtor is None:
                print("Resultado não encontrado!")

            while p_produtor is not None:
                print("->", *p_produtor)
                p_produtor = cur.fetchone()

        # --------------------------------------------PESQUISA POR ANO-------------------------------------------------
        elif pesquisa == "6":

            while True:
                try:
                    titulo6 = int(input("Pesquisa por Ano: \n"))
                    # a primeira exibição de um filme de curta duração aconteceu no Salão Grand Café, em Paris, em 28 de dezembro de 1895
                    if titulo6 < 1895 or titulo6>=2021:
                        raise ValueError("INSIRA UM ANO VÁLIDO!")
                except ValueError:
                    print("INSIRA UM ANO VÁLIDO!")
                    continue
                else:
                    break

            cur.execute(f"SELECT titulo from artigo where ano = '{titulo6}' ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_ano = cur.fetchone()

            if p_ano is None:
                print("Resultado não encontrado!")

            while p_ano is not None:
                print("->", *p_ano)

                p_ano = cur.fetchone()
    return

# -------------------------------------Pesquisa aos artigos neste momento alugados pelo cliente--------------------------
def pesquisa_user():

    cliente_atual = 2
    pesquisauser = True
    ordenar = True

    # Pergunta ao cliente que tipo de pesquisa quer fazer
    while pesquisauser:

        print(
            "-------------------------------Pesquisa aos artigos neste momento alugados:-----------------------------------------------")
        print("\n Como pretende pesquisar? \n")

        pesquisa = input("""
                                  1 - Tipo
                                  2 - Titulo
                                  3 - Ator
                                  4 - Realizador
                                  5 - Produtor
                                  6 - Ano
                                  V|v - Voltar MENU PESQUISA
            Pesquisa por: """)

        if pesquisa == "V" or pesquisa == "v":
            print("\n Voltar ao MENU PESQUISA")
            pesquisauser = False
            ordenar = False

        elif pesquisa == "1" or pesquisa == "2" or pesquisa == "3" or pesquisa == "4" or pesquisa == "5" or pesquisa == "6":
            ordenar = True

        else:
            ordenar = False
            print("\n Inválido! \n Tenta outra vez")

        # especificar critérios de ordenação dos resultados
        if ordenar == True:
            while True:
                try:
                    ordem = int(input("""Ordenação dos resultados:
                                        1 - ordem crescente
                                        2 - ordem decrescente
                     ORDEM(1 | 2): """))

                    if ordem != 1 and ordem != 2:
                        raise ValueError("ERRO")

                except ValueError:
                    print("ERRO")
                    continue
                else:
                    break

            if ordem == 1:
                ordem = "ASC"
            elif ordem == 2:
                ordem = "DESC"

        print("\n")

        # --------------------------------------------PESQUISA POR TIPO-------------------------------------------------
        if pesquisa == "1":

            titulo1 = input("Pesquisa por tipo: \n")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.tipo like '%{titulo1}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_tipo = cur.fetchone()

            if p_tipo is None:
                print("Resultado não encontrado!")

            while p_tipo is not None:
                print("->", *p_tipo)
                p_tipo = cur.fetchone()

        # --------------------------------------------PESQUISA POR TITULO-------------------------------------------------
        elif pesquisa == "2":

            titulo2 = input("Pesquisa por título: \n")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.titulo like '%{titulo2}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_titulo = cur.fetchone()

            if p_titulo is None:
                print("Resultado não encontrado!")

            while p_titulo is not None:
                print("->", *p_titulo)
                p_titulo = cur.fetchone()

        # --------------------------------------------PESQUISA POR ATOR-------------------------------------------------
        elif pesquisa == "3":

            titulo3 = input("Pesquisa por Ator: \n")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id join artigo_atores on artigo.id = artigo_atores.artigo_id join atores on atores.id= artigo_atores.atores_id where atores.nome like '%{titulo3}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}' ORDER BY titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_atores = cur.fetchone()

            if p_atores is None:
                print("Resultado não encontrado!")

            while p_atores is not None:
                print("->", *p_atores)
                p_atores = cur.fetchone()

        # --------------------------------------------PESQUISA POR REALIZADOR-------------------------------------------------
        elif pesquisa == "4":

            titulo4 = input("Pesquisa por realizador: \n")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.realizador like '%{titulo4}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_realizador = cur.fetchone()

            if p_realizador is None:
                print("Resultado não encontrado!")

            while p_realizador is not None:
                print("->", *p_realizador)
                p_realizador = cur.fetchone()

        # --------------------------------------------PESQUISA POR PRODUTOR-------------------------------------------------
        elif pesquisa == "5":

            titulo5 = input("Pesquisa por produtor: \n")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.produtor like '%{titulo5}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_produtor = cur.fetchone()

            if p_produtor is None:
                print("Resultado não encontrado!")

            while p_produtor is not None:
                print("->", *p_produtor)
                p_produtor = cur.fetchone()

        # --------------------------------------------PESQUISA POR ANO-------------------------------------------------
        elif pesquisa == "6":

            while True:
                try:
                    titulo6 = int(input("Pesquisa por Ano: \n"))
                    # a primeira exibição de um filme de curta duração aconteceu no Salão Grand Café, em Paris, em 28 de dezembro de 1895
                    if titulo6 < 1895 or titulo6 >= 2021:
                        raise ValueError("INSIRA UM ANO VÁLIDO!")
                except ValueError:
                    print("INSIRA UM ANO VÁLIDO!")
                    continue
                else:
                    break

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.ano = '{titulo6}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")

            if ordem == "ASC":
                print("Título (ordem crescente):")

            elif ordem == "DESC":
                print("Título (ordem decrescente):")

            p_ano = cur.fetchone()

            if p_ano is None:
                print("Resultado não encontrado!")

            while p_ano is not None:
                print("->", *p_ano)
                p_ano = cur.fetchone()

    return


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                               ADMIN
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Menu ADMIN
def menu_admin():
    while True:
        print("\n-------------------------------------MENU ADMIN-----------------------------------------------\n")

        escolha_admin = input("""
                              1 - Estatísticas
                              2 - Adicionar Artigo
                              3 - Remover Artigo
                              4 - Enviar Mensagens
                              5 - Inventário de Artigos(detalhes e histórico de preços)
                              V|v- Logout

        Ver: """)

        if escolha_admin == "1":
            admin_estatisticas()

        elif escolha_admin == "2":
            admin_adicionarartigo()

        elif escolha_admin == "3":
            admin_removerartigo()

        elif escolha_admin == "4":
            admin_mensagens()

        elif escolha_admin == "5":
            inventario()

        elif escolha_admin == "V" or escolha_admin== "v":
            print("LOGOUT")
            return

        else:
            print("Inválido\nTenta outra vez")


#==========================================================================================================================
#Menu ADMIN - Inventário, detalhes, condições de aluguer histórico de preços
def inventario():
    while True:
        print("---------------------------------INVENTÁRIO DE ARTIGOS----------------------------------------")

        cur.execute("SELECT id, titulo, tipo from artigo ORDER BY tipo ASC, titulo ASC;")

        for linha in cur.fetchall():
            id, titulo, tipo = linha
            print("Título: ", titulo,"| Tipo: ", tipo,"| ID: ", id)



        print("\n\t\t\t\t   O que pretende fazer?")

        det = input("\n\t\t\t\t1 - Ver Detalhes do Artigo\n\t\t\t\t\tV|v - Voltar\n\n\t\t\t\t\t    ")

        # ----------------------------------------- VER DETALHES ARTIGO-------------------------------------------------
        if det == "1":
            while True:
                print("\n---------------------------VER DETALHES ARTIGO---------------------------\n")
                voltar = input("ENTER - Ver detalhes\nV/v - Voltar ao Inventário\n\n")
                if voltar == "":
                    while True:
                        try:
                            artdet = int(input("De que artigo quer ver detalhes?(ID): "));
                            break
                        except ValueError:
                            print("Valor de ID inválido")


                    try:
                        cur.execute(f"SELECT titulo, tipo, realizador, produtor, ano from artigo where id = '{artdet}';")
                        detalhes = cur.fetchone()
                        if detalhes is None:
                           print(f"Não existe um artigo com o ID {artdet}")
                           break
                        else:
                            print("\nDetalhes do artigo: ")
                            print(f"Título: {detalhes[0]} | Tipo: {detalhes[1]} | Realizador: {detalhes[2]} | Produtor: {detalhes[3]} | Ano: {detalhes[4]} ")


                            try:
                                cur.execute(f"SELECT nome FROM atores, artigo_atores WHERE atores.id = artigo_atores.atores_id and artigo_id = {artdet};")
                                nomes = cur.fetchone()
                                if nomes is None:
                                    print("Atores : N/A")
                                else:
                                    print(f"Atores: ")
                                    while nomes is not None:
                                        print(" ", *nomes)
                                        nomes = cur.fetchone()
                            except:
                                print("Atores : N/A")


                            print("\n Mais detalhes: \n")
                            while True:

                                det1 = input("""
                                            1- Histórico de preços
                                            2- Condições de Aluguer
                                            V|v - Voltar
                                VER: """)

                                #Histórico de preços
                                if det1 == "1":
                                    historico(artdet)
                                    break

                                #Condições de aluguer
                                elif det1 == "2":

                                    print("\n----------------------------Condições de aluguer--------------------------------------\n")

                                    cur.execute(f"SELECT periodo_de_aluguer, preco from artigo, historico_precos where artigo.id = {artdet} and historico_precos.atual = True and historico_precos.artigo_id = {artdet};")

                                    for linha in cur.fetchall():
                                        periodo_de_aluguer, preco = linha
                                        print("Período de aluguer(em meses): ", periodo_de_aluguer, "| Preço: ", preco, " €")
                                    break

                                #Voltar
                                elif det1 == "V" or det1 == "v":
                                    break
                                else:
                                    print("Inválido")
                                    print("Tente outra vez")
                    except ValueError:
                        print("ID inválido")

                elif voltar == "v" or voltar == "V":
                    print("A VOLTAR AO INVENTÁRIO")
                    break
                else:
                    print("")

        # Volta ao Inventário
        elif det == "V" or det == "v":
            break

        # Input não válido
        else:
            print("\n\t\t\t\t\tInválido")
            print("\t\t\t\t     Tenta outra vez\n")


# -----------------------------------------------Histórico de preços---------------------------------------------
def historico(art):

    print("\n--------------------------------Histórico de preços----------------------------------------------\n")

    cur.execute(f"SELECT preco, entrada_em_vigor, atual from historico_precos where artigo_id = '{art}' ORDER BY entrada_em_vigor DESC;")

    for linha in cur.fetchall():
        preco, entrada_em_vigor, atual = linha
        print("Preço: ", preco, "€ | Entrada em vigor: ", entrada_em_vigor, " | Atual?:", atual)

    while True:
        corrigir = input("\nAlterar Preço? (S|N): \n")

        if corrigir == "S" or corrigir == "s":

            print("--------------------------------------CORRIGIR PREÇO---------------------------------------------------")

            while True:
                try:
                    p = float(input("Preço Novo: \n"))
                    if p < 0:
                        raise ValueError("INSIRA UM VALOR VÁLIDO!")
                    else:
                        break
                except ValueError:
                    print("INSIRA UM VALOR VÁLIDO!")

            tentativas = 3
            while tentativas > 0:
                confirmar = getpass("Introduza a sua chave de administrador para confirmar a alteração do preço:\n")
                cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                chave = cur.fetchone()[0]
                if confirmar == chave:
                    cur.execute(f"INSERT INTO historico_precos(id,preco, entrada_em_vigor, atual, artigo_id) VALUES (DEFAULT,{p}, CURRENT_TIMESTAMP, True, {art});")
                    print("Preço Alterado!")
                    conn.commit()
                    return
                else:
                    tentativas -= 1
                    print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                    if tentativas == 0:
                        print("\nAlteração de preço cancelada!")
                        return

            break

        elif corrigir == "N" or corrigir == "n":
            return


#==========================================================================================================================
#Menu ADMIN - Mensagens
def admin_mensagens():
    while True:
        print("----------------------MENU MENSAGENS---------------------")
        print("\n Que mensagem pretende enviar? \n")

        msg = input("""
                            1 - MENSAGEM GERAL
                            2 - MENSAGEM INDIVIDUAL
                            V|v - Voltar

        ENVIAR: """)

        # -----------------------------------Mensagem geral--------------------------------------
        if msg == "1":
            while True:
                print("----------------------MENU MENSAGEM GERAL---------------------")
                voltar = input("\nENTER - Enviar Mensagem\nV/v - Voltar ao MENU\n\n")
                if voltar == "":
                    while True:
                        texto = input("ESCREVA A MENSAGEM: \n")
                        verif_geral = input("Confirma que é esta a mensagem a enviar?(S/N)")
                        if verif_geral == "S" or verif_geral == "s":
                            try:
                                print("Mensagem Confirmada")
                                #Inserir mensagem na tabela mensagens
                                cur.execute(f"INSERT INTO mensagem(id, corpo) VALUES (DEFAULT, '{texto}') RETURNING id;")
                                id_mensagem = cur.fetchone()[0]
                                #Registar mensagem na tabela mensagem_administrador
                                cur.execute(f"INSERT INTO mensagem_administrador(mensagem_id, administrador_utilizador_id) VALUES ({id_mensagem}, {utilizador_atual});")
                                #Registar mensagem na tabela cliente_mensagem
                                cur.execute("SELECT utilizador_id FROM cliente")
                                for linha in cur.fetchall():
                                    utilizador_id = linha[0]
                                    cur.execute(f"INSERT INTO cliente_mensagem(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {utilizador_id});")
                                tentativas = 3
                                sair = False
                                while tentativas > 0:
                                    confirmar = getpass("Introduza a sua chave de administrador para confirmar o envio da mensagem:\n")
                                    cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                                    chave = cur.fetchone()[0]
                                    if confirmar == chave:
                                        print("MENSAGEM GERAL ENVIADA ")
                                        conn.commit()
                                        sair = True
                                        break
                                    else:
                                        tentativas -= 1
                                        print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                                        if tentativas == 0:
                                            print("\nEnvio da mensagem cancelado!")
                                            conn.rollback()
                                            sair = True
                                            break
                                if (sair == True):
                                    break

                            except:
                                conn.rollback()
                                print("ERRO: MENSAGEM GERAL ANULADA ")
                        elif verif_geral == "N" or verif_geral == "n":
                            print("Mensagem Eliminada")
                            break
                        else:
                            print("Opção inválida")
                            break

                elif voltar == "v" or voltar == "V":
                    print("A VOLTAR AO MENU")
                    mensagensa = False
                    break
                else:
                    print("")

        # -----------------------------------Mensagem individual-----------------------------------
        elif msg == "2":
            while True:
                print("----------------------MENU MENSAGEM INDIDUAL---------------------")
                voltar = input("\nENTER - Enviar Mensagem\nV/v - Voltar ao MENU\n\n")
                if voltar == "":
                    while True:
                        print("Clientes aos quais é possível enviar mensagem\n")
                        cur.execute("SELECT utilizador_id, nome FROM cliente, utilizador WHERE utilizador_id = id")
                        #print(cur.fetchall())
                        for linha in cur.fetchall():
                            utilizador_id, nome = linha
                            print("-> ID:", utilizador_id,"/Nome: ", nome)

                        try:
                            cliente_msg = int(input("Qual o ID do cliente ao qual pretende enviar mensagem?\n"))
                            cur.execute(f"SELECT utilizador_id FROM cliente WHERE utilizador_id = {cliente_msg}")
                            existe = cur.fetchone()
                            if existe is not None:
                                break
                            elif existe is None:
                                print("Não existe um cliente com o ID indicado")
                        except ValueError:
                            print("ID não válido\n")


                    while True:
                        texto = input("ESCREVA A MENSAGEM: \n")
                        verif_geral = input("Confirma que é esta a mensagem a enviar?(S/N)")
                        if verif_geral == "S" or verif_geral == "s":
                            try:
                                print("Mensagem Confirmada")
                                #Inserir mensagem na tabela mensagens
                                cur.execute(f"INSERT INTO mensagem(id, corpo) VALUES (DEFAULT, '{texto}') RETURNING id;")
                                id_mensagem = cur.fetchone()[0]
                                #Registar mensagem na tabela mensagem_administrador
                                cur.execute(f"INSERT INTO mensagem_administrador(mensagem_id, administrador_utilizador_id) VALUES ({id_mensagem}, {utilizador_atual});")
                                #Registar mensagem na tabela cliente_mensagem
                                cur.execute(f"INSERT INTO cliente_mensagem(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {cliente_msg});")

                                tentativas = 3
                                sair = False
                                while tentativas > 0:
                                    confirmar = getpass("Introduza a sua chave de administrador para confirmar o envio da mensagem:\n")
                                    cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                                    chave = cur.fetchone()[0]
                                    if confirmar == chave:
                                        print("MENSAGEM INDIDUAL ENVIADA ")
                                        conn.commit()
                                        sair = True
                                        break
                                    else:
                                        tentativas -= 1
                                        print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                                        if tentativas == 0:
                                            print("\nEnvio da mensagem cancelado!")
                                            conn.rollback()
                                            sair = True
                                            break
                                if (sair == True):
                                    break

                            except:
                                conn.rollback()
                                print("ERRO: MENSAGEM INDIDUAL ANULADA ")
                        elif verif_geral == "N" or verif_geral == "n":
                            print("Mensagem Eliminada")
                            break
                        else:
                            print("Opção inválida")
                            break

                elif voltar == "v" or voltar == "V":
                    print("A VOLTAR AO MENU")
                    mensagensa = False
                    break
                else:
                    print("")
        if msg == "v" or msg == "V":
            break


#==========================================================================================================================
#Menu ADMIN - Adicionar Artigos
def admin_adicionarartigo():
    while True:
        print("\n-------------------------------------Adicionar Artigo-----------------------------------------------\n")

        #Título
        while True:
            novo_titulo = input("Titulo do novo artigo: ")
            validar = input("\nConfirma o titulo do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nTitulo descartado")
            else:
                print("\nOpção inválida")

        #Tipo
        while True:
            novo_tipo = input("Tipo de artigo\n1 - Filme\n2 - Documentário\n3 - Série\n")
            if novo_tipo == "1" or novo_tipo == "2" or novo_tipo == "3":
                validar = input("Confirma o tipo do artigo a introduzir? (S/N)\n")
                if validar == "S" or validar == "s":
                    if novo_tipo == "1":
                        novo_tipo = "filme"
                    elif novo_tipo == "2":
                        novo_tipo = "documentario"
                    elif novo_tipo == "3":
                        novo_tipo = "serie"
                    break
                if validar == "N" or validar == "n":
                    print("\nTipo descartado")
                else:
                    print("\nOpção inválida")
            else:
                print("\nOpção inválida")

        #Realizador
        while True:
            novo_realizador = input("Realizador do novo artigo: ")
            validar = input("\nConfirma o realizador do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nRealizador descartado")
            else:
                print("\nOpção inválida")

        #Produtor
        while True:
            novo_produtor = input("Produtor do novo artigo: ")
            validar = input("\nConfirma o produtor do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nProdutor descartado")
            else:
                print("\nOpção inválida")

        #Ano
        while True:
            ano_atual = datetime.datetime.now()
            ano_atual = int(ano_atual.strftime("%Y"))
            try:
                novo_ano = int(input("Ano do novo artigo: "))

                if novo_ano < 1895 or novo_ano > ano_atual:
                    print("Valor não válido")
                else:
                    validar = input("\nConfirma o ano do artigo a introduzir? (S/N)\n")
                    if validar == "S" or validar == "s":
                        break
                    if validar == "N" or validar == "n":
                        print("\nAno descartado")
                    else:
                        print("\nOpção inválida")
            except ValueError:
                print("Valor não válido")

        #Periodo de aluguer
        while True:
            try:
                novo_periodoaluguer = int(input("Especifique o periodo de aluguer do novo artigo (em meses): "))
                if novo_periodoaluguer > 0:
                    validar = input("\nConfirma o periodo de aluguer do artigo a introduzir? (S/N)\n")
                    if validar == "S" or validar == "s":
                        break
                    if validar == "N" or validar == "n":
                        print("\nPeriodo de aluguer descartado")
                    else:
                        print("\nOpção inválida")
                else:
                    print("Valor inválido")
            except:
                print("\nValor inválido")

        #Adicionar preço
        while True:
            try:
                novo_preco = float(input("Especifique o preço do novo artigo: "))
                if novo_preco >= 0:
                    validar = input("\nConfirma o preço do artigo a introduzir? (S/N)\n")
                    if validar == "S" or validar == "s":
                        break
                    if validar == "N" or validar == "n":
                        print("\nPreço descartado")
                    else:
                        print("\nOpção inválida")
                else:
                    print("Valor inválido")
            except:
                print("\nValor inválido")

        #Efetuar Registo
        try:
            cur.execute(f"INSERT INTO artigo(id, titulo, tipo, realizador, produtor, ano, periodo_de_aluguer) VALUES (DEFAULT, '{novo_titulo}', '{novo_tipo}', '{novo_realizador}', '{novo_produtor}', {novo_ano}, {novo_periodoaluguer}) RETURNING id;")
            id_artigo = cur.fetchone()[0]
            cur.execute(f"INSERT INTO historico_precos(id,preco,entrada_em_vigor,atual,artigo_id) VALUES (DEFAULT, {novo_preco}, CURRENT_TIMESTAMP, True , {id_artigo});")
            perguntar = input("Pretende associar atores a este artigo? (S/N)\n")
            if perguntar == "S" or perguntar == "s":
                while True:
                    ator = input("\nInsira o nome do ator ou atriz a associar a este artigo(Primeiro e Último nome): ")
                    cur.execute(f"SELECT id FROM atores WHERE nome LIKE '%{ator}' AND nome LIKE '{ator}%'")
                    id_ator = cur.fetchone()
                    if id_ator is not None:                         #Ator pertence à base de dados
                        cur.execute(f"INSERT INTO artigo_atores(artigo_id, atores_id) VALUES ({id_artigo},{id_ator[0]});")
                        print(f"\n{ator} participa agora neste artigo")
                        mais = input("Pretende adicionar mais atores ao artigo?(S/N):\n")
                        if mais == "S" or mais == "s":
                            print("")
                        elif mais == "N" or mais == "n":
                            break
                        else:
                            print("Não válido")
                            break
                    elif id_ator is None:                           #Ator não pertence à base de dados
                        while True:
                            saber = input("Ator/atriz não registado/a na base de dados. Pretende adicionar o ator à nossa base de dados?(S/N)")
                            if saber == "S" or saber == "s":
                                while True:                 #Adicionar novo ator
                                    novo = True
                                    nome_novo_ator = input("Nome do novo ator a inserir na base de dados(Primeiro e Último nome): ")
                                    cur.execute(f"SELECT id FROM atores WHERE nome LIKE '%{nome_novo_ator}' AND nome LIKE '{nome_novo_ator}%'")
                                    existe = cur.fetchall()
                                    if len(existe) == 0 :
                                        check = input("Confirma os dados do novo ator a adicionar à base de dados?(S/N):\n")
                                    else:
                                        print("\nAtor/atriz já registado/a na base de dados")
                                        novo = False

                                    if (check == "S" or check == "s") and novo == True:
                                        cur.execute(f"INSERT INTO atores(id, nome) VALUES (DEFAULT,'{nome_novo_ator}') RETURNING id;")
                                        id_novo_ator = cur.fetchone()[0]
                                        cur.execute(f"INSERT INTO artigo_atores(artigo_id, atores_id) VALUES ({id_artigo},{id_novo_ator});")
                                        print(f"\n{nome_novo_ator} participa agora neste artigo")
                                        break
                                    else:
                                        print("Nome não registado")
                                break

                            elif saber == "N" or saber == "n":
                                break

                            else:
                                print("")

                        while True:
                            mais = input("Pretende adicionar mais atores ao artigo?(S/N):\n")
                            if mais == "N" or mais == "n":
                                out = True
                                break
                            elif mais == "S" or mais == "s":
                                print("")
                                out = False
                                break
                            else:
                                print("Valor inválido")


                        if out == True:
                            break


                tentativas = 3
                while tentativas > 0:
                    confirmar = getpass("Introduza a sua chave de administrador para confirmar a introdução do artigo:\n")
                    cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                    chave = cur.fetchone()[0]
                    if confirmar == chave:
                        print("\nArtigo adicionado com sucesso")
                        conn.commit()
                        return
                    else:
                        tentativas -= 1
                        print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                        if tentativas == 0:
                            print("\nAdição de artigo cancelada!")
                            conn.rollback()
                            return


            elif perguntar == "N" or perguntar == "n":
                tentativas = 3
                while tentativas > 0:
                    confirmar = getpass("Introduza a sua chave de administrador para confirmar a introdução do artigo:\n")
                    cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                    chave = cur.fetchone()[0]
                    if confirmar == chave:
                        print("\nArtigo adicionado com sucesso")
                        conn.commit()
                        return
                    else:
                        tentativas -= 1
                        print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                        if tentativas == 0:
                            print("\nAdição de artigo cancelada!")
                            conn.rollback()
                            return

            else:
                print("Valor inválido")
        except:
            print("\nDados Inválidos")
            conn.rollback()


#==========================================================================================================================
#Menu ADMIN - Remover Artigos
def admin_removerartigo():
    while True:
        print("\n-------------------------------------Remover Artigo-----------------------------------------------\n Artigos disponiveis para remoção\n NOTA:(ID,Título, Tipo de Artigo, Realizador, Produtor, Ano, Período de Aluguer)\n\n")
        cur.execute("SELECT (artigo.id, titulo, tipo, realizador, produtor, ano, periodo_de_aluguer) FROM artigo EXCEPT SELECT (artigo.id, titulo, tipo, realizador, produtor, ano, periodo_de_aluguer) FROM artigo INNER JOIN aluguer ON artigo.id = aluguer.artigo_id")

        #Apresentação de artigos possíveis de remoção
        disponiveis = cur.fetchone()
        while disponiveis is not None:
            disponiveis = cur.fetchone()
            if disponiveis is None:
                break
            else:
                print(f"-> {disponiveis[0]}")

        voltar = input("\nENTER - Avançar para a remoção\nV/v - Voltar ao MENU\n\n")

        if voltar == "":
            while True:
                    while True:
                        try:
                            escolha = int(input("Escolha o artigo que deseja remover(ID): "))
                            cur.execute(f"SELECT titulo FROM artigo WHERE id = {escolha}")
                            existe = cur.fetchone()
                            if existe is not None:
                                break
                            elif existe is None:
                                print("Não existe um artigo com o ID indicado")
                        except ValueError:
                            print("ID não válido")


                    validar = input("\nPretende avançar com a remoção? (S/N)\n")
                    if validar == "S" or validar == "s":
                        cur.execute(f"DELETE FROM historico_precos WHERE artigo_id = {escolha}")
                        cur.execute(f"DELETE FROM artigo_atores WHERE artigo_id = {escolha}")
                        cur.execute(f"DELETE FROM artigo WHERE id = {escolha}")

                        tentativas = 3
                        while tentativas > 0:
                            confirmar = getpass("Introduza a sua chave de administrador para confirmar a remoção do artigo:\n")
                            cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                            chave = cur.fetchone()[0]
                            if confirmar == chave:
                                print("\nArtigo removido com sucesso")
                                conn.commit()
                                return
                            else:
                                tentativas -= 1
                                print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                                if tentativas == 0:
                                    print("\nRemoção de artigo cancelada!")
                                    conn.rollback()
                                    return
                        break
                    if validar == "N" or validar == "n":
                        print("\nRemoção cancelada")
                        break
                    else:
                        print("\nOpção inválida")


        elif voltar == "V" or voltar == "v":
            break

    return

#==========================================================================================================================
#Menu ADMIN - Estatísticas
def admin_estatisticas():
    while True:
        print("\n-------------------------------------Estatísticas:-----------------------------------------------\n")

        estatisticas = input("""
                              1 - Número de Clientes
                              2 - Número de artigos
                              3 - Número de artigos por tipo
                              4 - Valor total dos artigos alugados no momento atual
                              5 - Valor total dos alugueres desde sempre
                              6 - Cliente atualmente com mais alugueres
                              7 - Artigo atualmente mais alugado
                              V|v- Voltar

        Ver: """)
        print("\n")

        #---------------------------------------------Numero de clientes--------------------------------------------------
        if estatisticas == "1":
            cur.execute("SELECT count(*) from cliente;")
            nclientes = cur.fetchone()

            if nclientes is None:
                print("Sem clientes registados")
            elif nclientes is not None:
                print("Número total de clientes: ", *nclientes)

        #---------------------------------------------Numero de artigos----------------------------------------------------
        elif estatisticas == "2":
            cur.execute("SELECT count(*) from artigo;")
            nartigos = cur.fetchone()

            if nartigos is None:
                print("Sem artigos registados")
            elif nartigos is not None:
                print("Número total de Artigos: ", *nartigos)

        #------------------------------------------Numero de artigos por tipo-----------------------------------------------
        elif estatisticas == "3":
            cur.execute("SELECT count(tipo) from artigo where tipo like 'filme';")          #Filmes
            nartigos_filme = cur.fetchone()

            if nartigos_filme is None:
                print("Número de Filmes: 0")
            elif nartigos_filme is not None:
                print("Número de Filmes: ", *nartigos_filme)


            cur.execute("SELECT count(tipo) from artigo where tipo like 'serie';")          #Séries
            nartigos_serie = cur.fetchone()

            if nartigos_serie is None:
                print("Número de Séries: 0")
            elif nartigos_serie is not None:
                print("Número de Séries: ", *nartigos_serie)


            cur.execute("SELECT count(tipo) from artigo where tipo like 'documentario';")   #Documentários
            nartigos_doc = cur.fetchone()

            if nartigos_doc is None:
                print("Número de Documentários: 0")
            elif nartigos_doc is not None:
                print("Número de Documentários: ", *nartigos_doc)


        #-----------------------------------Valor total dos artigos alugados no momento atual-------------------------------
        elif estatisticas == "4":
            cur.execute("SELECT sum(preco_aluguer) FROM aluguer WHERE ativo = True;")
            valortotal = cur.fetchone()

            if valortotal[0] is None:
                print("Valor total dos Artigos alugados atualmente: 0€")
            elif valortotal[0] is not None:
                print("Valor total dos Artigos alugados atualmente: ", *valortotal,"€")


        #--------------------------------------Valor total dos alugueres desde sempre---------------------------------------
        elif estatisticas == "5":

            cur.execute("SELECT sum(preco_aluguer) FROM aluguer ;")

            print("Valor total dos Alugueres desde sempre:")
            alugueres = cur.fetchone()

            if alugueres is None:
                print("Resultado não encontrado!")

            while alugueres is not None:
                print("->", *alugueres,"€")
                alugueres = cur.fetchone()

        #------------------------------------------Cliente com mais alugueres-----------------------------------------------
        elif estatisticas == "6":

            cur.execute("SELECT utilizador.nome, '| nº de alugueres:' ,count(*) as total from utilizador join cliente on utilizador.id = cliente.utilizador_id join aluguer on cliente.utilizador_id = aluguer.cliente_utilizador_id where aluguer.ativo = True GROUP by utilizador.nome order by total DESC LIMIT 10;")

            print("TOP 10 -> Cliente atualmente com mais alugueres: ")
            clientemvp = cur.fetchone()

            if clientemvp is None:
                print("Resultado não encontrado!")

            while clientemvp is not None:
                print("->", *clientemvp)
                clientemvp = cur.fetchone()

        #-------------------------------------------------Artigo mais alugado----------------------------------------------
        elif estatisticas == "7":
            cur.execute("SELECT artigo.titulo, '|nº vezes alugado: ', count(*) as total from artigo join aluguer on artigo.id = aluguer.artigo_id where aluguer.ativo = True GROUP by artigo.titulo order by total DESC LIMIT 10;")

            print("TOP 10 - Artigo atualmente mais alugado:")
            artigoalugado = cur.fetchone()

            if artigoalugado is None:
                print("Resultado não encontrado!")

            while artigoalugado is not None:
                print("->", *artigoalugado)
                artigoalugado = cur.fetchone()

        #----------------------------------------------------SAIR-----------------------------------------------------------
        elif estatisticas == "V" or estatisticas== "v":
            print("VOLTAR AO MENU ****")
            return

        else:
            print("Inválido\nTente outra vez")


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                                INÍCIO
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Iniciar programa
inicio()


#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
