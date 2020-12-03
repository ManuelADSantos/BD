import psycopg2

# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

#Iniciar sessão
print("1 - Login")
print("2 - Registar")




# Fecha a ligação à base de dados
cur.close()
conn.close()
