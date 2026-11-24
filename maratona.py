def formatar_duracao(minutos):
    horas = minutos // 60
    resto = minutos % 60
    if horas > 0:
        return f"{horas}h{resto:02d}min"
    return f"{resto}min"


def tempo_total(duracoes):
    soma = 0
    for d in duracoes:
        soma += d
    return soma


def dias_para_terminar(total_minutos, minutos_por_dia=120):
    return (total_minutos + minutos_por_dia - 1) // minutos_por_dia


def classificar_maratona(total_minutos):
    if total_minutos < 300:
        return "Leve"
    elif total_minutos <= 900:
        return "Média"
    return "Intensa"


def ler_inteiro_positivo(mensagem):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor > 0:
                return valor
            print("Digite um número inteiro maior que zero.")
        except ValueError:
            print("Digite um número inteiro válido.")


if __name__ == "__main__":
    print("=== MARATONA DE SÉRIE ===")
    while True:
        serie = input("Nome da série: ").strip()
        if serie != "":
            break
        print("O nome da série não pode ficar vazio.")

    temporadas = ler_inteiro_positivo("Quantas temporadas? ")
    duracoes_temporadas = []

    for t in range(1, temporadas + 1):
        episodios = ler_inteiro_positivo(f"Temporada {t} - número de episódios: ")
        duracao_ep = ler_inteiro_positivo(f"Temporada {t} - duração média do episódio (min): ")
        duracoes_temporadas.append(episodios * duracao_ep)

    print(f"\n=== {serie.upper()} ===")
    for i, duracao in enumerate(duracoes_temporadas, start=1):
        print(f"Temporada {i}: {formatar_duracao(duracao)}")

    total = tempo_total(duracoes_temporadas)
    classificacao = classificar_maratona(total)
    print(f"Total: {formatar_duracao(total)} ({classificacao})\n")

    min_dia = ler_inteiro_positivo("Quantos minutos por dia você pode assistir? ")
    dias_usuario = dias_para_terminar(total, min_dia)
    dias_padrao = dias_para_terminar(total)

    print(f"Você termina {serie} em {dias_usuario} dias.")
    print(f"Com 2 horas por dia (padrão), seriam {dias_padrao} dias.")
