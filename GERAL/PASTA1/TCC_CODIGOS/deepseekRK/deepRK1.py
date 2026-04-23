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

# Condições iniciais
a = 0                # Tempo inicial (t = 0)
b = 10               # Tempo final (10 segundos)
Num = 1000            # Aumentei o número de subdivisões para maior precisão
h = (b - a) / Num    # Tamanho do passo
V = V0               # Condição inicial (30 kV)
U = 0.5 * C * V**2   # Energia inicial

# Inicialização
t_pontos = np.arange(a, b, h)
V_pontos = []
U_pontos = []
tempo_critico = None

# Método de Runge-Kutta de 1ª ordem (Euler)
for i in t_pontos:
    V_pontos.append(V)
    U_pontos.append(U)
    
    # Verifica se a energia atingiu o valor crítico
    if U <= U_fogo and tempo_critico is None:
        tempo_critico = i
        print(f"Tempo crítico alcançado: t = {i:.4f} s")
        print(f"Energia final: U = {U:.6f} J")
        print(f"Tensão final: V = {V:.2f} V")
    
    # Cálculo do coeficiente RK1
    k1 = h * f(V, i)
    
    # Atualiza o valor da tensão
    V += k1
    
    # Atualiza o valor da energia
    U = 0.5 * C * V**2

# Plotagem
plt.figure(figsize=(12, 5))

# Gráfico da tensão
plt.subplot(1, 2, 1)
plt.plot(t_pontos, V_pontos, color='#FF4500', linewidth=1.5)
plt.axhline(y=np.sqrt(2*U_fogo/C), color='red', linestyle='--', label='Tensão crítica')
plt.title('Tensão vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.legend()

# Gráfico da energia
plt.subplot(1, 2, 2)
plt.plot(t_pontos, U_pontos, color='blue', linewidth=1.5)
plt.axhline(y=U_fogo, color='red', linestyle='--', label='Energia crítica (50 mJ)')
plt.title('Energia vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Resultado final
if tempo_critico is not None:
    print(f"\nRESULTADO: O tempo necessário para a energia cair abaixo de 50 mJ é {tempo_critico:.4f} segundos")
else:
    print("A energia não atingiu o valor crítico no intervalo de tempo simulado")