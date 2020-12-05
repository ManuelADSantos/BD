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
#Início
def inicio():
    while True:
        try:
            print("----------------------------Início--------------------------------")
            print("\nBem vind@ ao NETFLOX\n    1 - Login\n    2 - Registar")
            inicio_escolha = int(input("\nSelecione a opção que deseja: "))
            if (inicio_escolha == 1):       #Login
                login()
            elif(inicio_escolha == 2):      #Registo
                registo()
            else:
                print("!!! Opção inválida !!!")
        except ValueError:
            print("!!! Opção inválida !!!")


#==========================================================================================================================
#Login
def login():
    print("\n----------------------------Login--------------------------------")
    while True:
        email = input("\nEmail:   ")
        cur.execute(f"SELECT COUNT(email) from utilizador where email like '%{email}'")
        email_verif = cur.fetchone()
        if (email_verif[0]==0):
            password = getpass("\n\nPassword:   ")
            password_encriptada = sha256_crypt.hash(password)
            if(sha256_crypt.verify(password_verif ,password_encriptada)):
                print("Password aceite\n")
                break
            else:
                print("Password errada")
        else:
            print("\nEndereço de email inválido")


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
            cur.execute(f"INSERT INTO utilizador(id, email, password, nome) VALUES (DEFAULT, '{email}', '{password_encriptada}', '{nickname}');")
            #Confirmar mudanças
            conn.commit()
            #De volta ao início
            print("BEM VINDO AO NETFLOX")
            return
        except:
            print("Dados não válidos")


#==========================================================================================================================
#Procedimento
inicio()







#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
