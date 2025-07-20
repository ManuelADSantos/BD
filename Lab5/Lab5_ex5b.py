import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor()

cur.execute("SELECT nemp FROM emp WHERE nemp=1839")

primeira_linha = cur.fetchone()
if cur.rowcount > 0 :
        print(primeira_linha)

cur.close()
conn.close()
