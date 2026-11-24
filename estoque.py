import banco_estoque


def exibir_produtos(produtos):
    if not produtos:
        print("Nenhum produto encontrado.")
        return
    print(f"{'Id':>3}  {'Produto':<22} {'Categoria':<15} {'Preço':>8} {'Qtd':>5}")
    for pid, nome, categoria, preco, qtd, minimo in produtos:
        alerta = " <- repor" if qtd < minimo else ""
        print(f"{pid:>3}  {nome:<22} {categoria:<15} {preco:>8.2f} {qtd:>5}{alerta}")


def ler_int(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo is not None and valor < minimo:
                print(f"Digite um número inteiro maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_float(mensagem, minimo=0.0):
    while True:
        try:
            valor = float(input(mensagem).strip().replace(",", "."))
            if valor >= minimo:
                return valor
            print(f"Digite um valor maior ou igual a {minimo}.")
        except ValueError:
            print("Digite um número válido.")


def ler_texto_obrigatorio(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Este campo não pode ficar vazio.")


if __name__ == "__main__":
    conn = banco_estoque.conectar()

    while True:
        print("\n===== ESTOQUE - LOJA DE CAMPING =====")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Buscar por nome")
        print("4 - Entrada (chegou mercadoria)")
        print("5 - Saída (venda)")
        print("6 - Produtos para repor")
        print("7 - Valor total do estoque")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = ler_texto_obrigatorio("Nome do produto: ")
            categoria = ler_texto_obrigatorio("Categoria: ")
            preco = ler_float("Preço: R$ ", 0.01)
            qtd = ler_int("Quantidade inicial: ", 0)
            minimo = ler_int("Estoque mínimo: ", 0)
            novo_id = banco_estoque.cadastrar(conn, nome, categoria, preco, qtd, minimo)
            print(f"Produto cadastrado com id {novo_id}.")

        elif opcao == "2":
            exibir_produtos(banco_estoque.listar(conn))

        elif opcao == "3":
            termo = input("Parte do nome: ").strip()
            exibir_produtos(banco_estoque.buscar(conn, termo))

        elif opcao == "4":
            pid = ler_int("Id do produto: ", 1)
            qtd = ler_int("Quantidade que chegou: ", 1)
            if banco_estoque.entrada(conn, pid, qtd):
                print("Entrada registrada.")
            else:
                print("Produto não encontrado.")

        elif opcao == "5":
            pid = ler_int("Id do produto: ", 1)
            qtd = ler_int("Quantidade vendida: ", 1)
            mensagem = banco_estoque.saida(conn, pid, qtd)
            print(mensagem)

        elif opcao == "6":
            exibir_produtos(banco_estoque.estoque_baixo(conn))

        elif opcao == "7":
            total = banco_estoque.valor_total(conn)
            print(f"Valor total em estoque: R$ {total:.2f}")

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

    conn.close()
