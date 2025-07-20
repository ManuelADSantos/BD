numInicial = int(input("Indique o primeiro valor do intervalo(inteiro): "))
numFinal = int(input("Indique o último valor do intervalo(inteiro): "))

lista = range(numInicial, numFinal+1, 1)

soma = 0;
for i in range(numFinal-numInicial):
    if ((lista[i])%2 == 0):
        soma = soma + lista[i]

print("A soma dos valores pares no intervalo [", numInicial, ",", numFinal,"] é ", soma)