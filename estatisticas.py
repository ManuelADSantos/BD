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
                          8- Voltar

    Ver: """)
    print("\n")

    # Numero de clientes
    if estatisticas == "1":
        cur.execute("SELECT count(*) from cliente")

        nclientes = cur.fetchone()

        while nclientes is not None:
            print(nclientes)
            nclientes = cur.fetchone()

    #Numero de artigos
    elif estatisticas == "2":
        cur.execute("SELECT count(*) from artigo")

        nartigos = cur.fetchone()
        print(nartigos)
       # while nartigos is not None:
            #print(nartigos)
           # nartigos = cur.fetchone()

    #Numero de artigos por tipo
    elif estatisticas == "3":

        pesqtipo = input("Qual tipo?: ")

        cur.execute("SELECT count(tipo) from artigo where tipo = %s", pesqtipo)

        nartigos_tipo = cur.fetchone()
        print(nartigos_tipo)

    #Valor total dos artigos alugados no momento atual
    elif estatisticas == "4":
        cur.execute("SELECT count(preco) from historico_precos, aluguer where atual = true AND ativo = true")

        valortotal = cur.fetchone()
        print(valortotal)

    #Valor total dos alugueres desde sempre
    elif estatisticas == "5":

        cur.execute("SELECT count(preco) from historico_precos")

        alugueres = cur.fetchone()
        print(alugueres)

    #Cliente com mais alugueres
    elif estatisticas == "6":
        cur.execute("SELECT nome from utilizador where aluguer.ativo = true AND max(ativo) ")

        clientemvp =cur.fetchone()
        print(clientemvp)

    #Artigo mais alugado
    elif estatisticas == "7":
        cur.execute("SELECT titulo from artigo where aluguer = max(*)")

        artigoalugado = cur.fetchone()
        print(artigoalugado)

    elif estatisticas == "8":
        estatistica = False

    else:
        print("Inválido")
        print("Tenta outra vez")
# Fecha a ligação à base de dados
cur.close()
conn.close()
