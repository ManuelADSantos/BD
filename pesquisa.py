# PESQUISA
# Deve ser possível especificar critérios de ordenação dos resultados.
# Esta funcionalidade deve ser aplicável em dois contextos:
# i) a todos os artigos no sistema;
# ii) aos artigos neste momento alugados pelo cliente.


import psycopg2
import psycopg2.extras

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()


#-----------------------------------------------MENU PESQUISAR-----------------------------------------------------

def menu_pesquisar():

    pesquisarmenu = True

    #PEDE AO CLIENTE QUE TIPO DE PESQUISA QUER EFETUAR
    while pesquisarmenu:
        print("----------------------MENU PESQUISA---------------------")
        print("\n Onde pretende pesquisar? \n")

        pesquisar = input(""" 
                            1 - Pesquisa a todos os artigos do Sistema
                            2 - Pesquisa Artigos Alugados
                            V - Voltar

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
    ordenar = True

    #Pergunta ao cliente que tipo de pesquisa quer fazer
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
                              V - Voltar MENU PESQUISA 
        Pesquisa por: """)

        if pesquisa == "V" or pesquisa == "v":
            pesquisageral = False
            ordenar = False

        print("\n")

        #especificar critérios de ordenação dos resultados
        if ordenar == True:
            ordem = input(""" Ordenação dos resultados:

                                  C - ordem crescente
                                  D - ordem decrescente 
                
            Resposta: """)

        print("\n")

        #.........................................ORDEM CRESCENTE.....................................................
        if pesquisa == "1" and ordem == "C":

            titulo1 = input("Pesquisa por tipo(ordem crescente): \n")

            cur.execute("SELECT titulo from artigo where tipo like '%%s' ORDER by titulo ASC", titulo1)

            p_tipo = cur.fetchone()

            while p_tipo is not None:
                print(p_tipo)
                p_tipo = cur.fetchone()
            # conn.commit()

        elif pesquisa == "2" and ordem == "C":

            titulo2 = input("Pesquisa por título(ordem crescente): \n")

            cur.execute("SELECT titulo from artigo where titulo like '%%s' ORDER by titulo ASC", titulo2)

            p_titulo = cur.fetchone()

            while p_titulo is not None:
                print(p_titulo)
                p_titulo = cur.fetchone()

            # conn.commit()

        elif pesquisa == "3" and ordem == "C":

            titulo3 = input("Pesquisa por Ator(ordem crescente): \n")

            p_atores = cur.execute("SELECT titulo from artigo where ator like '%%s'  ORDER by titulo ASC", titulo3)

            print(p_atores)

        elif pesquisa == "4" and ordem == "C":

            titulo4 = input("Pesquisa por realizador(ordem crescente): \n")

            cur.execute("SELECT titulo from artigo where realizador like '%%s' ORDER by titulo ASC", titulo4)

            p_realizador = cur.fetchone()
            print(p_realizador)

            # while p_realizador is not None:
            #   print(p_realizador)
            #  p_realizador = cur.fetchone()
            # conn.commit()

        elif pesquisa == "5" and ordem == "C":

            titulo5 = input("Pesquisa por produtor(ordem crescente): \n")

            cur.execute("SELECT titulo from artigo where produtor like '%%s' ORDER by titulo ASC", titulo5)

            p_produtor = cur.fetchone()

            while p_produtor is not None:
                print(p_produtor)
                p_produtor = cur.fetchone()

            conn.commit()

        elif pesquisa == "6" and ordem == "C":

            titulo6 = int(input("Pesquisa por Ano(ordem crescente): \n"))

            cur.execute("SELECT Titulo from Artigo where Ano like '%%d' ORDER by titulo ASC", titulo6)

            p_ano: object = cur.fetchall()

            while p_ano is not None:
                print(p_ano)
                p_ano = cur.fetchone()

            conn.commit()

        #..........................................ORDEM DECRESCENTE..................................................
        elif pesquisa == "1" and ordem == "D":

            titulo1 = input("Pesquisa por tipo(ordem decrescente): \n")

            cur.execute("SELECT titulo from artigo where tipo like '%%s' ORDER by titulo ASC", titulo1)

            p_tipo = cur.fetchone()

            while p_tipo is not None:
                print(p_tipo)
                p_tipo = cur.fetchone()
            # conn.commit()

        elif pesquisa == "2" and ordem == "D":

            titulo2 = input("Pesquisa por título(ordem decrescente): \n")

            cur.execute("SELECT titulo from artigo where titulo like '%%s' ORDER by titulo ASC", titulo2)

            p_titulo = cur.fetchone()

            while p_titulo is not None:
                print(p_titulo)
                p_titulo = cur.fetchone()

            # conn.commit()

        elif pesquisa == "3" and ordem == "D":

            titulo3 = input("Pesquisa por Ator(ordem decrescente): \n")

            p_atores = cur.execute("SELECT titulo from artigo where ator like '%%s'  ORDER by titulo ASC", titulo3)

            print(p_atores)

        elif pesquisa == "4" and ordem == "D":

            titulo4 = input("Pesquisa por realizador(ordem decrescente): \n")

            cur.execute("SELECT titulo from artigo where realizador like '%%s' ORDER by titulo ASC", titulo4)

            p_realizador = cur.fetchone()
            print(p_realizador)

            # while p_realizador is not None:
            #   print(p_realizador)
            #  p_realizador = cur.fetchone()
            # conn.commit()

        elif pesquisa == "5" and ordem == "D":

            titulo5 = input("Pesquisa por produtor(ordem decrescente): \n")

            cur.execute("SELECT titulo from artigo where produtor like '%%s' ORDER by titulo ASC", titulo5)

            p_produtor = cur.fetchone()

            while p_produtor is not None:
                print(p_produtor)
                p_produtor = cur.fetchone()

            conn.commit()

        elif pesquisa == "6" and ordem == "D":

            titulo6 = int(input("Pesquisa por Ano(ordem decrescente): \n"))

            cur.execute("SELECT Titulo from Artigo where Ano like '%%d' ORDER by titulo ASC", titulo6)

            p_ano: object = cur.fetchall()

            while p_ano is not None:
                print(p_ano)
                p_ano = cur.fetchone()

            conn.commit()

        elif pesquisa == "V" or pesquisa == "v":
            print("Voltar ao MENU PESQUISA")

        else:
            print("Inválido")
            print("Tenta outra vez")


