#INVENTARIO

import psycopg2
import psycopg2.extras

# A função connect permite estabelecer uma ligação a uma base de dados
# Verifique se a password é igual à que escolheu na instalação de PostgreSQL
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

# Cria um objecto (cursor) que permite executar operações sobre a base de dados
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def historico ():

    print("\n--------------------------------Histórico de preços----------------------------------------------\n")

    cur.execute(f"SELECT h.preco, h.entrada_em_vigor, h.atual from historico_precos as h join artigo as a on h.artigo_id = a.id where titulo = '{artdet}' ORDER BY h.entrada_em_vigor DESC;")

    for linha in cur.fetchall():
        preco, entrada_em_vigor, atual = linha
        print("Preço: ", preco, "€ | Entrada em vigor: ", entrada_em_vigor, " | Atual?:", atual)

    while True:
        corrigir = input("\nCorrigir Preço? (S|N): \n")

        if corrigir == "S" or corrigir == "s":

            print("--------------------------------------CORRIGIR PREÇO---------------------------------------------------")
            break

        elif corrigir == "N" or corrigir == "n":
            break

        else:
            print("S|N")

print("----------------------------------------INVENTÁRIO DE ARTIGOS-----------------------------------------------")

cur.execute("SELECT titulo, tipo from artigo ORDER BY tipo ASC, titulo ASC;")

for linha in cur.fetchall():
    titulo, tipo = linha
    print("Título: ", titulo,"| Tipo: ", tipo)

inv = True
while inv:
        print("----------------------INVENTÁRIO---------------------")
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

                print("\n Mais detalhes: \n")

                while True:

                    det1 = input("""
                                1- Histórico de preços
                                2- Condições de ALuguer
                                V|v - Voltar
                    VER: """)

                    if det1 == "1":
                        historico()

                    elif det1 == "2":

                        print("\n----------------------------Condições de aluguer--------------------------------------\n")

                        cur.execute(f"SELECT a.periodo_de_aluguer, h.preco from artigo as a join historico_precos as h on a.id = h.artigo_id where a.titulo = '{artdet}' and h.atual = True;")

                        for linha in cur.fetchall():
                            periodo_de_aluguer, preco = linha
                            print("Período de aluguer: ", periodo_de_aluguer, "| Preço: ", preco, " €")

                    elif det1 == "V" or det1 == "v":
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



# Fecha a ligação à base de dados
cur.close()
conn.close()
