import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass


#==========================================================================================================================
# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

#==========================================================================================================================
#Variáveis globais
utilizador_atual = 0    #Utilizador com login efetuado


#==========================================================================================================================
#Início/Ecrã inicial
def inicio():
    while True:
        try:
            print("""----------------------------Início--------------------------------
                         ____      __
                        |    \    |  |
                        |     \   |  |
                        |  |\  \  |  |
                        |  | \  \ |  |
                        |  |  \  \|  |
                        |  |   \     |
                        |__|    \____|
                """)
            print("""\n                    Bem vind@ ao NETFLOX\n
                          1 - Login\n
                        2 - Registar\n
                          3 - Sair\n\n
                          ESCOLHA""")
            inicio_escolha = int(input("\n\t\t\t     "))
            if (inicio_escolha == 1):       #Login
                login()
            elif(inicio_escolha == 2):      #Registo
                registo()
            elif(inicio_escolha == 3):      #Sair
                return
            else:
                print(" ")
        except ValueError:
            print(" ")


#==========================================================================================================================
#Login
def login():
    print("\n----------------------------Login--------------------------------")
    while True:
        email = input("\nEmail   ")
        cur.execute(f"SELECT COUNT(email) FROM utilizador WHERE email LIKE '%{email}'")
        email_verif = cur.fetchone()
        if (email_verif[0]==1):
            while True:
                password = getpass("\nPassword   ")
                cur.execute(f"SELECT password FROM utilizador WHERE email LIKE '%{email}'")
                password_verif = cur.fetchone()
                if(sha256_crypt.verify(password ,password_verif[0])):
                    print("\nInicio de sessão bem sucedida\n")
                    break
                else:
                    print("\nPassword errada")
            break
        else:
            print("\nEndereço de email inválido")
    return


#==========================================================================================================================
#Registo
def registo():
    while True:
        #Registo do Email
        print("\n----------------------------Registo--------------------------------")
        while True:
            email = input("\nInsira o seu endereço de email\n    ")
            cur.execute(f"SELECT COUNT(email) from utilizador where email like '%{email}'")
            email_verif = cur.fetchone()
            if ("@" in email and email_verif[0]==0 and ' ' not in email and email[0]!= '@' and email[len(email)-1]!='@' and '.' in email):
                print(f"Email inserido\n    {email}")
                break
            else:
                print("\nEndereço de email inválido")

        #Registo da Password
        while(True):
            password = getpass("\n\nInsira a sua password\n    ")
            password_encriptada = sha256_crypt.hash(password)
            password_verif = getpass("Confirme a sua password\n    ")
            if(sha256_crypt.verify(password_verif ,password_encriptada)):
                print("Password aceite\n")
                break
            else:
                print("Passwords não correspondem")

        #Registo do nome
        nickname = input("\n\nInsira o seu nome\n    ")
        print(f"Nome inserido\n    {nickname}")

        #Guardar dados na base de dados
        try:
            cur.execute(f"INSERT INTO utilizador(id, email, password, nome) VALUES (DEFAULT, '{email}', '{password_encriptada}', '{nickname}') RETURNING id;")
            id = cur.fetchone()[0]
            cur.execute(f"INSERT INTO cliente(utilizador_id, saldo) VALUES ({id}, 15);")
            #Confirmar mudanças
            conn.commit()
            #De volta ao início
            print("BEM VIND@ À FAMÍLIA NETFLOX")
            return
        except:
            print("Dados não válidos")


#==========================================================================================================================
#Iniciar programa
inicio()







#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
