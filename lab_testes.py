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
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#==========================================================================================================================
#Variáveis globais
utilizador_atual = 2    #Utilizador com login efetuado
#==========================================================================================================================

#Registar mensagem na tabela leitura

id_mensagem = 1
cur.execute("SELECT utilizador_id FROM cliente")
print("CHECK 3")
for linha in cur.fetchall():
    utilizador_id = linha[0]
    #cur.execute(f"INSERT INTO cliente_mensagem(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {utilizador_id});")
    cur.execute(f"INSERT INTO leitura(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {utilizador_id});")
    print("CHECK 4")
    print(utilizador_id)
conn.commit()

#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
