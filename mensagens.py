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

            texto = input("ESCREVA A MENSAGEM: \n")

            print("ENVIAR MENSAGEM GERAL: ")

            cur.execute(f"INSERT INTO mensagem(id, corpo) VALUES (DEFAULT, '{texto}');")

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
