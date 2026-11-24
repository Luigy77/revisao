from datetime import datetime, date


def converter_data(texto):
    return datetime.strptime(texto.strip(), "%d/%m/%Y").date()


def dias_de_atraso(data_prevista, data_devolucao):
    atraso = (data_devolucao - data_prevista).days
    return max(0, atraso)


def valor_multa(dias, por_dia=1.50, maximo=30.00):
    if dias <= 0:
        return 0.0
    total = dias * por_dia
    return min(total, float(maximo))


if __name__ == "__main__":
    d1 = converter_data("05/11/2026")
    d2 = converter_data("10/11/2026")
    d3 = converter_data("01/11/2026")

    assert d1 == date(2026, 11, 5)
    assert dias_de_atraso(d1, d2) == 5
    assert dias_de_atraso(d1, d3) == 0
    assert valor_multa(5) == 7.5
    assert valor_multa(40) == 30.0
    assert valor_multa(5, por_dia=2) == 10.0
    print("Todos os testes de multas.py passaram com sucesso!")
