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

def admin_removerartigo():
    while True:
        print("\n-------------------------------------Remover Artigo-----------------------------------------------\n Artigos disponiveis para remoção\n NOTA:(ID,Título, Tipo de Artigo, Realizador, Produtor, Ano, Período de Aluguer)\n\n")
        cur.execute("SELECT (artigo.id, titulo, tipo, realizador, produtor, ano, periodo_de_aluguer) FROM artigo EXCEPT SELECT (artigo.id, titulo, tipo, realizador, produtor, ano, periodo_de_aluguer) FROM artigo INNER JOIN aluguer ON artigo.id = aluguer.artigo_id")

        #Apresentação de artigos possíveis de remoção
        disponiveis = cur.fetchone()
        while disponiveis is not None:
            disponiveis = cur.fetchone()
            if disponiveis is None:
                break
            else:
                print(f"-> {disponiveis[0]}")

        voltar = input("\nENTER - Avançar para a remoção\nV/v - Voltar ao MENU\n\n")

        if voltar == "":
            while True:
                    while True:
                        try:
                            escolha = int(input("Escolha o artigo que deseja remover(ID): "))
                            cur.execute(f"SELECT titulo FROM artigo WHERE id = {escolha}")
                            existe = cur.fetchone()
                            if existe is not None:
                                break
                            elif existe is None:
                                print("Não existe um artigo com o ID indicado")
                        except ValueError:
                            print("ID não válido")


                    validar = input("\nPretende avançar com a remoção? (S/N)\n")
                    if validar == "S" or validar == "s":
                        cur.execute(f"DELETE FROM historico_precos WHERE artigo_id = {escolha}")
                        cur.execute(f"DELETE FROM artigo_atores WHERE artigo_id = {escolha}")
                        cur.execute(f"DELETE FROM artigo WHERE id = {escolha}")

                        tentativas = 3
                        while tentativas > 0:
                            confirmar = getpass("Introduza a sua chave de administrador para confirmar a remoção do artigo:\n")
                            cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                            chave = cur.fetchone()[0]
                            if confirmar == chave:
                                print("\nArtigo removido com sucesso")
                                conn.commit()
                                return
                            else:
                                tentativas -= 1
                                print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                                if tentativas == 0:
                                    print("\nRemoção de artigo cancelada!")
                                    conn.rollback()
                                    return
                        break
                    if validar == "N" or validar == "n":
                        print("\nRemoção cancelada")
                        break
                    else:
                        print("\nOpção inválida")


        elif voltar == "V" or voltar == "v":
            break

    return


admin_removerartigo()
#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
