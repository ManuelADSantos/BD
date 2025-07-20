import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor()

num = 1839
cur.execute("SELECT * FROM emp WHERE nemp=%s", (1839,))
print(cur.fetchone())


# Importante! Torna as alterações à base de dados persistentes
conn.commit()
cur.close()
conn.close()
