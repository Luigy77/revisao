import json
import os
from datetime import datetime

ARQUIVO = "shows.json"


def carregar_shows():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_shows(shows):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(shows, f, ensure_ascii=False, indent=2)


def ordenar_por_data(shows):
    return sorted(shows, key=lambda s: datetime.strptime(s["data"], "%d/%m/%Y"))


def listar_shows(shows):
    if not shows:
        print("Nenhum show cadastrado.")
        return []
    ordenados = ordenar_por_data(shows)
    for i, s in enumerate(ordenados, start=1):
        status = "ESGOTADO" if s["ingressos"] == 0 else f"{s['ingressos']} ingressos"
        print(
            f"{i}. {s['data']}  {s['artista']:<20} {s['cidade']:<16} "
            f"R$ {s['preco']:>6.2f}  {status}"
        )
    return ordenados


def cadastrar_show(shows):
    while True:
        artista = input("Artista/banda: ").strip()
        if artista != "":
            break
        print("Informe o artista ou banda.")

    while True:
        cidade = input("Cidade: ").strip()
        if cidade != "":
            break
        print("Informe a cidade.")

    while True:
        data_str = input("Data (dd/mm/aaaa): ").strip()
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            break
        except ValueError:
            print("Data inválida. Digite no formato dd/mm/aaaa:")

    while True:
        try:
            preco = float(input("Preço do ingresso: R$ ").strip().replace(",", "."))
            if preco >= 0:
                break
            print("O preço não pode ser negativo.")
        except ValueError:
            print("Digite um valor numérico.")

    while True:
        try:
            ingressos = int(input("Ingressos disponíveis: ").strip())
            if ingressos >= 0:
                break
            print("Digite um número inteiro (0 ou mais).")
        except ValueError:
            print("Digite um número inteiro válido.")

    shows.append({
        "artista": artista,
        "cidade": cidade,
        "data": data_str,
        "preco": preco,
        "ingressos": ingressos,
    })
    salvar_shows(shows)
    print("Show cadastrado e agenda salva.")


def buscar_por_cidade(shows):
    cidade = input("Cidade: ").strip().lower()
    filtrados = [s for s in shows if s["cidade"].lower() == cidade]
    listar_shows(filtrados)


def vender_ingressos(shows):
    ordenados = listar_shows(shows)
    if not ordenados:
        return

    while True:
        try:
            num = int(input("Número do show: ").strip())
            if 1 <= num <= len(ordenados):
                break
            print("Número de show inválido.")
        except ValueError:
            print("Digite um número inteiro.")

    show = ordenados[num - 1]
    if show["ingressos"] == 0:
        print("Este show está ESGOTADO.")
        return

    while True:
        try:
            qtd = int(input("Quantos ingressos? ").strip())
            if qtd > 0:
                break
            print("Digite uma quantidade maior que zero.")
        except ValueError:
            print("Digite um número inteiro.")

    if qtd > show["ingressos"]:
        print(f"Só restam {show['ingressos']} ingressos.")
        return

    show["ingressos"] -= qtd
    total = qtd * show["preco"]
    salvar_shows(shows)
    print(f"Venda: {qtd} x R$ {show['preco']:.2f} = R$ {total:.2f}")


def remover_show(shows):
    ordenados = listar_shows(shows)
    if not ordenados:
        return

    while True:
        try:
            num = int(input("Número do show: ").strip())
            if 1 <= num <= len(ordenados):
                break
            print("Número de show inválido.")
        except ValueError:
            print("Digite um número inteiro.")

    alvo = ordenados[num - 1]
    shows.remove(alvo)
    salvar_shows(shows)
    print(f"Show de {alvo['artista']} removido.")


if __name__ == "__main__":
    shows = carregar_shows()
    print(f"Agenda carregada: {len(shows)} shows.")

    while True:
        print("\n===== AGENDA DE SHOWS =====")
        print("1 - Listar shows")
        print("2 - Cadastrar show")
        print("3 - Shows em uma cidade")
        print("4 - Vender ingressos")
        print("5 - Remover show")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            listar_shows(shows)
        elif opcao == "2":
            cadastrar_show(shows)
        elif opcao == "3":
            buscar_por_cidade(shows)
        elif opcao == "4":
            vender_ingressos(shows)
        elif opcao == "5":
            remover_show(shows)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
