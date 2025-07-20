altura = int(input("Insira a altura da escada: "))

#Usando um ciclo for
print("Usando um ciclo for")
for i in range(altura):
    print((i*" ")+"*")

#Usando um ciclo while
print("\nUsando um ciclo while")
linha = 0 #Contador de linhas
while(linha<altura):
    print((linha*" ")+"*")
    linha += 1
