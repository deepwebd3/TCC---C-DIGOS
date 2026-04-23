import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
U_fogo = 50e-3  # 50 mJ (energia crítica)
V0 = 30e3       # 30 kV (tensão inicial)
C = 500e-12     # 500 pF (capacitância)
R_pneu = 100e9  # 100 GΩ (resistência por pneu)

# Resistência equivalente (4 pneus em paralelo)
R_eq = R_pneu / 4

# Equação diferencial: dV/dt = -V/(R_eq*C)
def f(V, t):
    return -V / (R_eq * C)

# Função para calcular a energia
def energia(V):
    return 0.5 * C * V**2

# Parâmetros da simulação
a = 0                # Tempo inicial
b = 20               # Tempo final em segundos (aumentado para garantir convergência)
Num = 10        # Número de subdivisões
h = (b - a) / Num    # Tamanho do passo
V = V0              # Condição inicial: tensão no tempo t=0

# Inicialização dos vetores
t_pontos = np.arange(a, b, h)
V_pontos = []
U_pontos = []
tempo_critico = None

# Método de Runge-Kutta de 3ª ordem
for i in t_pontos:
    V_pontos.append(V)
    U = energia(V)
    U_pontos.append(U)
    
    # Verifica se a energia caiu abaixo do valor crítico
    if U <= U_fogo and tempo_critico is None:
        tempo_critico = i
        print(f"Tempo para atingir U_fogo: {i:.6f} segundos")
    
    # Cálculo dos coeficientes RK3
    k1 = h * f(V, i)
    k2 = h * f(V + 0.5 * k1, i + 0.5 * h)
    k3 = h * f(V - k1 + 2 * k2, i + h)
    
    # Atualiza o valor de V
    V += (k1 + 4 * k2 + k3) / 6

# Solução analítica para comparação
t_analitico = -R_eq * C * np.log(np.sqrt(2 * U_fogo / (C * V0**2)))
print(f"Tempo analítico: {t_analitico:.6f} segundos")

# Cálculos adicionais
tau = R_eq * C  # Constante de tempo
energia_inicial = energia(V0)

print(f"\nParâmetros do sistema:")
print(f"Resistência equivalente: {R_eq/1e9:.2f} GΩ")
print(f"Constante de tempo τ = R_eq*C = {tau:.6f} segundos")
print(f"Energia inicial: {energia_inicial*1000:.2f} mJ")
print(f"Energia crítica: {U_fogo*1000:.2f} mJ")

# Plotagem dos resultados
plt.figure(figsize=(14, 6))

# Gráfico da tensão
plt.subplot(1, 2, 1)
plt.plot(t_pontos[:len(V_pontos)], np.array(V_pontos)/1000, 'b-', linewidth=2, label='Tensão V(t) (RK3)')
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
if tempo_critico:
    plt.axvline(x=tempo_critico, color='r', linestyle='--', alpha=0.7, label=f't = {tempo_critico:.2f} s')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (kV)')
plt.title('Descarga do Capacitor Carro-Piso (Método RK3)')
plt.grid(True)
plt.legend()

# Gráfico da energia
plt.subplot(1, 2, 2)
plt.plot(t_pontos[:len(U_pontos)], np.array(U_pontos)*1000, 'r-', linewidth=2, label='Energia U(t) (RK3)')
plt.axhline(y=U_fogo*1000, color='g', linestyle='--', linewidth=2, label='U_fogo = 50 mJ')
if tempo_critico:
    plt.axvline(x=tempo_critico, color='r', linestyle='--', alpha=0.7, label=f't = {tempo_critico:.2f} s')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (mJ)')
plt.title('Energia Armazenada no Sistema (Método RK3)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Verificação final
if tempo_critico:
    print(f"\n✅ O carro atinge segurança após {tempo_critico:.4f} segundos")
    print(f"   (Tempo necessário para energia < {U_fogo*1000} mJ)")
else:
    print(f"\n❌ O carro não atingiu segurança no tempo simulado de {b} segundos")