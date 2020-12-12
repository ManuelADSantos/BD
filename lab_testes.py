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

def alugar_cliente():
    while True:
        print("---------------------------------ARTIGOS PARA ALUGAR----------------------------------------")
        cur.execute(f"SELECT id, titulo, tipo FROM artigo EXCEPT SELECT artigo.id, titulo, tipo FROM artigo, aluguer WHERE artigo.id = aluguer.artigo_id AND ativo = true AND aluguer.cliente_utilizador_id = {utilizador_atual};")
        for linha in cur.fetchall():
            id, titulo, tipo = linha
            print("Título: ", titulo, "| Tipo: ", tipo, "| ID: ", id)

        artdet = input("\n\t\t\t         ID - Artigo a alugar\n\t\t\t         v/V - Voltar ao Menu\n\t\t\t\t       ")

        if (artdet == "v" or artdet == "V"):
            print("De volta ao MENU")
            break

        try:
            artdet = int(artdet)
            try:
                cur.execute(f"SELECT titulo, tipo, realizador, produtor, ano from artigo where id = '{artdet}';")
                detalhes = cur.fetchone()
                if detalhes is None:
                    print(f"Não existe um artigo com o ID {artdet}")
                else:
                    print("\nDetalhes do artigo: ")
                    print(
                        f"Título: {detalhes[0]} | Tipo: {detalhes[1]} | Realizador: {detalhes[2]} | Produtor: {detalhes[3]} | Ano: {detalhes[4]} ")

                    try:
                        cur.execute(f"SELECT nome FROM atores, artigo_atores WHERE atores.id = artigo_atores.atores_id and artigo_id = {artdet};")
                        nomes = cur.fetchone()
                        if nomes is None:
                            print("Atores : N/A")
                        else:
                            print(f"Atores: ")
                            while nomes is not None:
                                print(" ", *nomes)
                                nomes = cur.fetchone()
                    except:
                        print("Atores : N/A")

                    print("\n----------------------------Condições de aluguer--------------------------------------\n")

                    cur.execute(f"SELECT periodo_de_aluguer, preco from artigo, historico_precos where artigo.id = {artdet} and historico_precos.atual = True and historico_precos.artigo_id = {artdet};")

                    for linha in cur.fetchall():
                        periodo_de_aluguer, preco = linha
                        print("Período de aluguer(em meses): ", periodo_de_aluguer, "| Preço: ", preco, " €")

                    while True:

                        det1 = input("""Pretende ALUGAR?

                        Responda (S|N): """)

                        if det1 == "S" or det1 == "s":
                            cur.execute(f"SELECT saldo FROM cliente WHERE utilizador_id = {utilizador_atual}")
                            saldo_atual = cur.fetchone()[0]

                            if saldo_atual < preco:
                                print("\nSALDO INSUFICIENTE PARA ALUGAR ESTE ARTIGO")
                                break
                            else:
                                try:
                                    cur.execute(f"INSERT INTO aluguer (id, data, ativo, artigo_id, cliente_utilizador_id, preco_aluguer) VALUES (DEFAULT, CURRENT_TIMESTAMP, True, {artdet}, {utilizador_atual},{preco});")
                                    conn.commit()
                                    print("\nALUGADO!\n")
                                    break
                                except:
                                    conn.rollback()
                                    print("\nALUGUER CANCELADO!\n")
                                    break

                        elif det1 == "N" or det1 == "n":
                            break
                        else:
                            print("Inválido\nTenta outra vez")

            except:
                print("ERRO!")
        except ValueError:
            print("VALOR INVÁLIDO")


alugar()
#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
