import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor()

# Faz uma inserção na base de dados
cur.execute("DELETE FROM dep WHERE ndep = 60")

# Importante! Torna as alterações à base de dados persistentes
conn.commit()
cur.close()
conn.close()
