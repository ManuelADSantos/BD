# Estatísticas

import psycopg2

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

estatistica = True

while estatistica:

    print("-------------------------------------Estatísticas:-----------------------------------------------")
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


# Numero de clientes
nclientes = cur.execute("SELECT count(*) from cliente")

print(nclientes)

#Numero de artigos
nartigos = cur.execute("SELECT count(*) from artigo")

print(nartigos)

#Numero de artigos por tipo
nartigos_tipo = cur.execute("SELECT count(tipo) from artigo")

print(nartigos_tipo)

#Valor total dos artigos alugados no momento atual
valortotal = cur.execute("SELECT count(preco) from historico_precos, aluguer where atual = true AND ativo = true")

print(valortotal)

#Valor total dos alugueres desde sempre
alugueres = cur.execute("SELECT count(preco) from historico_precos")

print(alugueres)

#Cliente com mais alugueres

clientemvp = cur.execute("SELECT nome from utilizador, aluguer where ativo = true AND ativo=max(ativo) ")

print(clientemvp)

#Artigo mais alugado
artigoalugado = cur.execute("SELECT titulo from artigo, aluguer where ativo = max(ativo)")

print(artigoalugado)
# Fecha a ligação à base de dados
cur.close()
conn.close()
