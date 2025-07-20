import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor()

cur.execute("SELECT nemp FROM emp WHERE nemp=9")

primeira_linha = cur.fetchone()
print(primeira_linha) # imprime (Decimal('1839'),)
val = primeira_linha # extrai o valor corretamente para a variável val!
print(val) # imprime 1839

cur.close()
conn.close()
