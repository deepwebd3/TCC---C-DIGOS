import numpy as np
import pylab as plt

# --------------------------
# Parâmetros do problema
# --------------------------
C = 500e-12    # 500 pF -> F
V0 = 30e3      # 30 kV -> V
R_pneu = 100e9 # 100 GΩ -> Ohm
U_fogo = 50e-3 # 50 mJ -> J

# Resistência equivalente (4 pneus em paralelo)
R_eq = R_pneu / 4.0

# Função diferencial: dV/dt = -V / (R_eq * C)
def f(V, t):
    return -V / (R_eq * C)

# --------------------------
# Parâmetros da simulação
# --------------------------
a = 0.0
b = 10.0
Num = 1000

# passo consistente com Num pontos
h = (b - a) / (Num - 1)

# malha de tempo robusta
t_pontos = np.linspace(a, b, Num)

# inicializações
V = V0
U = 0.5 * C * V**2

V_pontos = []
U_pontos = []
erro_relativo = []

tempo_critico = None
eps = np.finfo(float).eps

# pré-cálculo analítico na mesma malha para comparação
tau = R_eq * C
V_analitico_vet = V0 * np.exp(-t_pontos / tau)
U_analitico_vet = 0.5 * C * V_analitico_vet**2
energia_inicial = 0.5 * C * V0**2

# --------------------------
# Método RK2 (ponto médio)
# --------------------------
for i, t in enumerate(t_pontos):
    # salva os valores atuais
    V_pontos.append(V)
    U_pontos.append(U)

    # solução analítica no instante t
    V_analitico = V_analitico_vet[i]

    # erro relativo seguro
    denom = max(abs(V_analitico), eps)
    erro = abs(V - V_analitico) / denom
    erro_relativo.append(erro)

    # registra tempo crítico (primeiro instante que U <= U_fogo)
    if (U <= U_fogo) and (tempo_critico is None):
        tempo_critico = t
        print(f"\nTempo crítico alcançado (numérico): t = {t:.6f} s")
        print(f"Tensão naquele instante (numérica): V = {V:.6e} V")
        print(f"Energia naquele instante (numérica): U = {U:.6e} J\n")
        # OBS: não faço 'break' — a simulação continua. Trocar se preferir parar aqui.

    # passo RK2 (ponto médio)
    k1 = f(V, t)
    k2 = f(V + 0.5 * h * k1, t + 0.5 * h)
    V = V + h * k2
    U = 0.5 * C * V**2

# --------------------------
# Resultados analíticos de referência
# --------------------------
if U_fogo <= 0:
    raise ValueError("U_fogo deve ser positivo.")

if U_fogo > energia_inicial:
    t_critico_analitico = float('nan')
    print("Aviso: energia crítica é maior que a energia inicial; tempo crítico analítico indefinido (NaN).")
else:
    t_critico_analitico = - (tau / 2.0) * np.log(U_fogo / energia_inicial)

# conversão para arrays para plot e operações
t_pontos = np.array(t_pontos)
V_pontos = np.array(V_pontos)
U_pontos = np.array(U_pontos)
erro_relativo = np.array(erro_relativo)

# valores finais
V_final_num = V_pontos[-1]
U_final_num = U_pontos[-1]
V_final_analitico = V_analitico_vet[-1]
U_final_analitico = U_analitico_vet[-1]

# erro médio (uso todo o intervalo simulado)
erro_medio = np.mean(erro_relativo)

# --------------------------
# Impressão dos resultados
# --------------------------
print("\n=== RESULTADOS ===")
print(f"Constante de tempo τ = {tau:.6e} s")
if not np.isnan(t_critico_analitico):
    print(f"Tempo crítico analítico: {t_critico_analitico:.6f} s")
else:
    print("Tempo crítico analítico: NaN (energia crítica > energia inicial)")

if tempo_critico is not None:
    print(f"Tempo crítico (RK2): {tempo_critico:.6f} s")
    if not np.isnan(t_critico_analitico):
        print(f"Diferença numérico - analítico: {abs(tempo_critico - t_critico_analitico):.6e} s")
else:
    print("A energia não atingiu o valor crítico no intervalo de tempo simulado")

print(f"\nEnergia inicial: {energia_inicial:.6e} J")
print(f"Energia final (numérica): {U_final_num:.6e} J")
print(f"Energia final (analítica): {U_final_analitico:.6e} J")

print(f"\nTensão final (numérica): {V_final_num:.6e} V")
print(f"Tensão final (analítica): {V_final_analitico:.6e} V")
print(f"Tensão crítica (para 50 mJ): {np.sqrt(2 * U_fogo / C):.6e} V")

print(f"\nErro relativo médio = {erro_medio:.6e}")

# --------------------------
# Plotagem
# --------------------------
plt.figure(figsize=(15, 5))

# Tensão
plt.subplot(1, 3, 1)
plt.plot(t_pontos, V_pontos, linewidth=2, label='RK2 (Numérico)')
plt.plot(t_pontos, V_analitico_vet, 'r--', linewidth=1, label='Analítico')
plt.axhline(y=np.sqrt(2 * U_fogo / C), linestyle=':', label='Tensão crítica')
plt.title('Tensão vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.legend()

# Energia
plt.subplot(1, 3, 2)
plt.plot(t_pontos, U_pontos, linewidth=2, label='RK2 (Numérico)')
plt.plot(t_pontos, U_analitico_vet, 'r--', linewidth=1, label='Analítico')
plt.axhline(y=U_fogo, linestyle=':', label='Energia crítica (50 mJ)')
plt.title('Energia vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.grid(True)
plt.legend()

# Erro relativo
plt.subplot(1, 3, 3)
plt.plot(t_pontos, erro_relativo, linewidth=1.5)
plt.title('Erro Relativo do Método RK2')
plt.xlabel('Tempo (s)')
plt.ylabel('Erro relativo')
plt.grid(True)

plt.tight_layout()
plt.show()