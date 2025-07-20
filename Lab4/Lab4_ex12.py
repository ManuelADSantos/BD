cadeia1 = input("Insira uma string: ")
cadeia2 = input("Insira outra string: ")


for i in range(len(cadeia1)):
    for j in range(len(cadeia2)):
        if(cadeia1[i] == cadeia2[j]):
            cadeia2 = cadeia2.replace(cadeia2[j], " ")

count = 0
aux = ""
for k in range(len(cadeia2)):
        if(cadeia2[k] != " "):
            aux += cadeia2[k]
            count += 1

print("\nString alterada: ",aux)
