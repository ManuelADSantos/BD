import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass
import os
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

#==========================================================================================================================
# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#==========================================================================================================================
#Variáveis globais
utilizador_atual = 0            #ID Utilizador com login efetuado
nome_utilizador_atual = ""      #NOME Utilizador com login efetuado

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                             ECRÃ INICIAL
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Início/Ecrã inicial
def inicio():
    atualizar_aluguer()
    while True:
        try:
            print("\n================================================================")
            print("\n|                           INÍCIO                              |")
            print("\n================================================================")
            print("""
                         ____      __
                        |    \    |  |
                        |     \   |  |
                        |  |\  \  |  |
                        |  | \  \ |  |
                        |  |  \  \|  |
                        |  |   \     |
                        |__|    \____|
                """)
            print("""\n\t\t  || Bem vind@ ao NETFLOX ||\n
                          1 - Login\n
                        2 - Registar\n
                          3 - Sair""")

            #Escolha da ação a tomar
            inicio_escolha = int(input("\n\t\t\t      "))
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
    print("\n================================================================")
    print("\n|                             LOGIN                            |")
    print("\n================================================================")
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
                    print("\n\t         Inicio de sessão bem sucedida\n")
                    cur.execute(f"SELECT id, nome FROM utilizador WHERE email LIKE '%{email}' AND email LIKE '{email}%'")
                    dados = cur.fetchone()
                    global utilizador_atual
                    global nome_utilizador_atual
                    utilizador_atual, nome_utilizador_atual = dados
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
        print("\n================================================================")
        print("\n|                            REGISTO                            |")
        print("\n================================================================")
        while True:
            email = input("\n\t\t|| Insira o seu endereço de email ||\n\t\t   ")
            cur.execute(f"SELECT COUNT(email) FROM utilizador WHERE email LIKE '%{email}' AND email LIKE '{email}%'")
            email_verif = cur.fetchone()
            if ("@" in email and email_verif[0]==0 and ' ' not in email and email[0]!= '@' and email[len(email)-1]!='@' and '.' in email):
                print("\n\t\t      Endereço de email válido")
                break
            else:
                print("\n\t           Endereço de email inválido")

        #Registo da Password
        while(True):
            password = getpass("\n\n\t\t    || Insira a sua password ||\n\t\t\t    ")
            password_encriptada = sha256_crypt.hash(password)
            password_verif = getpass("\t\t   || Confirme a sua password ||\n\t\t\t      ")
            if(sha256_crypt.verify(password_verif ,password_encriptada)):
                print("\t                 Password aceite\n")
                break
            else:
                print("\n\t            Passwords não correspondem")

        #Registo do nome
        nickname = input("\n\n\t\t     || Insira o seu nome ||\n\t\t       ")

        #Guardar dados na base de dados
        try:
            cur.execute(f"INSERT INTO utilizador(id, email, password, nome) VALUES (DEFAULT, '{email}', '{password_encriptada}', '{nickname}') RETURNING id;")
            id = cur.fetchone()[0]
            cur.execute(f"INSERT INTO cliente(utilizador_id, saldo) VALUES ({id}, 15);")
            #Confirmar mudanças
            conn.commit()
            #De volta ao início
            print("\n\t\t|| BEM VIND@ À FAMÍLIA NETFLOX ||")
            return
        except:
            conn.rollback()
            print("ERRO NO REGISTO")


