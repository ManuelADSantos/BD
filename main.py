import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass


# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

#Início=========================================================================
while True:
    try:
        print("----------------------------Início--------------------------------")
        print("\nBem vind@ ao NETFLOX\n    1 - Login\n    2 - Registar")
        inicio_escolha = int(input("\nSelecione a opção que deseja: "))
        if (inicio_escolha == 1 or inicio_escolha == 2):
            break
        else:
            print("!!! Opção inválida !!!")
    except ValueError:
        print("!!! Opção inválida !!!")

#Registo========================================================================
if(inicio_escolha == 2):
    #Registo do Email
    while True:
        print("\n----------------------------Registo--------------------------------")
        email = input("Insira o seu endereço de email: \n    ")
        cur.execute(f"SELECT COUNT(email) from utilizador where email like '%{email}'")
        email_verif = cur.fetchone()
        if ("@" in email and email_verif[0]==0 and ' ' not in email):
            print(f"Email inserido:\n    {email}")
            break
        else:
            print("\nEndereço de email inválido")

    #Registo da Password
    while(True):
        password = getpass("\nInsira a sua password:\n    ")
        password_encriptada = sha256_crypt.hash(password)
        password_verif = getpass("Confirme a sua password:\n    ")
        if(sha256_crypt.verify(password_verif ,password_encriptada)):
            print("\nPassword aceite")
            break
        else:
            print("\nPasswords não correspondem")

    #Registo do nome
    nickname = input("Insira o seu nome: \n    ")
    print(f"Nome inserido:\n    {nickname}")

# Fecha a ligação à base de dados
cur.close()
conn.close()
