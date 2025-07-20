import psycopg2


# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

# Efectua uma consulta à base de dados
cur.execute("SELECT nome, local, ndep FROM dep where local like '%a';")

for linha in cur.fetchall():
    ndep, nome, local = linha
    print(ndep, nome, local)

# Fecha a ligação à base de dados
cur.close()
conn.close()