#==========================================================================================================================
#Atualizar validade dos alugueres
def atualizar_aluguer():
    cur.execute(f"SELECT data, aluguer.id , periodo_de_aluguer FROM aluguer, artigo WHERE aluguer.artigo_id = artigo.id AND aluguer.ativo = true")
    for linha in cur.fetchall():
        data = linha[0]
        id = linha[1]
        periodo_de_aluguer = linha[2]
        validade = data + relativedelta(months =+ periodo_de_aluguer)
        if(date.today() > validade.date()):
            try:
                cur.execute(f"UPDATE aluguer SET ativo = false WHERE id = id")
                conn.commit()
            except:
                conn.rollback()

    return


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                               CLIENTE
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#==========================================================================================================================
#Menu CLIENTE
def menu_cliente():
    atualizar_aluguer()
    while True:
        print("\n================================================================")
        print("\n|                         MENU CLIENTE                          |")
        print("\n================================================================")
        print(f"\n\t        O que deseja fazer {nome_utilizador_atual}?")


        escolha_cliente = input("""
                         1 - Catálogo
                         2 - Pesquisa
                          3 - Alugar
                      4 - Meus Alugueres
                          5 - Saldo
                        6 - Mensagens
                         V|v- Logout

                               """)

        if escolha_cliente == "1":
            lista_cliente()

        if escolha_cliente == "2":
            pesquisar_clientes()

        if escolha_cliente == "3":
            alugar_cliente()

        if escolha_cliente == "4":
            alugueres_cliente()

        if escolha_cliente == "5":
            saldos_cliente()

        if escolha_cliente == "6":
            mensagens_cliente()

        elif escolha_cliente == "V" or escolha_cliente == "v":
            print("\n\t\t         || LOGOUT ||")
            return


#==========================================================================================================================
#Menu CLIENTE - Saldo
def saldos_cliente():
    #-----------------------------------------------MENU SALDO-----------------------------------------------------

    #PEDE AO CLIENTE QUE TIPO DE PESQUISA QUER EFETUAR
    while True:

        print("\n================================================================")
        print("\n|                            SALDO                             |")
        print("\n================================================================")
        print(f"\n\t      {nome_utilizador_atual}, o seu saldo atual é de ")

        cur.execute(f"SELECT saldo FROM cliente WHERE utilizador_id = '{utilizador_atual}';")

        s1 = cur.fetchone()

        if s1 is None:
            print("Resultado não encontrado!")

        while s1 is not None:
            print("\t\t\t   ", *s1, '€')
            s1 = cur.fetchone()

        s = input("\n\t\t         V|v - Voltar\n\t\t\t       ")

        #Volta ao menu anterior
        if s == "V" or s == "v":
            return

        else:
            print("")


