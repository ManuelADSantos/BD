# PESQUISA
#Deve ser possível especificar critérios de ordenação dos resultados.
# Esta funcionalidade deve ser aplicável em dois contextos:
# i) a todos os artigos no sistema;
# ii) aos artigos neste momento alugados pelo cliente.


import psycopg2

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

pesquisageral = True

while pesquisageral:

    print("-------------------------------Pesquisa a todos os artigos do sistema:-----------------------------------------------")
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

    if pesquisa == "1":

        titulo1 = input("Pesquisa por tipo: \n")

        cur.execute("SELECT titulo from artigo where tipo = %s ORDER by titulo ASC", titulo1)

        p_tipo = cur.fetchone()

        while p_tipo is not None:
            print(p_tipo)
            p_tipo = cur.fetchone()
        #conn.commit()

    elif pesquisa == "2":

        titulo2 = input("Pesquisa por título: \n")

        cur.execute("SELECT titulo from artigo where titulo = %s ORDER by titulo ASC", titulo2)

        p_titulo = cur.fetchone()

        while p_titulo is not None:
            print(p_titulo)
            p_titulo = cur.fetchone()

        #conn.commit()

    elif pesquisa == "3":

        titulo3 = input("Pesquisa por Ator: \n")

        p_atores = cur.execute("SELECT titulo from artigo where ator = %s  ORDER by titulo ASC", titulo3)

        print(p_atores)

    elif pesquisa == "4":

        titulo4 = input("Pesquisa por realizador: \n")

        cur.execute("SELECT titulo from artigo where realizador = %s ORDER by titulo ASC", titulo4)

        p_realizador = cur.fetchall()

        while p_realizador is not None:
            print(p_realizador)
            p_realizador = cur.fetchone()
        conn.commit()

    elif pesquisa == "5":

        titulo5 = input("Pesquisa por produtor: \n")

        cur.execute("SELECT titulo from artigo where produtor = %s ORDER by titulo ASC", titulo5)

        p_produtor = cur.fetchall()

        while p_produtor is not None:
            print(p_produtor)
            p_produtor = cur.fetchone()

        conn.commit()

    elif pesquisa == "6":

        titulo6 = int(input("Pesquisa por Ano: \n"))

        cur.execute("SELECT Titulo from Artigo where Ano = %s ORDER by titulo ASC", titulo6)

        p_ano = cur.fetchall()

        while p_ano is not None:
            print(p_ano)
            p_ano = cur.fetchone()

        conn.commit()

    elif pesquisa == "7":

        pesquisageral = False

    else:
        print("Inválido")
        print("Tenta outra vez")

# Fecha a ligação à base de dados
cur.close()
conn.close()
