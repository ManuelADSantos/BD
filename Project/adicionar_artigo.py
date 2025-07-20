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


utilizador_atual = 1;
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
        print(novo_titulo)

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
        print(novo_tipo)

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
        print(novo_realizador)


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
        print(novo_produtor)

        #Ano
        while True:
            ano_atual = datetime.datetime.now()
            ano_atual = int(ano_atual.strftime("%Y"))
            try:
                novo_ano = int(input("Ano do novo artigo: "))

                if novo_ano < 1895 or novo_ano > ano_atual:
                    print("Valor não válido")
                else:
                    validar = input("\nConfirma o ano do artigo a introduzir? (S/N)\n")
                    if validar == "S" or validar == "s":
                        break
                    if validar == "N" or validar == "n":
                        print("\nAno descartado")
                    else:
                        print("\nOpção inválida")
            except ValueError:
                print("Valor não válido")
        print(novo_ano)


        #Periodo de aluguer
        while True:
            try:
                novo_periodoaluguer = int(input("Especifique o periodo de aluguer do novo artigo (em meses): "))
                if novo_periodoaluguer > 0:
                    validar = input("\nConfirma o periodo de aluguer do artigo a introduzir? (S/N)\n")
                    if validar == "S" or validar == "s":
                        break
                    if validar == "N" or validar == "n":
                        print("\nPeriodo de aluguer descartado")
                    else:
                        print("\nOpção inválida")
                else:
                    print("Valor inválido")
            except:
                print("\nValor inválido")
        print(novo_periodoaluguer)

        #Adicionar preço
        while True:
            try:
                novo_preco = float(input("Especifique o preço do novo artigo: "))
                if novo_preco >= 0:
                    validar = input("\nConfirma o preço do artigo a introduzir? (S/N)\n")
                    if validar == "S" or validar == "s":
                        break
                    if validar == "N" or validar == "n":
                        print("\nPreço descartado")
                    else:
                        print("\nOpção inválida")
                else:
                    print("Valor inválido")
            except:
                print("\nValor inválido")
        print(novo_preco)

        #Efetuar Registo
        try:
            cur.execute(f"INSERT INTO artigo(id, titulo, tipo, realizador, produtor, ano, periodo_de_aluguer) VALUES (DEFAULT, '{novo_titulo}', '{novo_tipo}', '{novo_realizador}', '{novo_produtor}', {novo_ano}, {novo_periodoaluguer}) RETURNING id;")
            print("CHECK")
            id_artigo = cur.fetchone()[0]
            cur.execute(f"INSERT INTO historico_precos(id,preco,entrada_em_vigor,atual,artigo_id) VALUES (DEFAULT, {novo_preco}, CURRENT_TIMESTAMP, True , {id_artigo});")
            perguntar = input("Pretende associar atores a este artigo? (S/N)\n")
            if perguntar == "S" or perguntar == "s":
                while True:
                    ator = input("\nInsira o nome do ator ou atriz a associar a este artigo(Primeiro e Último nome): ")
                    cur.execute(f"SELECT id FROM atores WHERE nome LIKE '%{ator}' AND nome LIKE '{ator}%'")
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
                        while True:
                            saber = input("Ator/atriz não registado/a na base de dados. Pretende adicionar o ator à nossa base de dados?(S/N)")
                            if saber == "S" or saber == "s":
                                while True:                 #Adicionar novo ator
                                    novo = True
                                    nome_novo_ator = input("Nome do novo ator a inserir na base de dados(Primeiro e Último nome): ")
                                    cur.execute(f"SELECT id FROM atores WHERE nome LIKE '%{nome_novo_ator}' AND nome LIKE '{nome_novo_ator}%'")
                                    existe = cur.fetchall()
                                    if len(existe) == 0 :
                                        check = input("Confirma os dados do novo ator a adicionar à base de dados?(S/N):\n")
                                    else:
                                        print("\nAtor/atriz já registado/a na base de dados")
                                        novo = False

                                    if (check == "S" or check == "s") and novo == True:
                                        cur.execute(f"INSERT INTO atores(id, nome) VALUES (DEFAULT,'{nome_novo_ator}') RETURNING id;")
                                        id_novo_ator = cur.fetchone()[0]
                                        cur.execute(f"INSERT INTO artigo_atores(artigo_id, atores_id) VALUES ({id_artigo},{id_novo_ator});")
                                        print(f"\n{nome_novo_ator} participa agora neste artigo")
                                        break
                                    else:
                                        print("Nome não registado")
                                break

                            elif saber == "N" or saber == "n":
                                break

                            else:
                                print("")

                        while True:
                            mais = input("Pretende adicionar mais atores ao artigo?(S/N):\n")
                            if mais == "N" or mais == "n":
                                out = True
                                break
                            elif mais == "S" or mais == "s":
                                print("")
                                out = False
                                break
                            else:
                                print("Valor inválido")


                        if out == True:
                            break


                tentativas = 3
                while tentativas > 0:
                    confirmar = getpass("Introduza a sua chave de administrador para confirmar a introdução do artigo:\n")
                    cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                    chave = cur.fetchone()[0]
                    if confirmar == chave:
                        print("\nArtigo adicionado com sucesso")
                        conn.commit()
                        return
                    else:
                        tentativas -= 1
                        print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                        if tentativas == 0:
                            print("\nAdição de artigo cancelada!")
                            conn.rollback()
                            return


            elif perguntar == "N" or perguntar == "n":
                tentativas = 3
                while tentativas > 0:
                    confirmar = getpass("Introduza a sua chave de administrador para confirmar a introdução do artigo:\n")
                    cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                    chave = cur.fetchone()[0]
                    if confirmar == chave:
                        print("\nArtigo adicionado com sucesso")
                        conn.commit()
                        return
                    else:
                        tentativas -= 1
                        print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                        if tentativas == 0:
                            print("\nAdição de artigo cancelada!")
                            conn.rollback()
                            return

            else:
                print("Valor inválido")
        except:
            print("\nDados Inválidos")
            conn.rollback()




admin_adicionarartigo()
#==========================================================================================================================
# Fecha a ligação à base de dados
cur.close()
conn.close()
