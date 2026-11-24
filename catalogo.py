import json


def carregar_catalogo(caminho="catalogo.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def formatar_classificacao(idade):
    return "L" if idade == 0 else str(idade)


def exibir_titulos(lista):
    if not lista:
        print("Nenhum título encontrado.")
        return
    for t in lista:
        classif = formatar_classificacao(t["classificacao"])
        print(
            f"{t['id']:>2}. {t['titulo']:<24} {t['tipo']:<7} "
            f"{t['genero']:<14} {t['ano']}  {classif:<3} nota {t['nota']:.1f}"
        )


def listar_tudo(catalogo):
    exibir_titulos(catalogo)


def obter_generos(catalogo):
    return sorted({t["genero"] for t in catalogo})


def filtrar_por_genero(catalogo, genero):
    alvo = genero.strip().lower()
    return [t for t in catalogo if t["genero"].lower() == alvo]


def buscar_titulo(catalogo, termo):
    alvo = termo.strip().lower()
    return [t for t in catalogo if alvo in t["titulo"].lower()]


def filtrar_por_idade(catalogo, idade):
    return [t for t in catalogo if t["classificacao"] <= idade]


def mais_bem_avaliados(catalogo, n=5):
    ordenados = sorted(catalogo, key=lambda t: t["nota"], reverse=True)
    return ordenados[:n]


def estatisticas(catalogo):
    total = len(catalogo)
    filmes = sum(1 for t in catalogo if t["tipo"].lower() == "filme")
    series = sum(1 for t in catalogo if t["tipo"].lower() == "série")
    media = sum(t["nota"] for t in catalogo) / total if total > 0 else 0.0
    generos = obter_generos(catalogo)
    print(f"Títulos: {total} (filmes: {filmes}, séries: {series})")
    print(f"Nota média: {media:.2f}")
    print(f"Gêneros: {', '.join(generos)}")


if __name__ == "__main__":
    catalogo = carregar_catalogo()
    print(f"Catálogo carregado: {len(catalogo)} títulos.")

    while True:
        print("\n===== CINEFLIX =====")
        print("1 - Listar tudo")
        print("2 - Filtrar por gênero")
        print("3 - Buscar título")
        print("4 - Títulos para a minha idade")
        print("5 - Mais bem avaliados")
        print("6 - Estatísticas")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            listar_tudo(catalogo)
        elif opcao == "2":
            generos = obter_generos(catalogo)
            print(f"Gêneros: {', '.join(generos)}")
            g = input("Gênero: ").strip()
            exibir_titulos(filtrar_por_genero(catalogo, g))
        elif opcao == "3":
            termo = input("Parte do título: ").strip()
            exibir_titulos(buscar_titulo(catalogo, termo))
        elif opcao == "4":
            while True:
                try:
                    idade = int(input("Sua idade: ").strip())
                    if idade >= 0:
                        break
                    print("Digite uma idade válida (0 ou mais).")
                except ValueError:
                    print("Digite um número inteiro.")
            exibir_titulos(filtrar_por_idade(catalogo, idade))
        elif opcao == "5":
            while True:
                qtd_str = input("Quantos (Enter = 5)? ").strip()
                if qtd_str == "":
                    qtd = 5
                    break
                try:
                    qtd = int(qtd_str)
                    if qtd > 0:
                        break
                    print("Digite um número maior que zero.")
                except ValueError:
                    print("Digite um número inteiro válido.")
            exibir_titulos(mais_bem_avaliados(catalogo, qtd))
        elif opcao == "6":
            estatisticas(catalogo)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
