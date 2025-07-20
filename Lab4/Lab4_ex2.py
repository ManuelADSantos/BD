vantagem = input("Indique a vantagem de pontos: ")
vantagem = eval(vantagem)
segundos = input("Indique o numero de segundos que faltam: ")
segundos = eval(segundos)

resultado = vantagem - 3

valido = True

while(valido):
    posse = input("Tem posse de bola?(Y/N)")
    if (posse == 'Y'):
        resultado = resultado + 0.5
        valido = False
    elif (posse == 'N'):
        resultado = resultado - 1
        if (resultado < 0):
            resultado = 0
        valido = False

resultado = resultado ** 2

if (resultado > segundos):
    print("A vantagem é segura")
else:
    print("A vantagem não é segura")

