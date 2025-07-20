num = input("Indique o número cuja soma dos dígitos quer calcular: ")

sum = 0
for i in range(len(num)):
    sum += eval(num[i])

print("A soma dos dígitos de ", num, " é ",sum)
