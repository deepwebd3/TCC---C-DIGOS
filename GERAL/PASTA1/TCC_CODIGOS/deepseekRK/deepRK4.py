import numpy as np
import pylab as plt

# Parâmetros do problema
V0 = 30e3  # Tensão inicial (30 kV)
C = 500e-12  # Capacitância (500 pF)
R_pneu = 100e9  # Resistência de cada pneu (100 GΩ)
U_fogo = 50e-3  # Energia crítica para ignição (50 mJ)

# Como os 4 pneus estão em paralelo, a resistência equivalente é R_pneu/4
R_eq = R_pneu / 4

# Função que define a equação diferencial: dV/dt = -V/(R*C)
def f(V, t):
    return -V / (R_eq * C)

# Tempo inicial e final da simulação
a = 0  # Tempo inicial
b = 20  # Tempo final (segundos)
Num = 1000  # Número de subdivisões
h = (b - a) / Num  # Tamanho do passo

# Condição inicial: tensão no tempo t=0
V = V0

# Inicialização dos vetores
t_pontos = np.arange(a, b, h)
V_pontos = []
U_pontos = []  # Energia armazenada
t_critico = None  # Tempo quando a energia cai abaixo do valor crítico

# Método de Runge-Kutta de 4ª ordem
for i, t in enumerate(t_pontos):
    V_pontos.append(V)
    
    # Calcula a energia armazenada U = (1/2)*C*V²
    U = 0.5 * C * V**2
    U_pontos.append(U)
    
    # Verifica se a energia caiu abaixo do valor crítico
    if U < U_fogo and t_critico is None:
        t_critico = t
        print(f"Tempo crítico encontrado: t = {t:.4f} s")
        print(f"Energia no tempo crítico: U = {U*1000:.4f} mJ")
        print(f"Tensão no tempo crítico: V = {V/1000:.4f} kV")
    
    # Cálculo dos coeficientes de Runge-Kutta
    k1 = h * f(V, t)
    k2 = h * f(V + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(V + 0.5 * k2, t + 0.5 * h)
    k4 = h * f(V + k3, t + h)

    # Atualiza o valor de V
    V += (k1 + 2 * k2 + 2 * k3 + k4) / 6

# Cria a figura com dois subplots
plt.figure(figsize=(12, 8))

# Subplot 1: Tensão vs Tempo
plt.subplot(2, 1, 1)
plt.plot(t_pontos, np.array(V_pontos)/1000, color='blue', linewidth=2, label='Tensão V(t)')
plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
plt.title('Descarga do Capacitor Carro-Piso')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (kV)')
plt.grid(True, alpha=0.3)
plt.legend()

# Subplot 2: Energia vs Tempo
plt.subplot(2, 1, 2)
plt.plot(t_pontos, np.array(U_pontos)*1000, color='red', linewidth=2, label='Energia U(t)')
plt.axhline(y=U_fogo*1000, color='green', linestyle='--', label=f'Energia crítica ({U_fogo*1000} mJ)')

# Marca o tempo crítico se foi encontrado
if t_critico is not None:
    plt.axvline(x=t_critico, color='orange', linestyle='--', 
                label=f'Tempo crítico: {t_critico:.4f} s')
    plt.plot(t_critico, U_fogo*1000, 'ro', markersize=8)

plt.xlabel('Tempo (s)')
plt.ylabel('Energia (mJ)')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

# Resultados finais
print("\n" + "="*50)
print("RESULTADOS DA SIMULAÇÃO")
print("="*50)
print(f"Tensão inicial: V0 = {V0/1000:.2f} kV")
print(f"Energia inicial: U0 = {0.5*C*V0**2*1000:.2f} mJ")
print(f"Energia crítica: U_fogo = {U_fogo*1000:.2f} mJ")
print(f"Constante de tempo: τ = R_eq*C = {R_eq*C:.4f} s")
print(f"Resistência equivalente: R_eq = R_pneu/4 = {R_eq/1e9:.2f} GΩ")

if t_critico is not None:
    print(f"Tempo para energia cair abaixo do valor crítico: {t_critico:.4f} s")
else:
    print("A energia não caiu abaixo do valor crítico no tempo simulado")
    print(f"Energia final: {U_pontos[-1]*1000:.4f} mJ")