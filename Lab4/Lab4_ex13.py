frase = input("Insira a frase a inverter: ")
alterada = ""

palavras = frase.split(" " or ",")
for i in range(len(palavras)):
    palavras[i] = palavras[i] [::-1]
    alterada += palavras[i] + " "

print(alterada)
