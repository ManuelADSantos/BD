altura = int(input("Insira a altura da escada: "))

linha = 0
largura = altura-1
while(linha<altura):
    print((largura*" ")+"*")
    largura -= 1
    linha += 1
