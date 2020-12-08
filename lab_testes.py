import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass
import os
import datetime
#==========================================================================================================================
# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

#==========================================================================================================================
#Variáveis globais
utilizador_atual = 1    #Utilizador com login efetuado
#==========================================================================================================================

#cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
#chave = cur.fetchone()[0]
#print(chave)

cur.execute(f"SELECT titulo FROM artigo WHERE id = 307")
ver = cur.fetchone()[0]
print(ver)




#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
