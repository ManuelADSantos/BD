numInicial = int(input("Indique o primeiro número do intervalo: "))
numFinal = int(input("Indique o último número do intervalo: ")) + 1

for a in range(numInicial,numFinal):
    num = a
    divisores = list(range(num))
    ind = 0
    teste = False
    sum = 0

    for i in range(1, num):
        if (num%i == 0):
            divisores[ind] = i
            ind += 1

    for k in range(ind):
        sum += divisores[k]

    if(sum == num):
        teste = True

    mostra = True
    if (teste == True):
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
