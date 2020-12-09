#MENSAGENS

import psycopg2

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

#-----------------------------------------------MENU MENSAGENS CLIENTE-------------------------------------------------
def cliente_mensagens():

    mensagensc = True

    #PEDE AO CLIENTE QUE TIPO DE PESQUISA QUER EFETUAR
    while mensagensc:
        print("----------------------MENU MENSAGENS---------------------")
        print("\n Que mensagens pretende ver? \n")

        msg = input("""
                            1 - MENSAGENS LIDAS
                            2 - MENSAGENS NÃO LIDAS
                            V|v - Voltar

        VER: """)

        #-------------------------------------Mensagens n Lidas----------------------------------
        if msg == "1":

            print("Mensagens não lidas: ")
            cur.execute(";")

        # -----------------------------------Mensagens lidas--------------------------------------
        elif msg == "2":

            print("Mensagens lidas: ")

            cur.execute(";")


        #Volta ao menu anterior
        elif msg == "V" or msg == "v":
            mensagensc = False

        else:
            print("Inválido")
            print("Tenta outra vez")


# -----------------------------------------------MENU MENSAGENS ADMIN-------------------------------------------------
def admin_mensagens():
    mensagensa = True

    # PEDE AO ADMIN QUE TIPO DE PESQUISA QUER EFETUAR
    while mensagensa:
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

                                conn.commit()
                                print("MENSAGEM GERAL ENVIADA ")
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
                    break
                else:
                    print("")
        # -----------------------------------Mensagem individual-----------------------------------
        elif msg == "2":

            print("ENVIAR MENSAGEM INDIVIDUAL: ")

            mcliente = input("A que cliente pretende enviar uma mensagem?: ")

            cur.execute(f"SELECT nome from utilizador where nome like '%{mcliente}';")

            print("Cliente:")

            c = cur.fetchone()

            if c is None:
                print("Cliente não encontrado!")

            while c is not None:
                print("->", *c)
                c = cur.fetchone()

            texto = input("ESCREVA A MENSAGEM: \n")

            cur.execute(f"INSERT INTO mensagem(id, corpo) VALUES (DEFAULT, '{texto}');")

            cur.execute(f"INSERT INTO mensagem_administrador VALUES ();")

        # Volta ao menu anterior
        elif msg == "V" or msg == "v":
            mensagensa = False

        else:
            print("Inválido")
            print("Tenta outra vez")

# Fecha a ligação à base de dados
cur.close()
conn.close()
