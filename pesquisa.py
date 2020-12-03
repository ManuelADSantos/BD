#PESQUISA

import psycopg2

    # A função connect permite estabelecer uma ligação a uma base de dados
    # Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

    # Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

while (1):

    print("-------------------------------------Pesquisa:-----------------------------------------------")
    print("\n Como pretende pesquisar? \n")

    pesquisa = input("""
                          1 - Tipo
                          2 - Titulo
                          3 - Ator
                          4 - Realizador
                          5 - Produtor
                          6 - Ano
                          7 - Voltar

                         Pesquisa por: """)
    print("\n")

    if pesquisa == "1" :

            titulo1 = input("Pesquisa por tipo: \n")

            cur.execute("SELECT titulo from artigo where tipo = 'titulo1' ORDER by titulo ASC")

            p_tipo = cur.fetchone()

            while p_tipo is not None:
                print(p_tipo)
                p_tipo = cur.fetchone()

    elif pesquisa == "2":

            titulo2 = input ("Pesquisa por título: \n")

            p_titulo = cur.execute("SELECT titulo from artigo where titulo = 'titulo2' ORDER by titulo ASC")

            print(p_titulo)

    elif pesquisa =="3":

            titulo3 = input ("Pesquisa por Ator: \n")

            p_atores = cur.execute("SELECT Titulo from Artigo where Ator = titulo3 ORDER by ASC")

            print(p_atores)

    elif pesquisa == "4":

            titulo4 = input("Pesquisa por realizador: \n")

            p_realizador = cur.execute("SELECT Titulo from Artigo where Realizador = ORDER by ASC")

            print(p_realizador)

    elif pesquisa == "5":

            titulo5 = input("Pesquisa por produtor: \n")

            p_produtor = cur.execute("SELECT Titulo from Artigo where Produtor = titulo5 ORDER by ASC")

            print(p_produtor)

    elif pesquisa == "6":

            titulo6 = input("Pesquisa por Ano: \n")

            p_ano = cur.execute("SELECT Titulo from Artigo where Ano = titulo6 ORDER by ASC")

            print(p_ano)

    elif pesquisa == "7":

        break

    else:
            print("Inválido")
            print("Tenta outra vez")


# Fecha a ligação à base de dados
cur.close()
conn.close()
