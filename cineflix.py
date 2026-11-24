import json
from datetime import date
import banco_streaming
import tempo


def pedir_perfil():
    while True:
        nome = input("Nome do perfil: ").strip()
        if nome != "":
            return nome
        print("O nome do perfil não pode ficar vazio.")


def ler_int_positivo(mensagem):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor > 0:
                return valor
            print("Digite um número inteiro maior que zero.")
        except ValueError:
            print("Digite um número inteiro válido.")


if __name__ == "__main__":
    conn = banco_streaming.conectar()
    importados = banco_streaming.importar_catalogo(conn)
    if importados > 0:
        print(f"{importados} títulos importados do catalogo.json.")

    perfil = pedir_perfil()

    while True:
        print(f"\n===== CINEFLIX ({perfil}) =====")
        print("1 - Ver catálogo")
        print("2 - Registrar que assisti")
        print("3 - Meu histórico")
        print("4 - Mais assistidos")
        print("5 - Tempo assistido por perfil")
        print("6 - Exportar relatório JSON")
        print("7 - Trocar de perfil")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            for tid, titulo, tipo, genero, ano, duracao, classif, nota in banco_streaming.listar_catalogo(conn):
                c_str = "L" if classif == 0 else str(classif)
                print(
                    f"{tid:>2}. {titulo:<24} {tipo:<7} {genero:<14} "
                    f"{ano}  {c_str:<3} {tempo.formatar_duracao(duracao):<8} nota {nota:.1f}"
                )

        elif opcao == "2":
            titulo_id = ler_int_positivo("Id do título: ")
            minutos = ler_int_positivo("Quantos minutos você assistiu? ")
            if banco_streaming.registrar_visualizacao(conn, perfil, titulo_id, minutos):
                print("Registrado!")
            else:
                print("Não existe título com esse id.")

        elif opcao == "3":
            registros = banco_streaming.historico_perfil(conn, perfil)
            if not registros:
                print("Nenhuma visualização registrada para este perfil.")
            else:
                total_min = 0
                for data_v, titulo, minutos in registros:
                    total_min += minutos
                    print(f"{data_v}  {titulo:<24} {tempo.formatar_duracao(minutos)}")
                print(f"Total: {tempo.formatar_duracao(total_min)} em {len(registros)} sessões")

        elif opcao == "4":
            top = banco_streaming.mais_assistidos(conn, 5)
            if not top:
                print("Nenhuma visualização registrada ainda.")
            else:
                for pos, (titulo, vezes) in enumerate(top, start=1):
                    print(f"{pos}º {titulo:<24} {vezes} vez(es)")

        elif opcao == "5":
            perfis = banco_streaming.tempo_por_perfil(conn)
            if not perfis:
                print("Nenhuma visualização registrada ainda.")
            else:
                for nome_p, total_min in perfis:
                    print(f"{nome_p:<16} {tempo.formatar_duracao(total_min)}")

        elif opcao == "6":
            top = banco_streaming.mais_assistidos(conn, 5)
            perfis = banco_streaming.tempo_por_perfil(conn)
            relatorio = {
                "data": date.today().isoformat(),
                "mais_assistidos": [
                    {"titulo": titulo, "visualizacoes": vezes} for titulo, vezes in top
                ],
                "tempo_por_perfil": [
                    {
                        "perfil": nome_p,
                        "minutos": total_min,
                        "tempo_formatado": tempo.formatar_duracao(total_min),
                    }
                    for nome_p, total_min in perfis
                ],
            }
            with open("relatorio.json", "w", encoding="utf-8") as f:
                json.dump(relatorio, f, ensure_ascii=False, indent=2)
            print(f"relatorio.json gravado ({len(top)} títulos, {len(perfis)} perfis).")

        elif opcao == "7":
            perfil = pedir_perfil()

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

    conn.close()
