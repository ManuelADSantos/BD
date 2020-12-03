import psycopg2

# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

print("Login")
print("Registar")


# mostra todos os resultados
print(cur.fetchall())

# Fecha a ligação à base de dados
cur.close()
conn.close()
