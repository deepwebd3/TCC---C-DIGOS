# =========================
# 📦 IMPORTS
# =========================
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# =========================
# 🔌 ELEMENTO
# =========================
class Elemento:

    def __init__(self, tipo, valor, no1, no2, fase=0):

        self.tipo = tipo
        self.valor = valor
        self.no1 = no1
        self.no2 = no2
        self.fase = fase

    def impedancia(self, omega):

        if self.tipo == "R":
            return self.valor

        elif self.tipo == "L":
            return 1j * omega * self.valor

        elif self.tipo == "C":
            return 1 / (1j * omega * self.valor)

        return None

    def valor_fonte(self):

        return self.valor * np.exp(1j * self.fase)


# =========================
# ⚡ CIRCUITO
# =========================
class Circuito:

    def __init__(self, f=60):

        self.elementos = []
        self.nos = set()
        self.f = f
        self.omega = 2 * np.pi * f

    def adicionar(self, e):

        self.elementos.append(e)
        self.nos.update([e.no1, e.no2])


# =========================
# 🔧 MONTAR CIRCUITO
# =========================
def montar_circuito(dados, f=60):

    c = Circuito(f=f)

    for e in dados:

        c.adicionar(
            Elemento(
                e["tipo"],
                e["valor"],
                e["no1"],
                e["no2"]
            )
        )

    return c


# =========================
# 📦 MOSTRAR COMPONENTES
# =========================
def mostrar_circuito(dados):

    print("\n📦 Componentes do circuito:\n")

    print(f"{'Tipo':12} {'Valor':15} {'Nó 1':8} {'Nó 2':8}")
    print("-"*48)

    for e in dados:

        tipo = e["tipo"]

        if tipo == "R":
            nome = "Resistor"
            unidade = "Ω"

        elif tipo == "C":
            nome = "Capacitor"
            unidade = "F"

        elif tipo == "L":
            nome = "Indutor"
            unidade = "H"

        elif tipo == "V":
            nome = "Fonte V"
            unidade = "V"

        valor = f"{e['valor']} {unidade}"

        print(f"{nome:12} {valor:15} {e['no1']:8} {e['no2']:8}")


# =========================
# 🔎 DESCREVER CIRCUITO
# =========================
def descrever_circuito(dados):

    print("\n🔎 Descrição do circuito:\n")

    for e in dados:

        if e["tipo"] == "V":
            print(f"• Fonte de tensão de {e['valor']} V entre {e['no1']} e {e['no2']}")

        elif e["tipo"] == "R":
            print(f"• Resistor de {e['valor']} Ω entre {e['no1']} e {e['no2']}")

        elif e["tipo"] == "C":
            print(f"• Capacitor de {e['valor']} F entre {e['no1']} e {e['no2']}")

        elif e["tipo"] == "L":
            print(f"• Indutor de {e['valor']} H entre {e['no1']} e {e['no2']}")


# =========================
# 🧠 SOLVER (MNA)
# =========================
def resolver_mna(c, ref="GND"):

    nos = list(c.nos - {ref})
    fontes_v = [e for e in c.elementos if e.tipo == "V"]

    n = len(nos)
    m = len(fontes_v)

    G = np.zeros((n,n), dtype=complex)
    B = np.zeros((n,m), dtype=complex)
    I = np.zeros(n, dtype=complex)
    E = np.zeros(m, dtype=complex)

    idx = {no:i for i,no in enumerate(nos)}

    for e in c.elementos:

        if e.tipo in ["R","L","C"]:

            Z = e.impedancia(c.omega)
            g = 1/Z

            if e.no1 != ref:
                G[idx[e.no1], idx[e.no1]] += g

            if e.no2 != ref:
                G[idx[e.no2], idx[e.no2]] += g

            if e.no1 != ref and e.no2 != ref:

                i = idx[e.no1]
                j = idx[e.no2]

                G[i,j] -= g
                G[j,i] -= g

    for k,e in enumerate(fontes_v):

        E[k] = e.valor_fonte()

        if e.no1 != ref:
            B[idx[e.no1],k] = 1

        if e.no2 != ref:
            B[idx[e.no2],k] = -1

    A = np.block([
        [G,B],
        [B.T, np.zeros((m,m))]
    ])

    Z = np.concatenate([I,E])

    X = np.linalg.solve(A,Z)

    V = X[:n]

    tensoes = {ref:0}

    for no,i in idx.items():
        tensoes[no] = V[i]

    return tensoes


