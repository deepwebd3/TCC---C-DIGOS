import numpy as np
import pylab as plt

# ==========================
# Parâmetros do problema
# ==========================
C = 500e-12     # Capacitância: 500 pF -> F
V0 = 30e3       # Tensão inicial: 30 kV -> V
R_pneu = 100e9  # Resistência de cada pneu: 100 GΩ -> Ohm
U_fogo = 50e-3  # Energia crítica: 50 mJ -> J

# Resistência equivalente (4 pneus em paralelo)
R_eq = R_pneu / 4.0

# Função diferencial dV/dt = -V/(R_eq*C)
def f(V, t):
    return -V / (R_eq * C)

# ==========================
# Condições iniciais e tempo
# ==========================
a = 0.0
b = 10.0
Num = 100

# passo consistente com np.linspace (Num pontos => Num-1 intervalos)
h = (b - a) / (Num - 1)

# Inicialização de arrays
t_pontos = np.linspace(a, b, Num)
V_pontos = np.zeros(Num)
U_pontos = np.zeros(Num)
erro_relativo = np.zeros(Num)

# Condição inicial
V_pontos[0] = V0
U_pontos[0] = 0.5 * C * V0**2
tempo_critico = None
eps = np.finfo(float).eps  # para evitar divisão por zero

# Pré-cálculo analítico vetorizado (para comparação)
tau = R_eq * C  # constante de tempo
V_analitico_vet = V0 * np.exp(-t_pontos / tau)
U_analitico_vet = 0.5 * C * V_analitico_vet**2

# ==========================
# Método de Euler (1ª ordem)
# ==========================
for i in range(1, Num):
    # Atualiza pelo método de Euler explícito
    V_pontos[i] = V_pontos[i-1] + h * f(V_pontos[i-1], t_pontos[i-1])
    U_pontos[i] = 0.5 * C * V_pontos[i]**2

    # Solução analítica no mesmo instante (já pré-calculada, mas deixo aqui por clareza)
    V_analitico = V_analitico_vet[i]

    # Calcula o erro relativo de forma segura (evita dividir por zero)
    denom = max(abs(V_analitico), eps)
    erro_relativo[i] = abs(V_pontos[i] - V_analitico) / denom

    # Exibe a solução analítica a cada 1 segundo (uso np.isclose para robustez)
    if np.isclose(t_pontos[i] % 1.0, 0.0, atol=1e-9):
        print(f"t = {t_pontos[i]:>4.1f} s → V_analítico = {V_analitico:.8e} V")

    # Verifica energia crítica (energia decresce com o tempo; detecta primeiro instante <= U_fogo)
    if U_pontos[i] <= U_fogo and tempo_critico is None:
        tempo_critico = t_pontos[i]
        print(f"\nTempo crítico alcançado (numérico): t = {t_pontos[i]:.6f} s")
        print(f"Tensão numérica: V = {V_pontos[i]:.8e} V")
        print(f"Tensão analítica: V_analítico = {V_analitico:.8e} V")
        print(f"Energia numérica: U = {U_pontos[i]:.8e} J\n")
        break

# ==========================
# Cálculo analítico de referência (tempo crítico)
# U(t) = 0.5 C V0^2 * exp(-2 t / tau)  =>  t = - (tau/2) ln( U_fogo / (0.5 C V0^2) )
# ==========================
energia_inicial = 0.5 * C * V0**2

if U_fogo <= 0:
    raise ValueError("U_fogo deve ser positivo.")

if U_fogo > energia_inicial:
    # energia crítica maior que energia inicial: nunca será atingida ao decair
    t_critico_analitico = float('nan')
    print("Aviso: energia crítica é maior que a energia inicial; tempo crítico analítico não definido (NaN).")
else:
    t_critico_analitico = - (tau / 2.0) * np.log(U_fogo / energia_inicial)

# ==========================
# Resultados numéricos finais
# ==========================
if tempo_critico is not None:
    idx_max = i + 1  # inclui o ponto onde a condição foi satisfeita
else:
    idx_max = Num

V_final_num = V_pontos[idx_max - 1]
U_final_num = U_pontos[idx_max - 1]

V_final_analitico = V_analitico_vet[idx_max - 1]
U_final_analitico = U_analitico_vet[idx_max - 1]

# erro médio somente até idx_max (evita incluir zeros não calculados além do stop)
erro_medio = np.mean(erro_relativo[:idx_max])

# ==========================
# Impressão dos resultados
# ==========================
print("\n=== RESULTADOS ===")
print(f"Constante de tempo τ = {tau:.6e} s")
if not np.isnan(t_critico_analitico):
    print(f"Tempo crítico analítico: {t_critico_analitico:.6f} s")
else:
    print("Tempo crítico analítico: NaN (energia crítica > energia inicial)")

if tempo_critico is not None:
    print(f"Tempo crítico (Euler): {tempo_critico:.6f} s")
    if not np.isnan(t_critico_analitico):
        print(f"Diferença numérico - analítico: {abs(tempo_critico - t_critico_analitico):.8e} s")
else:
    print("A energia não atingiu o valor crítico no intervalo simulado.")

print(f"\nEnergia inicial: {energia_inicial:.6e} J")
print(f"Energia final (numérica): {U_final_num:.6e} J")
print(f"Energia final (analítica): {U_final_analitico:.6e} J")

print(f"\nTensão final (numérica): {V_final_num:.6e} V")
print(f"Tensão final (analítica): {V_final_analitico:.6e} V")
print(f"Tensão crítica (para 50 mJ): {np.sqrt(2 * U_fogo / C):.6e} V")

print(f"\nErro relativo médio = {erro_medio:.6e}")

# ==========================
# Gráficos
# ==========================
plt.figure(figsize=(15, 5))

# Tensão
plt.subplot(1, 3, 1)
plt.plot(t_pontos[:idx_max], V_pontos[:idx_max], linewidth=1.8, label='Euler (Numérico)')
plt.plot(t_pontos[:idx_max], V_analitico_vet[:idx_max], 'k--', linewidth=1.2, label='Analítico')
plt.axhline(y=np.sqrt(2 * U_fogo / C), linestyle=':', label='Tensão crítica')
plt.title('Tensão vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.legend()

# Energia
plt.subplot(1, 3, 2)
plt.plot(t_pontos[:idx_max], U_pontos[:idx_max], linewidth=1.8, label='Energia (Euler)')
plt.axhline(y=U_fogo, linestyle=':', label='Energia crítica (50 mJ)')
plt.title('Energia vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.grid(True)
plt.legend()

# Erro relativo
plt.subplot(1, 3, 3)
plt.plot(t_pontos[:idx_max], erro_relativo[:idx_max], linewidth=1.5)
plt.title('Erro Relativo vs Tempo (Euler)')
plt.xlabel('Tempo (s)')
plt.ylabel('Erro relativo')
plt.grid(True)

plt.tight_layout()
plt.show()