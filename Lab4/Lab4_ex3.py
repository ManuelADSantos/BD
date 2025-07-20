preco = float(input("Indique o preço da fruta: "))
quantidade = float(input("Indique a quantidade de fruta a comprar: "))
limite = float(input("Quantidade a partir do qual há desconto: "))

if(quantidade > limite):
    custo = (limite * preco) + ((quantidade - limite) * 0.75 * preco)
    print("(Há desconto) Total a pagar: ", round(custo,3))
else:
    custo = quantidade * preco
    print("(Não há desconto) Total a pagar: ", round(custo,3))

