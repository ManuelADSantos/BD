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

cur.execute(f"SELECT DISTINCT leitura.mensagem_id, corpo, administrador_utilizador_id FROM mensagem, leitura, mensagem_administrador WHERE leitura.lida IS NOT NULL AND leitura.cliente_utilizador_id = {utilizador_atual} AND mensagem.id = leitura.mensagem_id ORDER BY mensagem_id ASC;")
dados = cur.fetchall()
print(dados)
print(len(dados))
for i in range(len(dados)):
    print(dados[i])
    print(dados[i][0])  #ID MENSAGEM
    print(dados[i][1])  #CORPO
    print(dados[i][2])  #ID ADMIN

# #ID da mensagem
# id_mensagem = dados[ind][0]
#
# #Corpo da mensagem
# if len(dados[ind][1]) > 15:
#     corpo = ""
#     for i in range(12):
#         corpo += dados[ind][1][1]
#     corpo += "  [...]"
# else:
#     corpo = dados[ind][1]
#
# #Administrador que enviou a mensagem
# admin_id = dados[ind][2]
# cur.execute(f"SELECT nome FROM utilizador WHERE id = {admin_id}")
# admin = cur.fetchone()[0]
#
# #Mostrar resulado
# print(f"ID: {id_mensagem} |Remetente: {admin} |Corpo: {corpo}")
# dados = cur.fetchone()
#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
