import psycopg2
import psycopg2.extras
from passlib.hash import sha256_crypt
from getpass import getpass
import os


#==========================================================================================================================
# Estabelecer ligação à base de dados
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Criar cursor
cur = conn.cursor()

#==========================================================================================================================
def admin_adicionarartigo():
    while True:
        print("\n-------------------------------------Adicionar Artigo-----------------------------------------------\n")

        #Título
        while True:
            novo_titulo = input("Titulo do novo artigo: ")
            validar = input("\nConfirma o titulo do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nTitulo descartado")
            else:
                print("\nOpção inválida")

        #Tipo
        while True:
            novo_tipo = input("Tipo de artigo\n1 - Filme\n2 - Documentário\n3 - Série\n")
            if novo_tipo == "1" or novo_tipo == "2" or novo_tipo == "3":
                validar = input("Confirma o tipo do artigo a introduzir? (S/N)\n")
                if validar == "S" or validar == "s":
                    if novo_tipo == "1":
                        novo_tipo = "filme"
                    elif novo_tipo == "2":
                        novo_tipo = "documentario"
                    elif novo_tipo == "3":
                        novo_tipo = "serie"
                    break
                if validar == "N" or validar == "n":
                    print("\nTipo descartado")
                else:
                    print("\nOpção inválida")
            else:
                print("\nOpção inválida")

        #Realizador
        while True:
            novo_realizador = input("Realizador do novo artigo: ")
            validar = input("\nConfirma o realizador do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nRealizador descartado")
            else:
                print("\nOpção inválida")

        #Produtor
        while True:
            novo_produtor = input("Produtor do novo artigo: ")
            validar = input("\nConfirma o produtor do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nProdutor descartado")
            else:
                print("\nOpção inválida")

        #Ano
        while True:
            novo_ano = int(input("Ano do novo artigo: "))
            validar = input("\nConfirma o ano do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nAno descartado")
            else:
                print("\nOpção inválida")

        #Periodo de aluguer
        while True:
            novo_periodoaluguer = int(input("Especifique o periodo de aluguer do novo artigo (em meses): "))
            validar = input("\nConfirma o periodo de aluguer do artigo a introduzir? (S/N)\n")
            if validar == "S" or validar == "s":
                break
            if validar == "N" or validar == "n":
                print("\nPeriodo de aluguer descartado")
            else:
                print("\nOpção inválida")

        #Efetuar Registo

        cur.execute(f"INSERT INTO artigo(id, titulo, tipo, realizador, produtor, ano, periodo_de_aluguer) VALUES (DEFAULT, '{novo_titulo}', '{novo_tipo}', '{novo_realizador}', '{novo_produtor}', {novo_ano}, {novo_periodoaluguer}) RETURNING id;")
        id_artigo = cur.fetchone()[0]
        perguntar = input("Pretende associar atores a este artigo? (S/N)\n")
        if perguntar == "S" or perguntar == "s":
            while True:
                ator = input("\nInsira o nome do ator ou atriz a associar a este artigo(Primeiro e Último nome): ")
                cur.execute(f"SELECT id FROM atores WHERE nome LIKE '%{ator}'")
                id_ator = cur.fetchone()
                if id_ator is not None:                         #Ator pertence à base de dados
                    cur.execute(f"INSERT INTO artigo_atores(artigo_id, atores_id) VALUES ({id_artigo},{id_ator[0]});")
                    print(f"\n{ator} participa agora neste artigo")
                    mais = input("Pretende adicionar mais atores ao artigo?(S/N):\n")
                    if mais == "S" or mais == "s":
                        print("")
                    else:
                        break
                elif id_ator is None:                           #Ator não pertence à base de dados
                    print("Ator/atriz não registado/a na base de dados")
                    while True:                 #Adicionar novo ator
                        nome_novo_ator = input("Nome do novo ator a inserir na base de dados(Primeiro e Último nome): ")
                        check = input("Confirma os dados do novo ator a adicionar à base de dados?(S/N):\n")
                        if check == "S" or check == "s":
                            cur.execute(f"INSERT INTO atores(id, nome) VALUES (DEFAULT,'{nome_novo_ator}') RETURNING id;")
                            id_novo_ator = cur.fetchone()[0]
                            cur.execute(f"INSERT INTO artigo_atores(artigo_id, atores_id) VALUES ({id_artigo},{id_novo_ator});")
                            break
                        else:
                            print("Nome não registado")

                    mais = input("Pretende adicionar mais atores ao artigo?(S/N):\n")
                    if mais == "S" or mais == "s":
                        print("")
                    else:
                        break

            conn.commit()
            return

        else:
            conn.commit()
            return



admin_adicionarartigo()
#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
