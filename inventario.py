#INVENTARIO

import psycopg2
import psycopg2.extras
from getpass import getpass

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

utilizador_atual = 1

#-----------------------------------------------ALUGUERES---------------------------------------------------------------
#UTILIZADOR
def alugueres():

    print("-------------------------------------------ALUGUERES------------------------------------------")

    cur.execute(f"SELECT artigo.titulo, artigo.periodo_de_aluguer, aluguer.data, aluguer.ativo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where cliente.utilizador_id = '{utilizador_atual}'and aluguer.ativo = True ORDER by aluguer.data DESC;")

    print("......................Ativos.......................")
    for linha in cur.fetchall():
        titulo, periodo_de_aluguer,data, ativo = linha
        print("Título: ", titulo, " | Data: ", data, "| Periodo de Aluguer: ", periodo_de_aluguer, " | Ativo?:", ativo)

    cur.execute(f"SELECT artigo.titulo, artigo.periodo_de_aluguer, aluguer.data, aluguer.ativo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where cliente.utilizador_id = '{utilizador_atual}' and aluguer.ativo = False ORDER by aluguer.data DESC;")

    print(".....................Não Ativos......................")
    for linha in cur.fetchall():
        titulo, periodo_de_aluguer, data, ativo = linha
        print("Título: ", titulo, " | Data: ", data, "| Periodo de Aluguer: ", periodo_de_aluguer, " | Ativo?:", ativo)

#ADMIN============================================================================================
def historico(art):

    print("\n--------------------------------Histórico de preços----------------------------------------------\n")

    cur.execute(f"SELECT preco, entrada_em_vigor, atual from historico_precos where artigo_id = '{art}' ORDER BY entrada_em_vigor DESC;")

    for linha in cur.fetchall():
        preco, entrada_em_vigor, atual = linha
        print("Preço: ", preco, "€ | Entrada em vigor: ", entrada_em_vigor, " | Atual?:", atual)

    while True:
        corrigir = input("\nCorrigir Preço? (S|N): \n")

        if corrigir == "S" or corrigir == "s":

            print("--------------------------------------CORRIGIR PREÇO---------------------------------------------------")

            while True:
                try:
                    p = float(input("Preço Novo: \n"))
                    if p < 0:
                        raise ValueError("INSIRA UM VALOR VÁLIDO!")
                    else:
                        break
                except ValueError:
                    print("INSIRA UM VALOR VÁLIDO!")

            tentativas = 3
            while tentativas > 0:
                confirmar = getpass("Introduza a sua chave de administrador para confirmar a alteração do preço:\n")
                cur.execute(f"SELECT chave FROM administrador WHERE utilizador_id = {utilizador_atual}")
                chave = cur.fetchone()[0]
                if confirmar == chave:
                    cur.execute(f"SELECT mudar_estado({art});");
                    cur.execute(f"INSERT INTO historico_precos(id,preco, entrada_em_vigor, atual, artigo_id) VALUES (DEFAULT,{p}, CURRENT_TIMESTAMP, True, {art});")
                    print("Preço Alterado!")
                    conn.commit()
                    break
                else:
                    tentativas -= 1
                    print(f"\nChave errada. Tem {tentativas} tentativas restantes")
                    if tentativas == 0:
                        print("\nAlteração de preço cancelada!")
                        break

            break

        elif corrigir == "N" or corrigir == "n":
            break

