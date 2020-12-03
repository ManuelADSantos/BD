#PESQUISA Esta mal

import psycopg2

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

print("Pesquisa: ")

def pesquisa 

ptitulo =

p_tipo = cur.execute("SELECT titulo from artigo where tipo = ORDER by ASC")

print(p_tipo)

p_titulo = cur.execute("SELECT titulo from artigo ORDER by ASC")

print(p_titulo)

p_atores = cur.execute("SELECT atores from artigo_atores ORDER by ASC")

print(p_atores)

p_realizador = cur.execute("SELECT realizador from artigo ORDER by ASC")

print(p_realizador)

p_produtor = cur.execute("SELECT produtor from artigo ORDER by ASC")

print(p_produtor)

p_ano = cur.execute("SELECT ano from artigo ORDER by ASC")

print(p_ano)

# Fecha a ligação à base de dados
cur.close()
conn.close()
