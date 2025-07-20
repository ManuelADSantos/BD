import psycopg2
import psycopg2.extras

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cur.execute("SELECT * FROM dep")

for linha in cur.fetchall():
    x1 = linha['nome']
    x2 = linha['local']
    print(x1, x2)

cur.close()
conn.close()
