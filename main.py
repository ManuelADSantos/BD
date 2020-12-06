import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass
import os


#==========================================================================================================================
# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

#==========================================================================================================================
#Variáveis globais
utilizador_atual = 0    #Utilizador com login efetuado


#==========================================================================================================================
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
                menu_admin()
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
        cur.execute(f"SELECT COUNT(email) FROM utilizador WHERE email LIKE '%{email}'")
        email_verif = cur.fetchone()
        if (email_verif[0]==1):
            while True:
                password = getpass("\n\t\t        || Password ||\n\t\t\t     ")
                cur.execute(f"SELECT password FROM utilizador WHERE email LIKE '%{email}'")
                password_verif = cur.fetchone()
                if(sha256_crypt.verify(password ,password_verif[0])):
                    print("\nInicio de sessão bem sucedida\n")
                    break
                else:
                    print("\nPassword errada")
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
            cur.execute(f"SELECT COUNT(email) from utilizador where email like '%{email}'")
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
            print("Dados não válidos")


#==========================================================================================================================
#Menu CLIENTE


#==========================================================================================================================
#Menu ADMIN
def menu_admin():
    while True:
        print("\n-------------------------------------MENU ADMIN-----------------------------------------------\n")

        escolha_admin = input("""
                              1 - Estatísticas
                              V|v- Logout

        Ver: """)

        if escolha_admin == "1":
            admin_estatisticas()

        elif escolha_admin == "V" or escolha_admin== "v":
            print("LOGOUT")
            return

        else:
            print("Inválido\nTenta outra vez")


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
                              6 - Cliente com mais alugueres
                              7 - Artigo mais alugado
                              V|v- Voltar

        Ver: """)
        print("\n")

        #---------------------------------------------Numero de clientes--------------------------------------------------

        if estatisticas == "1":
            cur.execute("SELECT count(*) from cliente;")

            print("Número total de clientes: ")
            nclientes = cur.fetchone()

            if nclientes is None:
                print("Resultado não encontrado!")

            while nclientes is not None:
                print("->", *nclientes)
                nclientes = cur.fetchone()

        #---------------------------------------------Numero de artigos----------------------------------------------------
        elif estatisticas == "2":
            cur.execute("SELECT count(*) from artigo;")

            print("Número total de Artigos: ")
            nclientes = cur.fetchone()

            if nclientes is None:
                print("Resultado não encontrado!")

            while nclientes is not None:
                print("->", *nclientes)
                nclientes = cur.fetchone()

        #------------------------------------------Numero de artigos por tipo-----------------------------------------------
        elif estatisticas == "3":

            pesqtipo = input("Qual tipo?: ")

            cur.execute(f"SELECT count(tipo) from artigo where tipo like '%{pesqtipo}';")

            print("Numéro de artigos do TIPO:", pesqtipo)
            nartigos_tipo = cur.fetchone()

            if nartigos_tipo is None:
                print("Resultado não encontrado!")

            while nartigos_tipo is not None:
                print("->", *nartigos_tipo)
                nartigos_tipo = cur.fetchone()

        #-----------------------------------Valor total dos artigos alugados no momento atual-------------------------------
        elif estatisticas == "4":
            cur.execute("SELECT sum(historico_precos.preco) from historico_precos join artigo on historico_precos.artigo_id = artigo.id join aluguer on artigo.id = aluguer.artigo_id where historico_precos.atual = True AND aluguer.ativo = True;")

            print("Valor total dos Artigos alugados atualmente:")
            valortotal = cur.fetchone()

            if valortotal is None:
                print("Resultado não encontrado!")

            while valortotal is not None:
                print("->", *valortotal)
                valortotal = cur.fetchone()

        #--------------------------------------Valor total dos alugueres desde sempre---------------------------------------
        elif estatisticas == "5":

            cur.execute("SELECT sum(preco) from historico_precos;")

            print("Valor total dos Alugueres desde sempre:")
            alugueres = cur.fetchone()

            if alugueres is None:
                print("Resultado não encontrado!")

            while alugueres is not None:
                print("->", *alugueres)
                alugueres = cur.fetchone()

        #------------------------------------------Cliente com mais alugueres-----------------------------------------------
        elif estatisticas == "6":

            cur.execute("SELECT utilizador.nome, '| nº de alugueres:' ,count(*) as total from utilizador join cliente on utilizador.id = cliente.utilizador_id join aluguer on cliente.utilizador_id = aluguer.cliente_utilizador_id where aluguer.ativo = True GROUP by utilizador.nome order by total DESC LIMIT 10;")

            print("TOP 10 -> Cliente com mais alugueres: ")
            clientemvp = cur.fetchone()

            if clientemvp is None:
                print("Resultado não encontrado!")

            while clientemvp is not None:
                print("->", *clientemvp)
                clientemvp = cur.fetchone()

        #-------------------------------------------------Artigo mais alugado----------------------------------------------
        elif estatisticas == "7":
            cur.execute("SELECT artigo.titulo, '|nº vezes alugado: ', count(*) as total from artigo join aluguer on artigo.id = aluguer.artigo_id where aluguer.ativo = True GROUP by artigo.titulo order by total DESC LIMIT 10;")

            print("TOP 10 - Artigo mais alugado atualmente:")
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
            print("Inválido\nTenta outra vez")

#==========================================================================================================================
#Iniciar programa
inicio()







#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
