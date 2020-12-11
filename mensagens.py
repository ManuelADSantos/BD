#MENSAGENS

import psycopg2
from getpass import getpass
# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

utilizador_atual = 2

#-----------------------------------------------MENU MENSAGENS CLIENTE-------------------------------------------------
def admin_mensagens():
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

#=========================================================================================================================================
def cliente_mensagens():
    while True:
        print("\n================================================================")
        print("\n|                           MENSAGENS                          |")
        print("\n================================================================")
        cur.execute(f"SELECT mensagem_id FROM cliente_mensagem WHERE cliente_utilizador_id = {utilizador_atual} EXCEPT SELECT mensagem_id FROM leitura WHERE lida IS NOT NULL AND cliente_utilizador_id = {utilizador_atual};")
        print(f"\n\t            Tem {len(cur.fetchall())} mensagens não lidas ")



        msg = input("""

                  || 1 - MENSAGENS NÃO LIDAS ||
                  || 2 - MENSAGENS JÁ LIDAS  ||
                  ||       V|v - Voltar      ||

                                """)
        if msg == "1":
            while True:
                print("\n\n\t\t || A ABRIR MENSAGENS NÃO LIDAS ||")
                print("\n================================================================")
                print("\n|                     MENSAGENS NÃO LIDAS                      |")
                print("\n================================================================")

                cur.execute(f"SELECT DISTINCT leitura.mensagem_id, corpo FROM mensagem, leitura WHERE leitura.lida IS NULL AND leitura.cliente_utilizador_id = {utilizador_atual} AND mensagem.id = leitura.mensagem_id ORDER BY mensagem_id ASC;")
                corpo = cur.fetchone()
                if corpo is not None:
                    #Corpo da mensagem
                    id_mensagem = corpo[0]
                    print("\n\t\t    || CORPO DA MENSAGEM ||\n\n", corpo[1])

                    #Administrador que enviou a mensagem
                    cur.execute(f"SELECT nome FROM utilizador WHERE id = (SELECT administrador_utilizador_id FROM mensagem_administrador WHERE mensagem_id = {id_mensagem});")
                    print("\n Atenciosamente, \n\t", cur.fetchone()[0])

                    while True:
                        opcao = input("\n\t\t ||   1 - PRÓXIMA MENSAGEM   ||\n\t\t || v/V - VOLTAR A MENSAGENS ||\n\t\t\t       ")
                        if opcao == "1" or opcao == "v" or opcao == "V":
                            break

                    if opcao == "1":
                        cur.execute(f"UPDATE leitura SET lida = CURRENT_TIMESTAMP WHERE cliente_utilizador_id = {utilizador_atual} AND mensagem_id = {id_mensagem};")
                        conn.commit()
                    elif opcao == "v" or opcao == "V":
                        cur.execute(f"UPDATE leitura SET lida = CURRENT_TIMESTAMP WHERE cliente_utilizador_id = {utilizador_atual} AND mensagem_id = {id_mensagem};")
                        conn.commit()
                        break
                else:
                    print("\n\t\t   Não tem mensagens não lidas\n\n\t\t   || A VOLTAR A MENSAGENS ||")
                    break

        elif msg == "2":
            while True:
                print("\n\n\t\t || A ABRIR MENSAGENS JÁ LIDAS ||")
                print("\n================================================================")
                print("\n|                      MENSAGENS JÀ LIDAS                       |")
                print("\n================================================================")

                cur.execute(f"SELECT DISTINCT leitura.mensagem_id, corpo, administrador_utilizador_id FROM mensagem, leitura, mensagem_administrador WHERE leitura.lida IS NOT NULL AND leitura.cliente_utilizador_id = {utilizador_atual} AND mensagem.id = leitura.mensagem_id ORDER BY mensagem_id ASC;")
                dados = cur.fetchone()
                if dados is not None:
                    while dados is not None:
                        #ID da mensagem
                        id_mensagem = dados[0]
                        #Corpo da mensagem
                        if len(dados[1]) > 15:
                            corpo = ""
                            for i in range(12):
                                corpo += dados[1][i]
                            corpo += "  [...]"
                        else:
                            corpo = dados[1]

                        #Administrador que enviou a mensagem
                        admin_id = dados[2]
                        cur.execute(f"SELECT nome FROM utilizador WHERE id = {admin_id}")
                        admin = cur.fetchone()[0]

                        print(f"ID: {id_mensagem} |Remetente: {admin} |Corpo: {corpo}")
                        dados = cur.fetchone()

                    break

                elif dados is None:
                    print("\n\t\t   Não tem mensagens já lidas\n\n\t\t   || A VOLTAR A MENSAGENS ||")
                    break


        elif msg == "v" or msg =="V":
            return

        else:
            print("")

cliente_mensagens()

# Fecha a ligação à base de dados
cur.close()
conn.close()
