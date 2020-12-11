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

cur.execute("SELECT artigo.titulo, '|nº vezes alugado: ', count(*) as total from artigo join aluguer on artigo.id = aluguer.artigo_id where aluguer.ativo = True GROUP by artigo.titulo order by total DESC LIMIT 10;")

print("TOP 10 - Artigo atualmente mais alugado:")
artigoalugado = cur.fetchone()

if artigoalugado is None:
    print("Resultado não encontrado!")

while artigoalugado is not None:
    print("->", *artigoalugado)
    artigoalugado = cur.fetchone()


#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
