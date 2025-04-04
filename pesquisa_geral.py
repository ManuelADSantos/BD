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
pesquisageral = True
ordenar = True
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
        pesquisageral = False
        ordenar = False
        
    print("\n")
    # especificar critérios de ordenação dos resultados
    if ordenar == True:

        while True:
            try:

                ordem = int(input(""" Ordenação dos resultados:
                                      1 - ordem crescente
                                      2 - ordem decrescente)
                ORDEM(1|2): """))

                if ordem != 1 and ordem != 2:
                    raise ValueError("ERRO")
            except ValueError:
                print("ERRO")
                continue
            else:
                break
                return(ordem)

    if ordem == 1:
        ordem = "ASC"
    elif ordem == 2:
        ordem = "DESC"

    print("\n")

    # .........................................ORDEM CRESCENTE.....................................................

    #--------------------------------------------PESQUISA POR TIPO-------------------------------------------------
    if pesquisa == "1":

        titulo1 = input("Pesquisa por tipo (ordem crescente): \n")

        cur.execute(f"SELECT titulo from artigo where tipo like '%{titulo1}' ORDER by titulo '%{ordem}';")

        print("Título (ordem crescente):")

        p_tipo = cur.fetchone()

        if p_tipo is None:
            print("Resultado não encontrado!")

        while p_tipo is not None:
            print("->", *p_tipo)
            p_tipo = cur.fetchone()

    # --------------------------------------------PESQUISA POR TITULO-------------------------------------------------
    elif pesquisa == "2" and ordem == "C":

        titulo2 = input("Pesquisa por título (ordem crescente): \n")

        cur.execute(f"SELECT titulo FROM artigo WHERE titulo like '%{titulo2}' ORDER by titulo ASC;")

        print("Título (ordem crescente):")
        p_titulo = cur.fetchone()

        if p_titulo is None:
            print("Resultado não encontrado!")

        while p_titulo is not None:
            print("->", *p_titulo)
            p_titulo = cur.fetchone()

    # --------------------------------------------PESQUISA POR ATOR--------------------------------------------------
    elif pesquisa == "3" and ordem == "C":

        titulo3 = input("Pesquisa por Ator (ordem crescente): \n")

        cur.execute(f"SELECT artigo.titulo from artigo join artigo_atores on artigo.id = artigo_atores.artigo_id join atores on atores.id= artigo_atores.atores_id where atores.nome like '%{titulo3}' ORDER BY titulo ASC;")

        print("Título (ordem crescente):")

        p_atores = cur.fetchone()

        if p_atores is None:
            print("Resultado não encontrado!")

        while p_atores is not None:
            print("->", *p_atores)
            p_atores = cur.fetchone()

    # --------------------------------------------PESQUISA POR REALIZADOR-------------------------------------------------
    elif pesquisa == "4" and ordem == "C":

        titulo4 = input("Pesquisa por realizador (ordem crescente): \n")

        cur.execute(f"SELECT titulo from artigo where realizador like '%{titulo4}' ORDER by titulo ASC;")

        print("Título (ordem crescente):")

        p_realizador = cur.fetchone()

        if p_realizador is None:
            print("Resultado não encontrado!")

        while p_realizador is not None:
            print("->", *p_realizador)
            p_realizador = cur.fetchone()


    # --------------------------------------------PESQUISA POR PRODUTOR-------------------------------------------------
    elif pesquisa == "5" and ordem == "C":

        titulo5 = input("Pesquisa por produtor (ordem crescente): \n")

        cur.execute(f"SELECT titulo from artigo where produtor like '%{titulo5}' ORDER by titulo ASC;")

        print("Título (ordem crescente):")

        p_produtor = cur.fetchone()

        if p_produtor is None:
            print("Resultado não encontrado!")

        while p_produtor is not None:
            print("->", *p_produtor)
            p_produtor = cur.fetchone()

    # --------------------------------------------PESQUISA POR ANO-------------------------------------------------
    elif pesquisa == "6" and ordem == "C":

        while True:
            try:
                titulo6 = int(input("Pesquisa por Ano (ordem crescente): \n"))
                # a primeira exibição de um filme de curta duração aconteceu no Salão Grand Café, em Paris, em 28 de dezembro de 1895
                if titulo6 < 1895 or titulo6 >= 2021:
                    raise ValueError("INSIRA UM ANO VÁLIDO!")
            except ValueError:
                print("INSIRA UM ANO VÁLIDO!")
                continue
            else:
                break

        cur.execute(f"SELECT titulo from artigo where ano = '{titulo6}' ORDER by titulo ASC;")

        print("Título (ordem crescente):")

        p_ano = cur.fetchone()

        if p_ano is None:
            print("Resultado não encontrado!")


        while p_ano is not None:
            print("->", *p_ano)


            p_ano = cur.fetchone()

    # ..........................................ORDEM DECRESCENTE..................................................
    # --------------------------------------------PESQUISA POR TIPO-------------------------------------------------
    elif pesquisa == "1" and ordem == "D":


        titulo1 = input("Pesquisa por tipo (ordem decrescente): \n")


        cur.execute(f"SELECT titulo from artigo where tipo like '%{titulo1}' ORDER by titulo DESC;")

        print("Título (ordem decrescente):")

        p_tipo = cur.fetchone()

        if p_tipo is None:
            print("Resultado não encontrado!")

        while p_tipo is not None:
            print("->", *p_tipo)

            p_tipo = cur.fetchone()


    # --------------------------------------------PESQUISA POR TITULO-------------------------------------------------
    elif pesquisa == "2" and ordem == "D":

        titulo2 = input("Pesquisa por título (ordem decrescente): \n")

        cur.execute(f"SELECT titulo FROM artigo WHERE titulo like '%{titulo2}' ORDER by titulo DESC;")

        print("Título (ordem decrescente):")
        p_titulo = cur.fetchone()

        if p_titulo is None:
            print("Resultado não encontrado!")

        while p_titulo is not None:
            print("->", *p_titulo)

            p_titulo = cur.fetchone()

    # --------------------------------------------PESQUISA POR ATOR-------------------------------------------------
    elif pesquisa == "3" and ordem == "D":

        titulo3 = input("Pesquisa por Ator (ordem decrescente): \n")

        cur.execute(f"SELECT artigo.titulo from artigo join artigo_atores on artigo.id = artigo_atores.artigo_id join atores on atores.id= artigo_atores.atores_id where atores.nome like '%{titulo3}' ORDER BY titulo DESC;")


        print("Título (ordem decrescente):")


        p_atores = cur.fetchone()


        if p_atores is None:
            print("Resultado não encontrado!")


        while p_atores is not None:
            print("->", *p_atores)
            p_atores = cur.fetchone()


    # --------------------------------------------PESQUISA POR RALIZADOR-------------------------------------------------
    elif pesquisa == "4" and ordem == "D":

        titulo4 = input("Pesquisa por realizador (ordem decrescente): \n")

        cur.execute(f"SELECT titulo from artigo where realizador like '%{titulo4}' ORDER by titulo DESC;")

        print("Título (ordem decrescente):")


        p_realizador = cur.fetchone()


        if p_realizador is None:
            print("Resultado não encontrado!")

        while p_realizador is not None:
            print("->", *p_realizador)


            p_realizador = cur.fetchone()


    # --------------------------------------------PESQUISA POR PRODUTOR-------------------------------------------------
    elif pesquisa == "5" and ordem == "D":


        titulo5 = input("Pesquisa por produtor (ordem decrescente): \n")

        cur.execute(f"SELECT titulo from artigo where produtor like '%{titulo5}' ORDER by titulo DESC;")

        print("Título (ordem decrescente):")


        p_produtor = cur.fetchone()

        if p_produtor is None:
            print("Resultado não encontrado!")

        while p_produtor is not None:
            print("->", *p_produtor)

            p_produtor = cur.fetchone()

    # --------------------------------------------PESQUISA POR ANO-------------------------------------------------
    elif pesquisa == "6" and ordem == "D":

        while True:
            try:
                titulo6 = int(input("Pesquisa por Ano (ordem decrescente): \n"))
                # a primeira exibição de um filme de curta duração aconteceu no Salão Grand Café, em Paris, em 28 de dezembro de 1895
                if titulo6 < 1895 or titulo6 >= 2021:
                    raise ValueError("INSIRA UM ANO VÁLIDO!")
            except ValueError:
                print("INSIRA UM ANO VÁLIDO!")
                continue
            else:
                break


        cur.execute(f"SELECT titulo from artigo where ano = '{titulo6}' ORDER by titulo DESC;")


        print("Título (ordem decrescente):")


        p_ano = cur.fetchone()

        if p_ano is None:
            print("Resultado não encontrado!")

        while p_ano is not None:
            print("->", *p_ano)

            p_ano = cur.fetchone()

    elif pesquisa == "V" or pesquisa == "v":
        print("Voltar ao MENU PESQUISA")

    else:
        print("Inválido!")
        print("Tenta outra vez \n")

# Fecha a ligação à base de dados
cur.close()
conn.close()