# =========================
# ⚡ POTÊNCIA
# =========================
def potencia(e, tensoes, omega):

    if e.tipo not in ["R","L","C"]:
        return 0,0,0

    V = tensoes[e.no1] - tensoes[e.no2]

    I = V / e.impedancia(omega)

    S = V * np.conj(I)

    return S.real, S.imag, abs(S)


# =========================
# 🔎 ENTRADA / SAÍDA
# =========================
def detectar_entrada_saida(c):

    entrada = None

    for e in c.elementos:

        if e.tipo == "V":
            entrada = e.no1
            break

    nos = list(c.nos - {"GND"})

    saida = None

    for no in nos:

        if no != entrada:
            saida = no

    return entrada,saida


# =========================
# 📈 GANHO
# =========================
def calcular_ganho(tensoes, entrada, saida):

    Vin = tensoes.get(entrada,0)
    Vout = tensoes.get(saida,0)

    if Vin == 0:
        return 0

    return Vout/Vin


# =========================
# 📊 BODE
# =========================
def gerar_bode(c, f_min=10, f_max=1e6, pontos=200, salvar=True, nome_arquivo="bode.png"):
    entrada, saida = detectar_entrada_saida(c)

    if entrada is None or saida is None:
        print("⚠️ Não foi possível detectar entrada e saída para o Bode.")
        return

    freqs = np.logspace(np.log10(f_min), np.log10(f_max), pontos)

    ganho_mag = []
    ganho_fase = []

    for f in freqs:
        c.omega = 2 * np.pi * f
        tensoes = resolver_mna(c)
        H = calcular_ganho(tensoes, entrada, saida)

        mag = abs(H)
        ganho_mag.append(-300 if mag == 0 else 20 * np.log10(mag))
        ganho_fase.append(np.angle(H, deg=True))

    fig, axs = plt.subplots(2, 1, figsize=(8, 8))

    axs[0].semilogx(freqs, ganho_mag)
    axs[0].set_title("Bode - Magnitude")
    axs[0].set_ylabel("Ganho (dB)")
    axs[0].grid(True, which="both")

    axs[1].semilogx(freqs, ganho_fase)
    axs[1].set_title("Bode - Fase")
    axs[1].set_xlabel("Frequência (Hz)")
    axs[1].set_ylabel("Fase (graus)")
    axs[1].grid(True, which="both")

    plt.tight_layout()

    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


# =========================
# 🎨 DESENHAR CIRCUITO
# =========================
def desenhar(c, salvar=True, nome_arquivo="circuito.png"):
    G = nx.Graph()

    for e in c.elementos:
        G.add_edge(e.no1, e.no2, label=f"{e.tipo}:{e.valor}")

    pos = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, "label"),
        font_size=9
    )

    plt.title("Circuito")

    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
        plt.close()
    else:
        plt.show()
        plt.close()


# =========================
# 🚀 EXECUÇÃO
# =========================
if __name__ == "__main__":

    print("⚡ Simulador Offline de Circuitos")

    dados = [
        {"tipo": "V", "valor": 10, "no1": "A", "no2": "GND"},
        {"tipo": "R", "valor": 10, "no1": "A", "no2": "B"},
        {"tipo": "C", "valor": 100e-6, "no1": "B", "no2": "GND"}
    ]

    # descrição
    descrever_circuito(dados)

    # tabela
    mostrar_circuito(dados)

    # montar circuito
    c = montar_circuito(dados)

    # resolver circuito
    tensoes = resolver_mna(c)

    print("\n⚡ Tensões nos nós:")

    for no, v in tensoes.items():
        print(f"{no}: {v:.4f}")

    print("\n🔌 Potência:")

    for e in c.elementos:

        P, Q, S = potencia(e, tensoes, c.omega)

        if e.tipo in ["R", "L", "C"]:
            print(f"{e.tipo} {e.no1}-{e.no2}: P={P:.4f} W | Q={Q:.4f} VAR | S={S:.4f} VA")

    entrada, saida = detectar_entrada_saida(c)

    print(f"\n🔎 Entrada: {entrada}")
    print(f"🔎 Saída: {saida}")

    ganho = calcular_ganho(tensoes, entrada, saida)

    print(f"\n📈 Ganho = {ganho}")
    print(f"|Ganho| = {abs(ganho):.4f}")
    print(f"Ganho dB = {20*np.log10(abs(ganho)):.4f}")

    # salvar imagens
    desenhar(c, salvar=True, nome_arquivo="circuito.png")
    gerar_bode(c, salvar=True, nome_arquivo="bode.png")

    print("\n✅ Figuras salvas:")
    print(" - circuito.png")
    print(" - bode.png")

    # fecha matplotlib corretamente
    plt.close("all")