erro_max = input("Indique o erro máximo admitido no cálculo da série harmónica: ")
erro_max = eval(erro_max)

valido = True
count = 1
resultado = 0

while(valido):
    anterior = resultado
    resultado += 1/count
    #print(resultado)
    count += 1
    if(resultado - anterior <= erro_max):
        break

print("O valor aproximado da série harmónica de erro máximo ", erro_max, " é ", resultado)
