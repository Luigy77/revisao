def ler_texto(mensagem, vazio=False):
    while True:
        texto = input(mensagem).strip()
        if vazio or texto != "":
            return texto
        print("Este campo não pode ficar vazio.")


def ler_inteiro(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo is not None and valor < minimo:
                print(f"O mínimo é {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"O máximo é {maximo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro válido.")


def linha(caractere="-", tamanho=40):
    return caractere * tamanho


if __name__ == "__main__":
    print(linha("=", 30))
    print("Teste do módulo utilidades.py")
    print(linha("-", 30))
    nome = ler_texto("Digite um nome obrigatório: ")
    obs = ler_texto("Observação (opcional): ", vazio=True)
    num = ler_inteiro("Digite um número de 1 a 10: ", 1, 10)
    print(f"Resultado: {nome} | {obs} | {num}")
