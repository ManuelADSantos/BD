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
utilizador_atual = 1    #Utilizador com login efetuado
#==========================================================================================================================

# PEDE AO ADMIN QUE TIPO DE PESQUISA QUER EFETUAR
while True:
    print("----------------------MENU MENSAGENS---------------------")
    print("\n Que mensagem pretende enviar? \n")

    msg = input("""
                        1 - MENSAGEM GERAL
                        2 - MENSAGEM INDIVIDUAL
                        V|v - Voltar

    ENVIAR: """)

    # -----------------------------------Mensagem geral--------------------------------------
    if msg == "1":
        while True:
            print("----------------------MENU MENSAGEM GERAL---------------------")
            voltar = input("\nENTER - Enviar Mensagem\nV/v - Voltar ao MENU\n\n")
            if voltar == "":
                while True:
                    texto = input("ESCREVA A MENSAGEM: \n")
                    verif_geral = input("Confirma que é esta a mensagem a enviar?(S/N)")
                    if verif_geral == "S" or verif_geral == "s":
                        try:
                            print("Mensagem Confirmada")
                            #Inserir mensagem na tabela mensagens
                            cur.execute(f"INSERT INTO mensagem(id, corpo) VALUES (DEFAULT, '{texto}') RETURNING id;")
                            id_mensagem = cur.fetchone()[0]
                            #Registar mensagem na tabela mensagem_administrador
                            cur.execute(f"INSERT INTO mensagem_administrador(mensagem_id, administrador_utilizador_id) VALUES ({id_mensagem}, {utilizador_atual});")
                            #Registar mensagem na tabela cliente_mensagem
                            cur.execute("SELECT * FROM cliente")
                            for linha in cur.fetchall():
                                cur.execute(f"INSERT INTO cliente_mensagem(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {linha['utilizador_id']});")

                            tentativas = 3
                            sair = False
                            while tentativas > 0:
                                confirmar = getpass("Introduza a sua chave de administrador para confirmar o envio da mensagem:\n")
                                cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                                chave = cur.fetchone()[0]
                                if confirmar == chave:
                                    print("MENSAGEM GERAL ENVIADA ")
                                    conn.commit()
                                    sair = True
                                    break
                                else:
                                    tentativas -= 1
                                    print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                                    if tentativas == 0:
                                        print("\nEnvio da mensagem cancelado!")
                                        conn.rollback()
                                        sair = True
                                        break
                            if (sair == True):
                                break

                        except:
                            conn.rollback()
                            print("ERRO: MENSAGEM GERAL ANULADA ")
                    elif verif_geral == "N" or verif_geral == "n":
                        print("Mensagem Eliminada")
                        break
                    else:
                        print("Opção inválida")
                        break

            elif voltar == "v" or voltar == "V":
                print("A VOLTAR AO MENU")
                mensagensa = False
                break
            else:
                print("")

    # -----------------------------------Mensagem individual-----------------------------------
    elif msg == "2":
        while True:
            print("----------------------MENU MENSAGEM INDIDUAL---------------------")
            voltar = input("\nENTER - Enviar Mensagem\nV/v - Voltar ao MENU\n\n")
            if voltar == "":
                while True:
                    print("Clientes aos quais é possível enviar mensagem\n")
                    cur.execute("SELECT utilizador_id, nome FROM cliente, utilizador WHERE utilizador_id = id")
                    for linha in cur.fetchall():
                        x1 = linha['utilizador_id']
                        x2 = linha['nome']
                        print("-> ID:", x1,"/Nome: ", x2)

                    try:
                        cliente_msg = int(input("Qual o ID do cliente ao qual pretende enviar mensagem?\n"))
                        cur.execute(f"SELECT utilizador_id FROM cliente WHERE utilizador_id = {cliente_msg}")
                        existe = cur.fetchone()
                        if existe is not None:
                            break
                        elif existe is None:
                            print("Não existe um cliente com o ID indicado")
                    except ValueError:
                        print("ID não válido\n")


                while True:
                    texto = input("ESCREVA A MENSAGEM: \n")
                    verif_geral = input("Confirma que é esta a mensagem a enviar?(S/N)")
                    if verif_geral == "S" or verif_geral == "s":
                        try:
                            print("Mensagem Confirmada")
                            #Inserir mensagem na tabela mensagens
                            cur.execute(f"INSERT INTO mensagem(id, corpo) VALUES (DEFAULT, '{texto}') RETURNING id;")
                            id_mensagem = cur.fetchone()[0]
                            #Registar mensagem na tabela mensagem_administrador
                            cur.execute(f"INSERT INTO mensagem_administrador(mensagem_id, administrador_utilizador_id) VALUES ({id_mensagem}, {utilizador_atual});")
                            #Registar mensagem na tabela cliente_mensagem
                            cur.execute(f"INSERT INTO cliente_mensagem(mensagem_id, cliente_utilizador_id) VALUES ({id_mensagem}, {cliente_msg});")

                            tentativas = 3
                            sair = False
                            while tentativas > 0:
                                confirmar = getpass("Introduza a sua chave de administrador para confirmar o envio da mensagem:\n")
                                cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                                chave = cur.fetchone()[0]
                                if confirmar == chave:
                                    print("MENSAGEM INDIDUAL ENVIADA ")
                                    conn.commit()
                                    sair = True
                                    break
                                else:
                                    tentativas -= 1
                                    print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                                    if tentativas == 0:
                                        print("\nEnvio da mensagem cancelado!")
                                        conn.rollback()
                                        sair = True
                                        break
                            if (sair == True):
                                break

                        except:
                            conn.rollback()
                            print("ERRO: MENSAGEM INDIDUAL ANULADA ")
                    elif verif_geral == "N" or verif_geral == "n":
                        print("Mensagem Eliminada")
                        break
                    else:
                        print("Opção inválida")
                        break

            elif voltar == "v" or voltar == "V":
                print("A VOLTAR AO MENU")
                mensagensa = False
                break
            else:
                print("")
    if msg == "v" or msg == "V":
        break

#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
