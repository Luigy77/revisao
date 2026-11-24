from datetime import date
import multas

print("=== BALCÃO DE DEVOLUÇÕES ===")

total_livros = 0
com_atraso = 0
total_multas = 0.0

while True:
    titulo = input("Título do livro (Enter para encerrar): ").strip()
    if titulo == "":
        break

    while True:
        prev_str = input("Data prevista (dd/mm/aaaa): ").strip()
        try:
            data_prevista = multas.converter_data(prev_str)
            break
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")

    while True:
        dev_str = input("Data da devolução (Enter = hoje): ").strip()
        if dev_str == "":
            data_devolucao = date.today()
            break
        try:
            data_devolucao = multas.converter_data(dev_str)
            break
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")

    atraso = multas.dias_de_atraso(data_prevista, data_devolucao)
    multa = multas.valor_multa(atraso)

    total_livros += 1
    if atraso > 0:
        com_atraso += 1
        total_multas += multa
        print(f"'{titulo}' com {atraso} dia(s) de atraso. Multa: R$ {multa:.2f}\n")
    else:
        print(f"'{titulo}' devolvido no prazo. Obrigado!\n")

print("\n=== FECHAMENTO DO DIA ===")
print(f"Livros devolvidos: {total_livros}")
print(f"Com atraso: {com_atraso}")
print(f"Total em multas: R$ {total_multas:.2f}")