#==========================================================================================================================
#Menu CLIENTE - Mensagens
def mensagens_cliente():
    while True:
        print("\n================================================================")
        print("\n|                           MENSAGENS                          |")
        print("\n================================================================")
        cur.execute(f"SELECT mensagem_id FROM cliente_mensagem WHERE cliente_utilizador_id = {utilizador_atual} EXCEPT SELECT mensagem_id FROM leitura WHERE lida IS NOT NULL AND cliente_utilizador_id = {utilizador_atual};")
        print(f"\n\t            Tem {len(cur.fetchall())} mensagens não lidas ")



        msg = input("""

                  || 1 - MENSAGENS NÃO LIDAS ||
                  || 2 - MENSAGENS JÁ LIDAS  ||
                  ||       V|v - Voltar      ||

                                """)
        if msg == "1":
            while True:
                print("\n\n\t\t || A ABRIR MENSAGENS NÃO LIDAS ||")
                print("\n================================================================")
                print("\n|                     MENSAGENS NÃO LIDAS                      |")
                print("\n================================================================")

                cur.execute(f"SELECT DISTINCT leitura.mensagem_id, corpo FROM mensagem, leitura WHERE leitura.lida IS NULL AND leitura.cliente_utilizador_id = {utilizador_atual} AND mensagem.id = leitura.mensagem_id ORDER BY mensagem_id ASC;")
                corpo = cur.fetchone()
                if corpo is not None:
                    #Corpo da mensagem
                    id_mensagem = corpo[0]
                    print("\n\t\t    || CORPO DA MENSAGEM ||\n\n", corpo[1])

                    #Administrador que enviou a mensagem
                    cur.execute(f"SELECT nome FROM utilizador WHERE id = (SELECT administrador_utilizador_id FROM mensagem_administrador WHERE mensagem_id = {id_mensagem});")
                    print("\n\n    -- De", cur.fetchone()[0], " --")

                    while True:
                        opcao = input("\n\t\t|| ENTER - PRÓXIMA MENSAGEM ||\n\t\t|| v/V - VOLTAR A MENSAGENS ||\n\t\t\t       ")
                        if opcao == "" or opcao == "v" or opcao == "V":
                            print("\n\t\t   || A VOLTAR A MENSAGENS ||")
                            break

                    if opcao == "":
                        cur.execute(f"UPDATE leitura SET lida = CURRENT_TIMESTAMP WHERE cliente_utilizador_id = {utilizador_atual} AND mensagem_id = {id_mensagem};")
                        conn.commit()
                    elif opcao == "v" or opcao == "V":
                        cur.execute(f"UPDATE leitura SET lida = CURRENT_TIMESTAMP WHERE cliente_utilizador_id = {utilizador_atual} AND mensagem_id = {id_mensagem};")
                        conn.commit()
                        break
                else:
                    print("\n\t\t   Não tem mensagens não lidas\n\n\t\t   || A VOLTAR A MENSAGENS ||")
                    break

        elif msg == "2":
            while True:
                print("\n\n\t\t || A ABRIR MENSAGENS JÁ LIDAS ||")
                print("\n================================================================")
                print("\n|                      MENSAGENS JÁ LIDAS                       |")
                print("\n================================================================\n")

                cur.execute(f"SELECT DISTINCT leitura.mensagem_id, corpo, administrador_utilizador_id FROM mensagem, leitura, mensagem_administrador WHERE leitura.lida IS NOT NULL AND leitura.cliente_utilizador_id = {utilizador_atual} AND mensagem.id = leitura.mensagem_id ORDER BY mensagem_id ASC;")
                dados = cur.fetchall()
                if len(dados) == 0:
                    print("\n\t\t   Não tem mensagens já lidas\n\n\t\t   || A VOLTAR A MENSAGENS ||")
                    break
                else:
                    for ind in range(len(dados)):
                        #ID da mensagem
                        id_mensagem = dados[ind][0]

                        #Corpo da mensagem
                        if len(dados[ind][1]) > 15:
                            corpo = ""
                            for i in range(15):
                                corpo += dados[ind][1][i]
                            corpo += "  [...]"
                        else:
                            corpo = dados[ind][1]

                        #Administrador que enviou a mensagem
                        admin_id = dados[ind][2]
                        cur.execute(f"SELECT nome FROM utilizador WHERE id = {admin_id}")
                        admin = cur.fetchone()[0]

                        #Mostrar resulado
                        print("ID: ",id_mensagem, " |Remetente: ",admin," |Corpo: ",corpo)
                    while True:
                        sair = False
                        opcao = input("\n\t        || ID - VER MENSAGEM COMPLETA ||\n\t        ||  v/V - VOLTAR A MENSAGENS  ||\n\t\t\t        ")
                        while True:
                            try:
                                opcao = int(opcao)
                                cur.execute(f"SELECT corpo FROM mensagem WHERE id = {opcao}")
                                valido = cur.fetchone()
                                if valido is None:
                                    print("\n\t\t           ID INVÁLIDO\n")
                                else:
                                    print(f"\n\t\t/\/\/\ MENSAGEM {opcao} COMPLETA /\/\/\ \n")
                                    print("  ", *valido)
                                    print(f"\n\t\t\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ \n")
                                break

                            except:
                                if opcao == "v" or opcao == "V":
                                    print("\n\t\t   || A VOLTAR A MENSAGENS ||")
                                    sair = True
                                    break
                                else:
                                    print("\n\t\t         OPÇÃO INVÁLIDA\n")
                                    break
                        if sair:
                            break

                    break


        elif msg == "v" or msg =="V":
            print("\n\t\t|| A VOLTAR AO MENU PRINCIPAL ||")
            return

        else:
            print("")

#==========================================================================================================================
#Menu CLIENTE - PESQUISAR
def pesquisar_clientes():

    pesquisarmenu = True

    #PEDE AO CLIENTE QUE TIPO DE PESQUISA QUER EFETUAR
    while pesquisarmenu:
        print("\n================================================================")
        print("\n|                          PESQUISA                            |")
        print("\n================================================================")
        print(f"\n\t     O que deseja pesquisar {nome_utilizador_atual}?")

        pesquisar = input("""
         1 - Pesquisa a todos os artigos do Sistema
               2 - Pesquisa a artigos alugados
                   V|v - Voltar atrás

                           """)

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
            print("")


