primeiroNome = input("Insira o seu primeiro nome: ")
meioNome = input("Insira o seu nome do meio: ")
ultimoNome = input("Insira o seu último nome: ")

nome = primeiroNome + "," + meioNome + "," + ultimoNome

virg1=0
while (virg1 < len(nome) and nome[virg1] != ","):
    virg1 += 1

virg2=virg1+1
while (virg2 < len(nome) and nome[virg2] != ","):
    virg2 += 1

print("\nPrimeiro Nome: ", nome[:virg1])                                                         #Primeiro nome
print("Último Nome: ", nome[virg2+1:])                                                 #Último nome
print("Último Nome seguido do Primeiro Nome: ", nome[virg2+1:] + "," + nome[:virg1])  #Último Nome seguido do Primeiro Nome
print("O seu nome tem ", len(nome)-2, " carateres de comprimento")                              #Comprimento do Nome
