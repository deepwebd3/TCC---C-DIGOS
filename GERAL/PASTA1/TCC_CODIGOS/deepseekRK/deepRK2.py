import numpy as np
import pylab as plt

# Parâmetros do problema
C = 500e-12  # 500 pF em Farads
V0 = 30e3    # 30 kV em Volts
R_pneu = 100e9  # 100 GΩ em Ohms
U_fogo = 50e-3  # 50 mJ em Joules

# Resistência equivalente (4 pneus em paralelo)
R_eq = R_pneu / 4

# Função que define a equação diferencial para a tensão
def f(V, t):
    return -V / (R_eq * C)

# Parâmetros da simulação
a = 0                # Tempo inicial (t = 0)
b = 10               # Tempo final (10 segundos)
Num = 100             # Número de subdivisões para maior precisão
h = (b - a) / Num    # Tamanho do passo
V = V0               # Condição inicial (30 kV)
U = 0.5 * C * V**2   # Energia inicial

# Inicialização
t_pontos = np.arange(a, b, h)
V_pontos = []
U_pontos = []
tempo_critico = None

# Método de Runge-Kutta de 2ª ordem (Ponto Médio)
for i in t_pontos:
    V_pontos.append(V)
    U_pontos.append(U)
    
    # Verifica se a energia atingiu o valor crítico
    if U <= U_fogo and tempo_critico is None:
        tempo_critico = i
        print(f"Tempo crítico alcançado: t = {i:.6f} s")
        print(f"Energia final: U = {U:.8f} J")
        print(f"Tensão final: V = {V:.4f} V")
    
    # Cálculo dos coeficientes RK2
    k1 = h * f(V, i)
    k2 = h * f(V + 0.5 * k1, i + 0.5 * h)
    
    # Atualiza o valor da tensão
    V += k2
    
    # Atualiza o valor da energia
    U = 0.5 * C * V**2

# Cálculo da solução analítica para comparação
tau = R_eq * C  # Constante de tempo
t_analitico = np.linspace(a, b, 1000)
V_analitico = V0 * np.exp(-t_analitico/tau)
U_analitico = 0.5 * C * V_analitico**2

# Encontrar tempo crítico analítico
t_critico_analitico = (tau/2) * np.log(0.5 * C * V0**2 / U_fogo)

# Plotagem
plt.figure(figsize=(15, 5))

# Gráfico da tensão
plt.subplot(1, 3, 1)
plt.plot(t_pontos, V_pontos, color='#2E8B57', linewidth=2, label='RK2 (Numérico)')
plt.plot(t_analitico, V_analitico, 'r--', linewidth=1, label='Analítico')
plt.axhline(y=np.sqrt(2*U_fogo/C), color='red', linestyle=':', label='Tensão crítica')
plt.title('Tensão vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.legend()

# Gráfico da energia
plt.subplot(1, 3, 2)
plt.plot(t_pontos, U_pontos, color='blue', linewidth=2, label='RK2 (Numérico)')
plt.plot(t_analitico, U_analitico, 'r--', linewidth=1, label='Analítico')
plt.axhline(y=U_fogo, color='red', linestyle=':', label='Energia crítica (50 mJ)')
plt.title('Energia vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.grid(True)
plt.legend()

# Gráfico do erro
plt.subplot(1, 3, 3)
erro_V = np.abs(V_pontos - V0 * np.exp(-t_pontos/tau))
plt.semilogy(t_pontos, erro_V, color='purple', linewidth=1.5)
plt.title('Erro do Método RK2')
plt.xlabel('Tempo (s)')
plt.ylabel('Erro absoluto (V)')
plt.grid(True)

plt.tight_layout()
plt.show()

# Resultados finais
print(f"\n=== RESULTADOS ===")
print(f"Constante de tempo τ = {tau:.4f} s")
print(f"Tempo crítico analítico: {t_critico_analitico:.6f} s")
if tempo_critico is not None:
    print(f"Tempo crítico RK2: {tempo_critico:.6f} s")
    print(f"Diferença: {abs(tempo_critico - t_critico_analitico):.8f} s")
else:
    print("A energia não atingiu o valor crítico no intervalo de tempo simulado")

print(f"\nEnergia inicial: {0.5 * C * V0**2:.6f} J")
print(f"Energia crítica: {U_fogo:.6f} J")
print(f"Tensão crítica: {np.sqrt(2*U_fogo/C):.2f} V")