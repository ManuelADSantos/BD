import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass
import os
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

#==========================================================================================================================
# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#==========================================================================================================================
#Variáveis globais
utilizador_atual = 0    #Utilizador com login efetuado
#==========================================================================================================================
# Função

def atualizar_aluguer():
    cur.execute(f"SELECT data, aluguer.id , periodo_de_aluguer FROM aluguer, artigo WHERE aluguer.artigo_id = artigo.id AND aluguer.ativo = true")
    for linha in cur.fetchall():
        data = linha[0]
        id = linha[1]
        periodo_de_aluguer = linha[2]
        validade = data + relativedelta(months =+ periodo_de_aluguer)
        print("ID: ",id,"| Período de aluguer: ", periodo_de_aluguer, "| Data: ", data, "|Fim: ", validade)
        if(date.today() < validade.date()):
            try:
                cur.execute(f"UPDATE aluguer SET ativo = false WHERE id = id")
                print("ACABOU")
                conn.commit()
            except:
                conn.rollback()

atualizar_aluguer()


#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()



conn.close()
