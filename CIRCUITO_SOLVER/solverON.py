# =========================
# 📦 IMPORTS
# =========================
import os
import re
import json
import base64
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from openai import OpenAI

# =========================
# 🔑 CONFIGURAÇÃO DA API
# =========================
client = None
IA_ATIVA = False

def inicializar_openai():
    global client, IA_ATIVA

    api_key = os.getenv("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")

    if not api_key:
        IA_ATIVA = False
        print("⚠️ OPENAI_API_KEY não encontrada.")
        print("⚠️ A IA foi desativada. Use modo='manual' para testar o solver sem IA.")
        return

    try:
        client = OpenAI(api_key=api_key)
        IA_ATIVA = True
        print("✅ OpenAI inicializada com sucesso.")
    except Exception as e:
        client = None
        IA_ATIVA = False
        print("❌ Erro ao inicializar a OpenAI:")
        print(f"   {type(e).__name__}: {e}")


# =========================
# 🧹 UTILITÁRIOS
# =========================
def limpar_json_resposta(conteudo):
    """
    Remove blocos ```json ... ``` e tenta extrair apenas o JSON.
    """
    if conteudo is None:
        raise ValueError("Resposta vazia da IA.")

    conteudo = conteudo.strip()

    # remove blocos markdown
    conteudo = re.sub(r"^```json\s*", "", conteudo, flags=re.IGNORECASE)
    conteudo = re.sub(r"^```\s*", "", conteudo)
    conteudo = re.sub(r"\s*```$", "", conteudo)

    # tenta extrair lista JSON
    inicio_lista = conteudo.find("[")
    fim_lista = conteudo.rfind("]")

    # tenta extrair objeto JSON
    inicio_obj = conteudo.find("{")
    fim_obj = conteudo.rfind("}")

    if inicio_lista != -1 and fim_lista != -1 and inicio_lista < fim_lista:
        conteudo = conteudo[inicio_lista:fim_lista + 1]
    elif inicio_obj != -1 and fim_obj != -1 and inicio_obj < fim_obj:
        conteudo = conteudo[inicio_obj:fim_obj + 1]

    return json.loads(conteudo)


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
# 🤖 IA → TEXTO → JSON
# =========================
def texto_para_circuito(texto):
    if not IA_ATIVA or client is None:
        print("⚠️ IA desativada.")
        return None

    try:
        resposta = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": """
Converta a descrição textual de um circuito em JSON válido.

Formato:
[
  {"tipo":"V","valor":10,"no1":"A","no2":"GND"},
  {"tipo":"R","valor":1000,"no1":"A","no2":"B"},
  {"tipo":"C","valor":100e-6,"no1":"B","no2":"GND"}
]

Regras:
- Use apenas: R, L, C, V, I
- Retorne somente JSON
- Sem explicações
- Sem markdown
- Use GND para terra
- Nós simples: A, B, C...
- Se houver fase em fonte AC, inclua "fase"
"""
                },
                {"role": "user", "content": texto}
            ]
        )

        conteudo = resposta.choices[0].message.content
        return limpar_json_resposta(conteudo)

    except Exception as e:
        print("❌ Erro ao converter texto em circuito:")
        print(f"   {type(e).__name__}: {e}")
        return None


# =========================
# 🖼️ IA → IMAGEM → JSON
# =========================
def imagem_para_circuito(caminho_imagem):
    if not IA_ATIVA or client is None:
        print("⚠️ IA desativada.")
        return None

    if not os.path.exists(caminho_imagem):
        print(f"❌ Imagem não encontrada: {caminho_imagem}")
        return None

    try:
        with open(caminho_imagem, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8")

        ext = os.path.splitext(caminho_imagem)[1].lower()
        if ext == ".png":
            mime = "image/png"
        elif ext in [".jpg", ".jpeg"]:
            mime = "image/jpeg"
        else:
            print("❌ Formato de imagem não suportado. Use PNG, JPG ou JPEG.")
            return None

        resposta = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": """
Você é um extrator de circuitos a partir de imagem.

Analise a imagem e devolva SOMENTE um JSON válido neste formato:

