import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor()

# Faz uma inserção na base de dados
cur.execute("INSERT INTO dep (ndep, nome, local) VALUES (60, 'Marketing', 'Faro')")

# Importante! Torna as alterações à base de dados persistentes
conn.commit()
cur.close()
conn.close()
