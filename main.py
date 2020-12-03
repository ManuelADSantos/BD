import psycopg2
import os


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
        if ("@" in email):
            print(f"\nEmail inserido:\n    {email}")
            break
        else:
            print("\nEndereço de email não válido")

    #Registo da Password
    password = input("\nInsira a sua password:\n    ")

    



# Fecha a ligação à base de dados
cur.close()
conn.close()
