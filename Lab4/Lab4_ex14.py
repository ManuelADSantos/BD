frase = input("Insira a frase a inverter: ")
alterada = ""

palavras = frase.split(" ")
for i in range(len(palavras)):
    if (palavras[i] != ""):
        alterada += palavras[i] + " "

print(alterada)
