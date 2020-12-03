import psycopg2

# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

#Iniciar sessão
print("Bem vindo ao NETFLOX")
print("1 - Login")
print("2 - Registar")
iniciar_sessao = input("")

case



# Fecha a ligação à base de dados
cur.close()
conn.close()
