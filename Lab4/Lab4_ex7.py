num = int(input("Indique o número a verificar se é perfeito: "))
divisores = list(range(num))
ind = 0

for i in range(1, num):
    #print("Índice ",ind)
    if (num%i == 0):
        #print("Número ", i)
        divisores[ind] = i
        #print("Número guardado ", divisores[ind])
        ind += 1

mostra = True
if (ind != 0):
    print("\nO número ", num," é perfeito")
    frase = ""
    for j in range(ind):
        frase += str(divisores[j])
        if(mostra == True):
            if(j==ind-1):
                mostra = False
            else:
                frase += " + "
    print(num, " = ", frase)

else:
    print("O número ", num," não é perfeito")
