import psycopg2
import psycopg2.extras

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor()

utilizador_atual = 1

def alugueres():
    print("-------------------------------------------ALUGUERES------------------------------------------")

    cur.execute(f"SELECT artigo.titulo, artigo.periodo_de_aluguer, aluguer.data, aluguer.ativo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where cliente.utilizador_id = '{utilizador_atual}'and aluguer.ativo = True ORDER by aluguer.data DESC;")

    print("......................Ativos.......................")
    for linha in cur.fetchall():
        titulo, periodo_de_aluguer, data, ativo = linha
        print("Título: ", titulo, " | Data: ", data, "| Periodo de Aluguer: ", periodo_de_aluguer, " | Ativo?:", ativo)

    cur.execute(
        f"SELECT artigo.titulo, artigo.periodo_de_aluguer, aluguer.data, aluguer.ativo from artigo join aluguer on artigo.id = aluguer.artigo_id join cliente on aluguer.cliente_utilizador_id = cliente.utilizador_id where cliente.utilizador_id = '{utilizador_atual}' and aluguer.ativo = False ORDER by aluguer.data DESC;")

    print(".....................Não Ativos......................")
    for linha in cur.fetchall():
        titulo, periodo_de_aluguer, data, ativo = linha
        print("Título: ", titulo, " | Data: ", data, "| Periodo de Aluguer: ", periodo_de_aluguer, " | Ativo?:", ativo)

def lista():
    while True:
        print("---------------------------------INVENTÁRIO DE ARTIGOS----------------------------------------")

        cur.execute("SELECT id, titulo, tipo from artigo ORDER BY tipo ASC, titulo ASC;")

        for linha in cur.fetchall():
            id, titulo, tipo = linha
            print("Título: ", titulo, "| Tipo: ", tipo, "| ID: ", id)

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
                        cur.execute(
                            f"SELECT titulo, tipo, realizador, produtor, ano from artigo where id = '{artdet}';")
                        detalhes = cur.fetchone()
                        if detalhes is None:
                            print(f"Não existe um artigo com o ID {artdet}")
                            break
                        else:
                            print("\nDetalhes do artigo: ")
                            print(
                                f"Título: {detalhes[0]} | Tipo: {detalhes[1]} | Realizador: {detalhes[2]} | Produtor: {detalhes[3]} | Ano: {detalhes[4]} ")

                            try:
                                cur.execute(
                                    f"SELECT nome FROM atores, artigo_atores WHERE atores.id = artigo_atores.atores_id and artigo_id = {artdet};")
                                nomes = cur.fetchone()
                                if nomes is None:
                                    print("Atores : N/A")
                                else:
                                    print(f"Atores: ")
                                    while nomes is not None:
                                        print(" ", *nomes)
                                        nomes = cur.fetchone()
                            except:
                                print("Atores : N/A")

                            print("\n----------------------------Condições de aluguer--------------------------------------\n")

                            cur.execute(f"SELECT periodo_de_aluguer, preco from artigo, historico_precos where artigo.id = {artdet} and historico_precos.atual = True and historico_precos.artigo_id = {artdet};")

                            for linha in cur.fetchall():
                                periodo_de_aluguer, preco = linha
                                print("Período de aluguer(em meses): ", periodo_de_aluguer, "| Preço: ", preco, " €")

                            while True:

                                det1 = input("""Prentende ALUGAR?

                                Responda (S|N): """)

                                if det1 == "S" or det1 == "s":

                                    #cur.execute(f"INSERT INTO aluguer (id, data, ativo, artigo_id, cliente_utilizador_id) VALUES (DEFAULT, CURRENT_TIMESTAMP, True, (SELECT id from artigo where id = '{artdet}'), '{utilizador_atual}');")

                                    print("\nALUGADO!\n")

                                    alugueres()

                                    break

                                elif det1 == "N" or det1 == "n":
                                    break
                                else:
                                    print("Inválido\nTenta outra vez")

                    except ValueError:
                        print("ERRO!")

                elif voltar == "v" or voltar == "V":
                    print("A VOLTAR AO INVENTÁRIO")
                    break
                else:
                    print("Inválido\nTenta outra vez")

    # Volta ao Inventário
        elif det == "V" or det == "v":
            break

    # Input não válido
        else:
            print("\n\t\t\t\t\tInválido")
            print("\t\t\t\t     Tenta outra vez\n")


lista()

# Fecha a ligação à base de dados
cur.close()
conn.close()