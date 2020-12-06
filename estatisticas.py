# Estatísticas

import psycopg2

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

estatistica = True

while estatistica:

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
        estatistica = False

    else:
        print("Inválido")
        print("Tenta outra vez")

# Fecha a ligação à base de dados
cur.close()
conn.close()