# -----------------------------------------------Pesquisa a todos os artigos do sistema------------------------------------
def pesquisa_geral():
    pesquisageral = True
    ordenar = False
    # Pergunta ao cliente que tipo de pesquisa quer fazer
    while pesquisageral:
        print("\n================================================================")
        print("\n|                    PESQUISA GERAL                            |")
        print("\n================================================================")
        print(f"\n            Como pretende pesquisar {nome_utilizador_atual}? \n")
        pesquisa = input("""
                        1 - Tipo
                        2 - Titulo
                        3 - Ator
                        4 - Realizador
                        5 - Produtor
                        6 - Ano
                V|v - Voltar MENU PESQUISA

                            """)

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

                    ordem = int(input("""\n                   Ordenar resultados por
                    1 - ordem crescente
                    2 - ordem decrescente

                             """))

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

            titulo1 = input("\t\t  || Pesquisa por tipo || \n\t\t\t")

            cur.execute(f"SELECT titulo from artigo where tipo like '%{titulo1}' ORDER by titulo {ordem};")

            p_tipo = cur.fetchone()

            if p_tipo is None:
                print("\n\t\tResultado não encontrado!")

            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")
                while p_tipo is not None:
                    print("-> ", *p_tipo)
                    p_tipo = cur.fetchone()

        # --------------------------------------------PESQUISA POR TITULO-------------------------------------------------
        elif pesquisa == "2":

            titulo2 = input("\t\t  || Pesquisa por titulo || \n\t\t\t")

            cur.execute(f"SELECT titulo FROM artigo WHERE titulo like '%{titulo2}' ORDER by titulo {ordem};")

            p_titulo = cur.fetchone()

            if p_titulo is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")

                while p_titulo is not None:
                    print("->", *p_titulo)
                    p_titulo = cur.fetchone()

        # --------------------------------------------PESQUISA POR ATOR--------------------------------------------------
        elif pesquisa == "3":

            titulo3 = input("\t\t  || Pesquisa por ator || \n\t\t\t")

            cur.execute(
                f"SELECT artigo.titulo from artigo join artigo_atores on artigo.id = artigo_atores.artigo_id join atores on atores.id= artigo_atores.atores_id where atores.nome like '%{titulo3}' ORDER BY titulo {ordem};")

            p_atores = cur.fetchone()

            if p_atores is None:
                print("\n\t\tResultado não encontrado!")

            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")

                while p_atores is not None:
                    print("->", *p_atores)
                    p_atores = cur.fetchone()

        # --------------------------------------------PESQUISA POR REALIZADOR-------------------------------------------------
        elif pesquisa == "4":

            titulo4 = input("\t\t  || Pesquisa por realizador || \n\t\t\t")

            cur.execute(f"SELECT titulo from artigo where realizador like '%{titulo4}' ORDER by titulo {ordem};")


            p_realizador = cur.fetchone()

            if p_realizador is None:
                print("\n\t\tResultado não encontrado!")

            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")
                while p_realizador is not None:
                    print("->", *p_realizador)
                    p_realizador = cur.fetchone()


        # --------------------------------------------PESQUISA POR PRODUTOR-------------------------------------------------
        elif pesquisa == "5":

            titulo5 = input("\t\t  || Pesquisa por produtor || \n\t\t\t")

            cur.execute(f"SELECT titulo from artigo where produtor like '%{titulo5}' ORDER by titulo {ordem};")

            p_produtor = cur.fetchone()

            if p_produtor is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")
                while p_produtor is not None:
                    print("->", *p_produtor)
                    p_produtor = cur.fetchone()

        # --------------------------------------------PESQUISA POR ANO-------------------------------------------------
        elif pesquisa == "6":

            while True:
                try:
                    titulo6 = int(input("\t\t  || Pesquisa por ano || \n\t\t\t"))
                    # a primeira exibição de um filme de curta duração aconteceu no Salão Grand Café, em Paris, em 28 de dezembro de 1895
                    if titulo6 < 1895 or titulo6>=2021:
                        raise ValueError("INSIRA UM ANO VÁLIDO!")
                except ValueError:
                    print("INSIRA UM ANO VÁLIDO!")
                    continue
                else:
                    break

            cur.execute(f"SELECT titulo from artigo where ano = '{titulo6}' ORDER by titulo {ordem};")

            p_ano = cur.fetchone()

            if p_ano is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")

                while p_ano is not None:
                    print("->", *p_ano)
                    p_ano = cur.fetchone()
    return