# -------------------------------------Pesquisa aos artigos neste momento alugados pelo cliente--------------------------
def pesquisa_user():

    pesquisauser = True

    ordenar = True

    while pesquisauser:

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
                              V - Voltar MENU PESQUISA 
        Pesquisa por: """)

        if pesquisa == "V" or pesquisa == "v":
            pesquisauser = False
            ordenar = False

        print("\n")

        # especificar critérios de ordenação dos resultados
        if ordenar == True:
            ordem = input(""" Ordenação dos resultados:

                                  C - ordem crescente
                                  D - ordem decrescente 

            Resposta: """)

        print("\n")

        # .........................................ORDEM CRESCENTE.....................................................
        if pesquisa == "1" and ordem == "C":

            titulo1 = input("Pesquisa por tipo(ordem crescente): \n")

            cur.execute("SELECT titulo from artigo where tipo like '%%s' ORDER by titulo ASC", titulo1)

            p_tipo = cur.fetchone()

            while p_tipo is not None:
                print(p_tipo)
                p_tipo = cur.fetchone()
            # conn.commit()

        elif pesquisa == "2" and ordem == "C":

            titulo2 = input("Pesquisa por título(ordem crescente): \n")

            cur.execute("SELECT titulo from artigo where titulo like '%%s' ORDER by titulo ASC", titulo2)

            p_titulo = cur.fetchone()

            while p_titulo is not None:
                print(p_titulo)
                p_titulo = cur.fetchone()

            # conn.commit()

        elif pesquisa == "3" and ordem == "C":

            titulo3 = input("Pesquisa por Ator(ordem crescente): \n")

            p_atores = cur.execute("SELECT titulo from artigo where ator like '%%s'  ORDER by titulo ASC", titulo3)

            print(p_atores)

        elif pesquisa == "4" and ordem == "C":

            titulo4 = input("Pesquisa por realizador(ordem crescente): \n")

            cur.execute("SELECT titulo from artigo where realizador like '%%s' ORDER by titulo ASC", titulo4)

            p_realizador = cur.fetchone()
            print(p_realizador)

            # while p_realizador is not None:
            #   print(p_realizador)
            #  p_realizador = cur.fetchone()
            # conn.commit()

        elif pesquisa == "5" and ordem == "C":

            titulo5 = input("Pesquisa por produtor(ordem crescente): \n")

            cur.execute("SELECT titulo from artigo where produtor like '%%s' ORDER by titulo ASC", titulo5)

            p_produtor = cur.fetchone()

            while p_produtor is not None:
                print(p_produtor)
                p_produtor = cur.fetchone()

            conn.commit()

        elif pesquisa == "6" and ordem == "C":

            titulo6 = int(input("Pesquisa por Ano(ordem crescente): \n"))

            cur.execute("SELECT Titulo from Artigo where Ano like '%%d' ORDER by titulo ASC", titulo6)

            p_ano: object = cur.fetchall()

            while p_ano is not None:
                print(p_ano)
                p_ano = cur.fetchone()

            conn.commit()

        # ..........................................ORDEM DECRESCENTE..................................................
        elif pesquisa == "1" and ordem == "D":

            titulo1 = input("Pesquisa por tipo(ordem decrescente): \n")

            cur.execute("SELECT titulo from artigo where tipo like '%%s' ORDER by titulo ASC", titulo1)

            p_tipo = cur.fetchone()

            while p_tipo is not None:
                print(p_tipo)
                p_tipo = cur.fetchone()
            # conn.commit()

        elif pesquisa == "2" and ordem == "D":

            titulo2 = input("Pesquisa por título(ordem decrescente): \n")

            cur.execute("SELECT titulo from artigo where titulo like '%%s' ORDER by titulo ASC", titulo2)

            p_titulo = cur.fetchone()

            while p_titulo is not None:
                print(p_titulo)
                p_titulo = cur.fetchone()

            # conn.commit()

        elif pesquisa == "3" and ordem == "D":

            titulo3 = input("Pesquisa por Ator(ordem decrescente): \n")

            p_atores = cur.execute("SELECT titulo from artigo where ator like '%%s'  ORDER by titulo ASC", titulo3)

            print(p_atores)

        elif pesquisa == "4" and ordem == "D":

            titulo4 = input("Pesquisa por realizador(ordem decrescente): \n")

            cur.execute("SELECT titulo from artigo where realizador like '%%s' ORDER by titulo ASC", titulo4)

            p_realizador = cur.fetchone()
            print(p_realizador)

            # while p_realizador is not None:
            #   print(p_realizador)
            #  p_realizador = cur.fetchone()
            # conn.commit()

        elif pesquisa == "5" and ordem == "D":

            titulo5 = input("Pesquisa por produtor(ordem decrescente): \n")

            cur.execute("SELECT titulo from artigo where produtor like '%%s' ORDER by titulo ASC", titulo5)

            p_produtor = cur.fetchone()

            while p_produtor is not None:
                print(p_produtor)
                p_produtor = cur.fetchone()

            conn.commit()

        elif pesquisa == "6" and ordem == "D":

            titulo6 = int(input("Pesquisa por Ano(ordem decrescente): \n"))

            cur.execute("SELECT Titulo from Artigo where Ano like '%%d' ORDER by titulo ASC", titulo6)

            p_ano: object = cur.fetchall()

            while p_ano is not None:
                print(p_ano)
                p_ano = cur.fetchone()

            conn.commit()

        elif pesquisa == "V" or pesquisa == "v":
            print("Voltar ao MENU PESQUISA")

        else:
            ordenar == False
            print("Inválido")
            print("Tenta outra vez")


menu_pesquisar()

# Fecha a ligação à base de dados
cur.close()
conn.close()
