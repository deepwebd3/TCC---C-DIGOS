import numpy as np
import matplotlib.pyplot as plt

# Definindo a fonte para Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12  # Tamanho padrão da fonte

# Definindo a EDO: dy/dx = f(x, y)
def f(x, y):
    return y - x**2 + 1  # Exemplo: dy/dx = y - x² + 1

# Solução analítica para comparação
def solucao_analitica(x):
    return (x + 1)**2 - 0.5 * np.exp(x)

# Parâmetros do método RK1 (Euler)
x0 = 0.0
y0 = 0.5
h = 0.5  # Tamanho do passo
x_final = 2.0

# Armazenando os pontos do método RK1
x_rk1 = [x0]
y_rk1 = [y0]

# Executando o método RK1 (Euler)
while x_rk1[-1] < x_final:
    x_novo = x_rk1[-1] + h
    y_novo = y_rk1[-1] + h * f(x_rk1[-1], y_rk1[-1])
    x_rk1.append(x_novo)
    y_rk1.append(y_novo)

# Gerando pontos para a solução analítica
x_analitico = np.linspace(x0, x_final, 100)
y_analitico = solucao_analitica(x_analitico)

# Criando o gráfico
plt.figure(figsize=(12, 7))

# 1. Solução analítica (referência)
plt.plot(x_analitico, y_analitico, 'b-', label='Solução Analítica', linewidth=2)

# 2. Aproximação RK1 (Euler)
plt.plot(x_rk1, y_rk1, 'ro--', label='Runge-Kutta de 1ª Ordem', linewidth=1, markersize=8)

# 3. Elementos explicativos do método RK1
for i in range(len(x_rk1) - 1):
    # Ponto atual
    plt.scatter(x_rk1[i], y_rk1[i], color='green', s=100, zorder=5)
    
    # Linha do passo h (avanço em x)
    plt.plot([x_rk1[i], x_rk1[i+1]], [y_rk1[i], y_rk1[i]], 'g--', linewidth=1)
    
    # Linha da inclinação (f(xₙ, yₙ))
    x_tang = np.linspace(x_rk1[i], x_rk1[i+1], 10)
    y_tang = y_rk1[i] + (x_tang - x_rk1[i]) * f(x_rk1[i], y_rk1[i])
    plt.plot(x_tang, y_tang, 'm:', linewidth=1.5, label='Inclinação em (xₙ,yₙ)' if i == 0 else "")
    
    # Linha vertical (ajuste em y)
    plt.plot([x_rk1[i+1], x_rk1[i+1]], [y_rk1[i], y_rk1[i+1]], 'r--', linewidth=1)

# Anotações explicativas (com fonte Times New Roman)
plt.annotate('Passo h',
             xy=(x_rk1[0] + h/2, y_rk1[0] - 0.1),
             xytext=(x_rk1[0] + h/2, y_rk1[0] - 0.4),
             ha='center',
             fontsize=20,
             fontfamily='Times New Roman')

plt.annotate('Inclinação f(xₙ,yₙ)',
             xy=(x_rk1[0] + h/4, y_rk1[0] + 0.1),
             xytext=(x_rk1[0] - 0.5, y_rk1[0] + 0.5),
             arrowprops=dict(arrowstyle='->'),
             fontsize=20,
             fontfamily='Times New Roman')

plt.annotate('Aproximação RK1',
             xy=(x_rk1[1], y_rk1[1]),
             xytext=(x_rk1[1] + 0.2, y_rk1[1] - 0.3),
             arrowprops=dict(arrowstyle='->'),
             bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
             fontsize=20,
             fontfamily='Times New Roman')

# Configurações do gráfico (com fonte Times New Roman)
plt.title('', 
          fontsize=30, pad=25, fontfamily='Times New Roman')
plt.xlabel('x', fontsize=12, fontfamily='Times New Roman')
plt.ylabel('y', fontsize=12, fontfamily='Times New Roman')

# Ajustando SOMENTE o tamanho das legendas (sem alterar mais nada)
plt.legend(
    loc='upper left',
    prop={'family': 'Times New Roman', 'size': 20}  # Aumentando para 14
)

plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()