# -------------------------------------Pesquisa aos artigos neste momento alugados pelo cliente----------------------------
def pesquisa_user():

    cliente_atual = 2
    pesquisauser = True
    ordenar = True

    # Pergunta ao cliente que tipo de pesquisa quer fazer
    while pesquisauser:

        print("\n================================================================")
        print("\n|               PESQUISA ARTIGOS ALUGADOS                       |")
        print("\n================================================================")
        print(f"\n            Como pretende pesquisar {nome_utilizador_atual}? \n")

        pesquisa = input("""
                        1 - Tipo
                        2 - Titulo
                        3 - Ator
                        4 - Realizador
                        5 - Produtor
                        6 - Ano
                V|v - Voltar MENU PESQUISA

                            """)

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

                    ordem = int(input("""\n                   Ordenar resultados por
                    1 - ordem crescente
                    2 - ordem decrescente

                             """))

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

            titulo1 = input("\t\t  || Pesquisa por tipo || \n\t\t\t")

            cur.execute(f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.tipo like '%{titulo1}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")


            p_tipo = cur.fetchone()

            if p_tipo is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")
                while p_tipo is not None:
                    print("->", *p_tipo)
                    p_tipo = cur.fetchone()

        # --------------------------------------------PESQUISA POR TITULO-------------------------------------------------
        elif pesquisa == "2":

            titulo2 = input("\t\t  || Pesquisa por titulo || \n\t\t\t")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.titulo like '%{titulo2}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")


            p_titulo = cur.fetchone()

            if p_titulo is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")
                while p_titulo is not None:
                    print("->", *p_titulo)
                    p_titulo = cur.fetchone()

        # --------------------------------------------PESQUISA POR ATOR-------------------------------------------------
        elif pesquisa == "3":

            titulo3 = input("\t\t  || Pesquisa por ator || \n\t\t\t")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id join artigo_atores on artigo.id = artigo_atores.artigo_id join atores on atores.id= artigo_atores.atores_id where atores.nome like '%{titulo3}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}' ORDER BY titulo {ordem};")


            p_atores = cur.fetchone()

            if p_atores is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")

                while p_atores is not None:
                    print("->", *p_atores)
                    p_atores = cur.fetchone()

        # --------------------------------------------PESQUISA POR REALIZADOR-------------------------------------------------
        elif pesquisa == "4":

            titulo4 = input("\t\t  || Pesquisa por realizador || \n\t\t\t")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.realizador like '%{titulo4}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")


            p_realizador = cur.fetchone()

            if p_realizador is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")
                while p_realizador is not None:
                    print("->", *p_realizador)
                    p_realizador = cur.fetchone()

        # --------------------------------------------PESQUISA POR PRODUTOR-------------------------------------------------
        elif pesquisa == "5":

            titulo5 = input("\t\t  || Pesquisa por produtor || \n\t\t\t")

            cur.execute(
                f"SELECT artigo.titulo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where artigo.produtor like '%{titulo5}' and aluguer.ativo = True and cliente.utilizador_id = '{cliente_atual}'ORDER by titulo {ordem};")


            p_produtor = cur.fetchone()

            if p_produtor is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")

                while p_produtor is not None:
                    print("->", *p_produtor)
                    p_produtor = cur.fetchone()

        # --------------------------------------------PESQUISA POR ANO-------------------------------------------------
        elif pesquisa == "6":

            while True:
                try:
                    titulo6 = int(input("\t\t  || Pesquisa por ano || \n\t\t\t"))
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

            p_ano = cur.fetchone()

            if p_ano is None:
                print("\n\t\tResultado não encontrado!")
            else:
                if ordem == "ASC":
                    print("\nTítulo (ordem crescente):")

                elif ordem == "DESC":
                    print("\nTítulo (ordem decrescente):")

                while p_ano is not None:
                    print("->", *p_ano)
                    p_ano = cur.fetchone()

    return

# -------------------------------------Lista de Alugueres----------------------------
def alugueres_cliente():
    print("\n================================================================")
    print("\n|               DADOS SOBRE OS MEUS ALUGADOS                    |")
    print("\n================================================================")
    print(f"\n                   Dados de {nome_utilizador_atual} \n")

    cur.execute(f"SELECT artigo.titulo, artigo.periodo_de_aluguer, aluguer.data, artigo.tipo, aluguer.preco_aluguer from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where cliente.utilizador_id = '{utilizador_atual}'and aluguer.ativo = True ORDER by aluguer.data DESC;")

    print("\n                   || Alugueres Ativos ||\n")
    for linha in cur.fetchall():
        titulo, periodo_de_aluguer, data, tipo, preco = linha
        print("Título: ", titulo, " | Tipo: ", tipo," | Data de aluguer: ", data.strftime("%d/%m/%Y %H:%M"), "| Periodo de Aluguer: ", periodo_de_aluguer, " meses | Preço de Aluguer: ", preco, "€")

    cur.execute(
        f"SELECT artigo.titulo, artigo.periodo_de_aluguer, aluguer.data, artigo.tipo, aluguer.preco_aluguer from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where cliente.utilizador_id = '{utilizador_atual}' and aluguer.ativo = False ORDER by aluguer.data DESC;")

    print("\n\n                  || Alugueres Não Ativos ||\n")
    for linha in cur.fetchall():
        titulo, periodo_de_aluguer, data, tipo, preco = linha
        print("Título: ", titulo, " | Tipo: ", tipo," | Data de aluguer: ", data.strftime("%d/%m/%Y %H:%M"), "| Periodo de Aluguer: ", periodo_de_aluguer, " meses | Preço de Aluguer: ", preco, "€")

    print("\n\n                || Total Gasto em Alugueres ||")
    cur.execute(f"SELECT coalesce(sum(preco_aluguer), 0) from aluguer where cliente_utilizador_id = {utilizador_atual};")
    p = cur.fetchone()
    print("\n\t\t\t    ", *p, " €")

    print("\n\n          || Total Gasto em Aluguer de Documentários ||")
    cur.execute(f"SELECT coalesce(sum(preco_aluguer), 0) from aluguer join artigo on aluguer.artigo_id = artigo.id where artigo.tipo like '%documentario%' and cliente_utilizador_id = {utilizador_atual};")
    p1 = cur.fetchone()
    print("\n\t\t\t    ", *p1, " €")

    print("\n\n             || Total Gasto em Aluguer de Filmes ||")
    cur.execute(f"SELECT coalesce(sum(preco_aluguer), 0) from aluguer join artigo on aluguer.artigo_id = artigo.id where artigo.tipo like '%filme%' and cliente_utilizador_id = {utilizador_atual};")
    p2 = cur.fetchone()
    print("\n\t\t\t    ", *p2, " €")

    print("\n\n             || Total Gasto em Aluguer de Séries ||")
    cur.execute(f"SELECT coalesce(sum(preco_aluguer), 0) from aluguer join artigo on aluguer.artigo_id = artigo.id where artigo.tipo like '%serie%' and cliente_utilizador_id = {utilizador_atual};")
    p3 = cur.fetchone()
    print("\n\t\t\t    ", *p3, " €")


    print("\n\n\t\t v/V - Voltar ao Menu Cliente")
    while True:
        voltar = input("\t\t\t\t")
        if voltar == "v" or voltar == "V":
            break
    return


#-------------------------------------Catálogo/ Lista de todos os artigos-------------------------------------------------
def lista_cliente():
    while True:
        print("\n================================================================")
        print("\n|                         CATÁLOGO                             |")
        print("\n================================================================")
        print(f"\n            Aqui pode ver todos os nossos artigos {nome_utilizador_atual}\n")

        cur.execute("SELECT id, titulo, tipo from artigo ORDER BY tipo ASC, titulo ASC;")

        for linha in cur.fetchall():
            id, titulo, tipo = linha
            print("Título: ", titulo, "| Tipo: ", tipo, "| ID: ", id)

        det = input("\n\t\t\tV|v - Voltar\n\n\t\t\t\t\t    ")

        # Volta ao Inventário
        if det == "V" or det == "v":
            print("A VOLTAR AO MENU CLIENTE")
            return
        # Input não válido
        else:
            print("\n\t\t\t\t\tInválido")
            print("\t\t\t\t     Tenta outra vez\n")


#----------------------------------------Alugar artigos----------------------------------------------------
def alugar_cliente():
    while True:
        print("\n================================================================")
        print("\n|                      ALUGAR ARTIGOS                          |")
        print("\n================================================================")
        print(f"\n                    O que deseja alugar {nome_utilizador_atual}?\n")
        cur.execute(f"SELECT id, titulo, tipo FROM artigo EXCEPT SELECT artigo.id, titulo, tipo FROM artigo, aluguer WHERE artigo.id = aluguer.artigo_id AND ativo = true AND aluguer.cliente_utilizador_id = {utilizador_atual};")
        for linha in cur.fetchall():
            id, titulo, tipo = linha
            print("Título: ", titulo, "| Tipo: ", tipo, "| ID: ", id)

        artdet = input("\n\t           ID - Artigo a alugar\n\t           v/V - Voltar ao Menu\n\t\t            ")

        if (artdet == "v" or artdet == "V"):
            print("De volta ao MENU")
            return

        try:
            artdet = int(artdet)
            try:
                cur.execute(f"SELECT titulo, tipo, realizador, produtor, ano from artigo where id = '{artdet}';")
                detalhes = cur.fetchone()
                if detalhes is None:
                    print(f"Não existe um artigo com o ID {artdet}")
                else:
                    print("\n\n\t\t  || Detalhes do artigo ||\n")
                    print(
                        f"Título: {detalhes[0]} | Tipo: {detalhes[1]} | Realizador: {detalhes[2]} | Produtor: {detalhes[3]} | Ano: {detalhes[4]} ")

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

                    print("\n\t\t || Condições de aluguer ||\n")

                    cur.execute(f"SELECT periodo_de_aluguer, preco from artigo, historico_precos where artigo.id = {artdet} and historico_precos.atual = True and historico_precos.artigo_id = {artdet};")

                    for linha in cur.fetchall():
                        periodo_de_aluguer, preco = linha
                        print("Período de aluguer(em meses): ", periodo_de_aluguer, "| Preço: ", preco, " €")

                    while True:

                        det1 = input("""\n\n\t\t    Pretende ALUGAR(S|N)?
                            """)

                        if det1 == "S" or det1 == "s":
                            cur.execute(f"SELECT saldo FROM cliente WHERE utilizador_id = {utilizador_atual}")
                            saldo_atual = cur.fetchone()[0]

                            if saldo_atual < preco:
                                print("\n          SALDO INSUFICIENTE PARA ALUGAR ESTE ARTIGO")
                                break
                            else:
                                try:
                                    cur.execute(f"INSERT INTO aluguer (id, data, ativo, artigo_id, cliente_utilizador_id, preco_aluguer) VALUES (DEFAULT, CURRENT_TIMESTAMP, True, {artdet}, {utilizador_atual},{preco});")
                                    conn.commit()
                                    print("\nALUGADO!\n")
                                    break
                                except:
                                    conn.rollback()
                                    print("\nALUGUER CANCELADO!\n")
                                    break

                        elif det1 == "N" or det1 == "n":
                            break
                        else:
                            print("Inválido\nTenta outra vez")

            except:
                print("ERRO!")
        except ValueError:
            print("VALOR INVÁLIDO")

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                               ADMIN
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Menu ADMIN
def menu_admin():
    atualizar_aluguer()
    while True:
        print("\n-------------------------------------MENU ADMIN-----------------------------------------------\n")

        escolha_admin = input("""
                              1 - Estatísticas
                              2 - Adicionar Artigo
                              3 - Remover Artigo
                              4 - Enviar Mensagens
                              5 - Inventário de Artigos(detalhes e histórico de preços)
                              6 - Alterar Saldo de Cliente
                              V|v- Logout

        Ver: """)

        if escolha_admin == "1":
            estatisticas_admin()

        elif escolha_admin == "2":
            adicionarartigo_admin()

        elif escolha_admin == "3":
            removerartigo_admin()

        elif escolha_admin == "4":
            mensagens_admin()

        elif escolha_admin == "5":
            inventario_admin()

        elif escolha_admin == "6":
            alterarsaldo_admin()

        elif escolha_admin == "V" or escolha_admin== "v":
            print("LOGOUT")
            return

        else:
            print("Inválido\nTenta outra vez")


#==========================================================================================================================
#Menu ADMIN - Inventário, detalhes, condições de aluguer histórico de preços
def inventario_admin():
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


# ---------------------------------------------------Histórico de preços---------------------------------------------------
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
def mensagens_admin():
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
                                #Registar mensagem na tabela cliente_mensagem e leitura
                                cur.execute("SELECT utilizador_id FROM cliente")
                                for linha in cur.fetchall():
                                    utilizador_id = linha[0]
                                    cur.execute(f"INSERT INTO cliente_mensagem(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {utilizador_id});")
                                    cur.execute(f"INSERT INTO leitura(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {utilizador_id});")

                                tentativas = 3
                                sair = False
                                while tentativas > 0:
                                    confirmar = getpass("\nIntroduza a sua chave de administrador para confirmar o envio da mensagem:\n")
                                    cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                                    chave = cur.fetchone()[0]
                                    if confirmar == chave:
                                        print("\nMENSAGEM GERAL ENVIADA ")
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
                                #Registar mensagem na tabela leitura
                                cur.execute(f"INSERT INTO leitura(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {cliente_msg});")
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
def adicionarartigo_admin():
    while True:
        print("\n-------------------------------------Adicionar Artigo-----------------------------------------------\n")

        #Título
        while True:
            novo_titulo = input("\nTitulo do novo artigo: ")
            validar = input("\nConfirma o titulo do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nTitulo descartado")
            else:
                print("\nOpção inválida")

        #Tipo
        while True:
            novo_tipo = input("\nTipo de artigo\n1 - Filme\n2 - Documentário\n3 - Série\n")
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
            novo_realizador = input("\nRealizador do novo artigo: ")
            validar = input("\nConfirma o realizador do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nRealizador descartado")
            else:
                print("\nOpção inválida")

        #Produtor
        while True:
            novo_produtor = input("\nProdutor do novo artigo: ")
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
                novo_ano = int(input("\nAno do novo artigo: "))

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
                novo_periodoaluguer = int(input("\nEspecifique o periodo de aluguer do novo artigo (em meses): "))
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
                novo_preco = float(input("\nEspecifique o preço do novo artigo: "))
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
                        mais = input("\nPretende adicionar mais atores ao artigo?(S/N):\n")
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
                                        check = input("\nConfirma os dados do novo ator a adicionar à base de dados?(S/N):\n")
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
                            mais = input("\nPretende adicionar mais atores ao artigo?(S/N):\n")
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
                    confirmar = getpass("\nIntroduza a sua chave de administrador para confirmar a introdução do artigo:\n")
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
                    confirmar = getpass("\nIntroduza a sua chave de administrador para confirmar a introdução do artigo:\n")
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
def removerartigo_admin():
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
def estatisticas_admin():
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


#==========================================================================================================================
#Menu ADMIN - Alterar Saldo
def alterarsaldo_admin():
    while True:
        print("------------------------------- ALTERAR SALDO -------------------------------\n")
        cur.execute("SELECT utilizador_id, nome, saldo FROM cliente, utilizador WHERE cliente.utilizador_id = utilizador.id ORDER BY utilizador_id ASC;")
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



#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#                                                                INÍCIO
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Iniciar programa
inicio()


#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
