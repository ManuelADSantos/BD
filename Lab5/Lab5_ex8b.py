import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor()

done = False
lista = []

while(not done):
    n = int(input("Insira emp: "))
    if n==0 :
        done = True
    else:
        lista.append(n)

cmd = "("

for i in range(len(lista)):
    if i != 0:
        cmd += ','
    cmd += "%s"

cmd += ")"

sql = "select distinct funcao from emp where nemp in" + cmd

print(sql, tuple(lista))
cur.execute(sql, tuple(lista))
print(cur, cur.fetchall())

# Importante! Torna as alterações à base de dados persistentes
conn.commit()
cur.close()
conn.close()
