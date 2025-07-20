import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor()

min = 100000
max = 200000
cur.execute("select * from emp where sal > %s and sal < %s", (min, max))

# Importante! Torna as alterações à base de dados persistentes
conn.commit()
cur.close()
conn.close()
