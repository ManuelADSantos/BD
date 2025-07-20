import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

cur = conn.cursor()

while True:
    try:
        n = int(input("Enter the number of the department to change: "))
        name = input("Enter the name of the department to change: ")
        sql = "UPDATE dep set nome = '" + name + "' where ndep =" + str(n)
        print(sql)
        cur.execute(sql)
        break
    except ValueError:
        print("Sorry, please review the entered value.")
        continue

# Importante! Torna as alterações à base de dados persistentes
conn.commit()

cur.close()
conn.close()
