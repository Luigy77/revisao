itens = []
pesos = []
limite = 15.0
aviso_exibido = False

print("=== MOCHILA DE CAMPING ===")
print("Digite os itens. Para terminar, digite FIM.\n")

while True:
    nome = input("Item: ").strip()
    if nome.upper() == "FIM":
        break
    if nome == "":
        print("Digite o nome de um item ou FIM para encerrar.")
        continue

    while True:
        peso_str = input("Peso (kg): ").strip().replace(",", ".")
        try:
            peso = float(peso_str)
            if peso <= 0:
                print("O peso deve ser maior que zero.")
            else:
                break
        except ValueError:
            print("Digite um número, por exemplo 1.5")

    itens.append(nome)
    pesos.append(peso)

    peso_atual = sum(pesos)
    if peso_atual > limite and not aviso_exibido:
        print(f"Atenção: a mochila já tem {peso_atual:.1f} kg (limite 15 kg)!")
        aviso_exibido = True

print("\n=== RESUMO ===")

if len(itens) == 0:
    print("A mochila está vazia.")
else:
    for i in range(len(itens)):
        print(f"{i + 1}. {itens[i]:<20} {pesos[i]:.1f} kg")

    qtd_itens = len(itens)
    peso_total = sum(pesos)
    peso_medio = peso_total / qtd_itens
    maior_peso = max(pesos)
    item_mais_pesado = itens[pesos.index(maior_peso)]

    print(f"Itens: {qtd_itens}")
    print(f"Peso total: {peso_total:.1f} kg")
    print(f"Peso médio: {peso_medio:.2f} kg")
    print(f"Item mais pesado: {item_mais_pesado} ({maior_peso:.1f} kg)")

    if peso_total > limite:
        print(f"Tire {peso_total - limite:.1f} kg da mochila para ficar dentro do limite.")
    elif peso_total < limite:
        print(f"Ainda cabem {limite - peso_total:.1f} kg na mochila.")
    else:
        print("A mochila está no limite exato de 15.0 kg.")