[
  {"tipo":"V","valor":10,"no1":"A","no2":"GND"},
  {"tipo":"R","valor":1000,"no1":"A","no2":"B"},
  {"tipo":"C","valor":100e-6,"no1":"B","no2":"GND"}
]

Regras:
- Use apenas: R, L, C, V, I
- Sem explicações
- Sem markdown
- Retorne somente JSON puro
- Converta 1k para 1000
- Converta 100uF para 100e-6
- Converta 10mH para 10e-3
- Use GND para terra
- Use nós simples: A, B, C...
- Se houver fase em fonte AC, inclua "fase"
"""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Leia esta imagem e extraia o circuito em JSON."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime};base64,{img_base64}"
                            }
                        }
                    ]
                }
            ]
        )

        conteudo = resposta.choices[0].message.content
        return limpar_json_resposta(conteudo)

    except Exception as e:
        print("❌ Erro ao converter imagem em circuito:")
        print(f"   {type(e).__name__}: {e}")
        return None


# =========================
# 🔧 JSON → CIRCUITO
# =========================
def montar_circuito(dados, f=60):
    c = Circuito(f=f)

    for e in dados:
        c.adicionar(
            Elemento(
                e["tipo"],
                e["valor"],
                e["no1"],
                e["no2"],
                e.get("fase", 0)
            )
        )

    return c


# =========================
# 🧠 SOLVER (MNA)
# =========================
def resolver_mna(c, ref="GND"):
    nos = list(c.nos - {ref})
    fontes_v = [e for e in c.elementos if e.tipo == "V"]

    n = len(nos)
    m = len(fontes_v)

    G = np.zeros((n, n), dtype=complex)
    B = np.zeros((n, m), dtype=complex)
    I = np.zeros(n, dtype=complex)
    E = np.zeros(m, dtype=complex)

    idx = {no: i for i, no in enumerate(nos)}

    for e in c.elementos:
        if e.tipo in ["R", "L", "C"]:
            Z = e.impedancia(c.omega)
            if Z == 0:
                raise ValueError(f"Impedância nula no elemento {e.tipo} entre {e.no1} e {e.no2}")

            g = 1 / Z

            if e.no1 != ref:
                G[idx[e.no1], idx[e.no1]] += g
            if e.no2 != ref:
                G[idx[e.no2], idx[e.no2]] += g

            if e.no1 != ref and e.no2 != ref:
                i, j = idx[e.no1], idx[e.no2]
                G[i, j] -= g
                G[j, i] -= g

        elif e.tipo == "I":
            val = e.valor_fonte()
            if e.no1 != ref:
                I[idx[e.no1]] -= val
            if e.no2 != ref:
                I[idx[e.no2]] += val

    for k, e in enumerate(fontes_v):
        E[k] = e.valor_fonte()
        if e.no1 != ref:
            B[idx[e.no1], k] = 1
        if e.no2 != ref:
            B[idx[e.no2], k] = -1

    A = np.block([
        [G, B],
        [B.T, np.zeros((m, m), dtype=complex)]
    ])
    Zvet = np.concatenate([I, E])

    X = np.linalg.solve(A, Zvet)
    V = X[:n]

    tensoes = {ref: 0}
    for no, i in idx.items():
        tensoes[no] = V[i]

    return tensoes


# =========================
# 🔌 CORRENTE
# =========================
def corrente(e, tensoes, omega):
    if e.tipo in ["R", "L", "C"]:
        return (tensoes[e.no1] - tensoes[e.no2]) / e.impedancia(omega)
    return None


# =========================
# ⚡ POTÊNCIA
# =========================
def potencia(e, tensoes, omega):
    if e.tipo not in ["R", "L", "C"]:
        return 0, 0, 0

    V = tensoes[e.no1] - tensoes[e.no2]
    I = corrente(e, tensoes, omega)
    S = V * np.conj(I)

    return S.real, S.imag, abs(S)


# =========================
# 🔎 DETECTAR ENTRADA/SAÍDA
# =========================
def detectar_entrada_saida(c, ref="GND"):
    entrada = None

    for e in c.elementos:
        if e.tipo == "V":
            entrada = e.no1
            break

    nos = list(c.nos - {ref})
    saida = None
    for no in nos:
        if no != entrada:
            saida = no

    return entrada, saida


# =========================
# 📈 GANHO
# =========================
def calcular_ganho(tensoes, entrada, saida):
    Vin = tensoes.get(entrada, 0)
    Vout = tensoes.get(saida, 0)

    if Vin == 0:
        return 0

    return Vout / Vin


# =========================
# 📊 BODE
# =========================
def gerar_bode(c, f_min=10, f_max=1e6, pontos=200):
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

    plt.figure(figsize=(8, 5))
    plt.semilogx(freqs, ganho_mag)
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Ganho (dB)")
    plt.title("Bode - Magnitude")
    plt.grid(True, which="both")
    plt.tight_layout()

    plt.figure(figsize=(8, 5))
    plt.semilogx(freqs, ganho_fase)
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Fase (graus)")
    plt.title("Bode - Fase")
    plt.grid(True, which="both")
    plt.tight_layout()

    plt.show()


# =========================
# 🎨 VISUALIZAÇÃO
# =========================
def desenhar(c):
    G = nx.Graph()

    for e in c.elementos:
        G.add_edge(e.no1, e.no2, label=f"{e.tipo}:{e.valor}")

    pos = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=nx.get_edge_attributes(G, "label"),
        font_size=9
    )

    plt.title("Representação do Circuito")
    plt.show()


# =========================
# 🧾 RELATÓRIO
# =========================
def mostrar_resultados(c, tensoes):
    print("\n⚡ Tensões nos nós:")
    for no, v in tensoes.items():
        print(f"{no}: {v:.4f}")

    print("\n🔌 Potência nos elementos passivos:")
    for e in c.elementos:
        P, Q, S = potencia(e, tensoes, c.omega)
        if e.tipo in ["R", "L", "C"]:
            print(f"{e.tipo} {e.no1}-{e.no2}: P={P:.4f} W | Q={Q:.4f} VAR | S={S:.4f} VA")

    entrada, saida = detectar_entrada_saida(c)
    print(f"\n🔎 Entrada detectada: {entrada}")
    print(f"🔎 Saída detectada: {saida}")

    if entrada is not None and saida is not None:
        ganho = calcular_ganho(tensoes, entrada, saida)
        print(f"\n📈 Ganho Vout/Vin = {ganho}")
        print(f"📈 |Ganho| = {abs(ganho):.4f}")
        if abs(ganho) != 0:
            print(f"📈 Ganho em dB = {20*np.log10(abs(ganho)):.4f} dB")
        else:
            print("📈 Ganho em dB = -inf")
    else:
        print("\n⚠️ Não foi possível calcular o ganho automaticamente.")


# =========================
# 🚀 EXECUÇÃO
# =========================
if __name__ == "__main__":
    print("⚡ Simulador + Análise de Frequência + Leitura por Texto/Imagem")
    inicializar_openai()

    # opções: "manual", "texto", "imagem"
    modo = "manual"

    if modo == "manual":
        dados = [
            {"tipo": "V", "valor": 10, "no1": "A", "no2": "GND"},
            {"tipo": "R", "valor": 10, "no1": "A", "no2": "B"},
            {"tipo": "C", "valor": 100e-6, "no1": "B", "no2": "GND"}
        ]

    elif modo == "texto":
        descricao = """
        Uma fonte de tensão de 10 V entre A e GND,
        um resistor de 10 ohms entre A e B,
        e um capacitor de 100 uF entre B e GND.
        """
        dados = texto_para_circuito(descricao)

    elif modo == "imagem":
        caminho_imagem = "circuito.png"
        dados = imagem_para_circuito(caminho_imagem)

    else:
        raise ValueError("Modo inválido. Use: manual, texto ou imagem.")

    if dados is None:
        print("⚠️ Não foi possível obter os dados do circuito.")
        raise SystemExit

    print("\n📦 JSON do circuito:")
    print(json.dumps(dados, indent=2, ensure_ascii=False))

    c = montar_circuito(dados, f=60)
    tensoes = resolver_mna(c)

    mostrar_resultados(c, tensoes)
    desenhar(c)
    gerar_bode(c)