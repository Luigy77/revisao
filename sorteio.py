import random
from datetime import datetime
import utilidades

print(utilidades.linha("="))
print("SORTEIO DE BRINDES - FEIRA DE CIÊNCIAS")
print(utilidades.linha("="))
print("Digite os nomes dos participantes (Enter vazio para terminar).")

participantes = []
participantes_lower = []

while True:
    indice = len(participantes) + 1
    nome = utilidades.ler_texto(f"Participante {indice}: ", vazio=True)
    if nome == "":
        if len(participantes) == 0:
            print("Cadastre pelo menos 1 participante.")
            continue
        break

    if nome.lower() in participantes_lower:
        print(f"{nome} já está na lista.")
        continue

    participantes.append(nome)
    participantes_lower.append(nome.lower())

max_brindes = len(participantes)
qtd_brindes = utilidades.ler_inteiro(f"\nQuantos brindes (1 a {max_brindes})? ", 1, max_brindes)

brindes = []
for i in range(1, qtd_brindes + 1):
    brinde = utilidades.ler_texto(f"Brinde {i}: ")
    brindes.append(brinde)

ganhadores = random.sample(participantes, qtd_brindes)
agora = datetime.now().strftime("%d/%m/%Y às %H:%M")

print("\n" + utilidades.linha("-"))
print(f"Sorteio realizado em {agora}")
print(f"{len(participantes)} participantes, {qtd_brindes} brindes")
print(utilidades.linha("-"))

for brinde, ganhador in zip(brindes, ganhadores):
    print(f"{brinde:<20} -> {ganhador}")
