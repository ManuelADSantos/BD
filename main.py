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
                #Diferenciar entre admin e cliente
                cur.execute(f"SELECT * FROM administrador where utilizador_id = {utilizador_atual}")
                ser_admin = cur.fetchone()
                if ser_admin is not None:       #ADMIN
                    menu_admin()
                elif ser_admin is None:         #CLIENTE
                    print("MENU CLIENTE")

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
                    cur.execute(f"SELECT id FROM utilizador WHERE email LIKE '%{email}'")
                    global utilizador_atual
                    utilizador_atual = cur.fetchone()[0]
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
                              2 - Adicionar Artigo
                              V|v- Logout

        Ver: """)

        if escolha_admin == "1":
            admin_estatisticas()

        elif escolha_admin == "2":
            admin_adicionarartigo()

        elif escolha_admin == "V" or escolha_admin== "v":
            print("LOGOUT")
            return

        else:
            print("Inválido\nTenta outra vez")


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
            novo_ano = int(input("Ano do novo artigo: "))
            validar = input("\nConfirma o ano do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nAno descartado")
            else:
                print("\nOpção inválida")

        #Periodo de aluguer
        while True:
            novo_periodoaluguer = int(input("Especifique o periodo de aluguer do novo artigo (em meses): "))
            validar = input("\nConfirma o periodo de aluguer do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nPeriodo de aluguer descartado")
            else:
                print("\nOpção inválida")

        #Efetuar Registo
        try:
            cur.execute(f"INSERT INTO artigo(id, titulo, tipo, realizador, produtor, ano, periodo_de_aluguer) VALUES (DEFAULT, '{novo_titulo}', '{novo_tipo}', '{novo_realizador}', '{novo_produtor}', {novo_ano}, {novo_periodoaluguer}) RETURNING id;")
            id_artigo = cur.fetchone()[0]
            perguntar = input("Pretende associar atores a este artigo? (S/N)\n")
            if perguntar == "S" or perguntar == "s":
                while True:
                    ator = input("\nInsira o nome do ator ou atriz a associar a este artigo(Primeiro e Último nome): ")
                    cur.execute(f"SELECT id FROM atores WHERE nome LIKE '%{ator}'")
                    id_ator = cur.fetchone()
                    if id_ator is not None:                         #Ator pertence à base de dados
                        cur.execute(f"INSERT INTO artigo_atores(artigo_id, atores_id) VALUES ({id_artigo},{id_ator[0]});")
                        print(f"\n{ator} participa agora neste artigo")
                        mais = input("Pretende adicionar mais atores ao artigo?(S/N):\n")
                        if mais == "S" or mais == "s":
                            print("")
                        else:
                            break
                    elif id_ator is None:                           #Ator não pertence à base de dados
                        print("Ator/atriz não registado/a na base de dados")
                        while True:                 #Adicionar novo ator
                            nome_novo_ator = input("Nome do novo ator a inserir na base de dados(Primeiro e Último nome): ")
                            check = input("Confirma os dados do novo ator a adicionar à base de dados?(S/N):\n")
                            if check == "S" or check == "s":
                                cur.execute(f"INSERT INTO atores(id, nome) VALUES (DEFAULT,'{nome_novo_ator}') RETURNING id;")
                                id_novo_ator = cur.fetchone()[0]
                                cur.execute(f"INSERT INTO artigo_atores(artigo_id, atores_id) VALUES ({id_artigo},{id_novo_ator});")
                                break
                            else:
                                print("Nome não registado")

                        mais = input("Pretende adicionar mais atores ao artigo?(S/N):\n")
                        if mais == "S" or mais == "s":
                            print("")
                        else:
                            break

                conn.commit()
                return

            else:
                conn.rollback()
                return

        except:
            print("\nDados Inválidos")



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
            cur.execute("SELECT sum(historico_precos.preco) FROM historico_precos JOIN artigo ON historico_precos.artigo_id = artigo.id JOIN aluguer ON artigo.id = aluguer.artigo_id WHERE historico_precos.atual = True AND aluguer.ativo = True;")
            valortotal = cur.fetchone()

            if valortotal[0] is None:
                print("Valor total dos Artigos alugados atualmente: 0€")
            elif valortotal[0] is not None:
                print("Valor total dos Artigos alugados atualmente: ", *valortotal,"€")


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
            print("Inválido\nTente outra vez")

#==========================================================================================================================
#Iniciar programa
inicio()







#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