#ADMIN============================================================================================================================
def inventario():
    while True:
        print("---------------------------------INVENTÁRIO DE ARTIGOS----------------------------------------")

        cur.execute("SELECT id, titulo, tipo from artigo ORDER BY tipo ASC, titulo ASC;")

        for linha in cur.fetchall():
            id, titulo, tipo = linha
            print("Título: ", titulo,"| Tipo: ", tipo,"| ID: ", id)



        print("\n\t\t\t\t   O que pretende fazer?")

        det = input("\n\t\t\t\t1 - Ver Detalhes do Artigo\n\t\t\t\t\tV|v - Voltar\n\n\t\t\t\t\t    ")

        # ----------------------------------------- VER DETALHES ARTIGO-------------------------------------------------
        if det == "1":
            while True:
                print("\n---------------------------VER DETALHES ARTIGO---------------------------\n")
                voltar = input("ENTER - Ver detalhes\nV/v - Voltar ao Inventário\n\n")
                if voltar == "":
                    while True:
                        try:
                            artdet = int(input("De que artigo quer ver detalhes?(ID): "));
                            break
                        except ValueError:
                            print("Valor de ID inválido")


                    try:
                        cur.execute(f"SELECT titulo, tipo, realizador, produtor, ano from artigo where id = '{artdet}';")
                        detalhes = cur.fetchone()
                        if detalhes is None:
                           print(f"Não existe um artigo com o ID {artdet}")
                           break
                        else:
                            while detalhes is not None:
                                print("\nDetalhes do artigo: ")
                                print("[ Título | Tipo | Realizador | Produtor | Ano | Ator ]")
                                print(detalhes)
                                detalhes = cur.fetchone()

                            print("\n Mais detalhes: \n")
                            while True:

                                det1 = input("""
                                            1- Histórico de preços
                                            2- Condições de Aluguer
                                            V|v - Voltar
                                VER: """)

                                #Histórico de preços
                                if det1 == "1":
                                    historico(artdet)
                                    break

                                #Condições de aluguer
                                elif det1 == "2":

                                    print("\n----------------------------Condições de aluguer--------------------------------------\n")

                                    cur.execute(f"SELECT periodo_de_aluguer, preco from artigo, historico_precos where artigo.id = {artdet} and historico_precos.atual = True and historico_precos.artigo_id = {artdet};")

                                    for linha in cur.fetchall():
                                        periodo_de_aluguer, preco = linha
                                        print("Período de aluguer(em meses): ", periodo_de_aluguer, "| Preço: ", preco, " €")
                                    break

                                #Voltar
                                elif det1 == "V" or det1 == "v":
                                    break
                                else:
                                    print("Inválido")
                                    print("Tente outra vez")
                    except ValueError:
                        print("ID inválido")

                elif voltar == "v" or voltar == "V":
                    print("A VOLTAR AO INVENTÁRIO")
                    break
                else:
                    print("")

        # Volta ao Inventário
        elif det == "V" or det == "v":
            break

        # Input não válido
        else:
            print("\n\t\t\t\t\tInválido")
            print("\t\t\t\t     Tenta outra vez\n")

#------------------------------------------Lista de artigos para alugar-------------------------------------------------
#UTILIZADOR
def lista():

    print("\n---------------------------------Artigos para alugar-----------------------------\n")

    cur.execute("SELECT titulo, tipo from artigo ORDER BY tipo ASC, titulo ASC;")

    for linha in cur.fetchall():
        titulo, tipo = linha
        print("Título: ", titulo,"| Tipo: ", tipo)


    inv = True
    while inv:
        print("\nO Que pretende fazer?\n")

        det = input("""
                                           1 - Ver Detalhes do Artigo
                                           V|v - Voltar

                       Resposta: """)

    # ----------------------------------------- VER DETALHES ARTIGO-------------------------------------------------
        if det == "1":

            print("\nVER DETALHES ARTIGO\n")

            artdet = input("Qual artigo quer ver detalhes?: ")

            cur.execute(f"SELECT a.titulo, a.tipo, a.realizador, a.produtor, a.ano, at.nome from artigo as a join artigo_atores as aa on a.id = aa.artigo_id join atores as at on aa.atores_id = at.id where a.titulo = '{artdet}';")

            detalhes = cur.fetchone()

            if detalhes is None:
                print("Resultado não encontrado!")

            while detalhes is not None:
                print("\nDetalhes do artigo: ")
                print("[ Título | Tipo | Realizador | Produtor | Ano | Ator ]")
                print(detalhes)
                detalhes = cur.fetchone()

            print("\n----------------------------Condições de aluguer--------------------------------------\n")

            cur.execute(f"SELECT a.periodo_de_aluguer, h.preco from artigo as a join historico_precos as h on a.id = h.artigo_id where a.titulo = '{artdet}' and h.atual = True;")

            for linha in cur.fetchall():
                 periodo_de_aluguer, preco = linha
                 print("Período de aluguer: ", periodo_de_aluguer, "| Preço: ", preco, " €")

            print("\n OPÇÕES: \n")

            while True:

                det1 = input("""Prentende ALUGAR?

                Responda (S|N): """)

                if det1 == "S" or det1 == "s":

                    cur.execute(f"INSERT INTO aluguer (id, data, ativo, artigo_id, cliente_utilizador_id) VALUES (DEFAULT, CURRENT_TIMESTAMP, True, (SELECT id from artigo where titulo = '{artdet}'), '{utilizador_atual}');")

                    print("\nALUGADO!\n")

                    alugueres()

                elif det1 == "N" or det1 == "n":
                    break
                else:
                    print("Inválido")
                    print("Tenta outra vez")

        # Volta ao menu anterior
        elif det == "V" or det == "v":
            inv = False

        else:
            print("Inválido")
            print("Tenta outra vez")

inventario()

# Fecha a ligação à base de dados
cur.close()
conn.close()
