import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# CONFIGURAÇÕES GERAIS DE FONTE E ESTILO
# ==============================================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 13  # Tamanho base aumentado
plt.rcParams['axes.titlesize'] = 15  # Título do gráfico
plt.rcParams['axes.labelsize'] = 14  # Rótulos dos eixos
plt.rcParams['xtick.labelsize'] = 12  # Rótulos do eixo x
plt.rcParams['ytick.labelsize'] = 12  # Rótulos do eixo y
plt.rcParams['legend.fontsize'] = 12  # Legenda
plt.rcParams['figure.titlesize'] = 15  # Título da figura

# ==============================================
# DEFINIÇÕES MATEMÁTICAS
# ==============================================
def f(x, y):
    return y - x**2 + 1

def solucao_analitica(x):
    return (x + 1)**2 - 0.5 * np.exp(x)

# ==============================================
# PARÂMETROS E CÁLCULOS
# ==============================================
x0, y0 = 0.0, 0.5
h = 0.5
x_final = 2.0

x_heun = [x0]
y_preditor = [y0]
y_heun = [y0]

while x_heun[-1] < x_final:
    # Etapa preditora (Euler)
    x_novo = x_heun[-1] + h
    y_pred = y_heun[-1] + h * f(x_heun[-1], y_heun[-1])
    
    x_heun.append(x_novo)
    y_preditor.append(y_pred)
    
    # Etapa corretora
    y_corr = y_heun[-1] + h/2 * (f(x_heun[-1], y_heun[-1]) + f(x_novo, y_pred))
    y_heun.append(y_corr)

# Preparação da solução analítica
x_analitico = np.linspace(x0, x_final, 200)
y_analitico = solucao_analitica(x_analitico)

# ==============================================
# CONFIGURAÇÃO DO GRÁFICO
# ==============================================
plt.figure(figsize=(7, 5))  # Tamanho ligeiramente aumentado

# 1. Solução analítica
plt.plot(x_analitico, y_analitico, 'b-', label='Solução Analítica', linewidth=2.0)

# 2. Método de Heun (preditor)
plt.plot(x_heun, y_preditor, 'ro--', label='Previsão de Heun (Euler)', 
         linewidth=1.5, markersize=6, markeredgewidth=1.2)

# 3. Elementos explicativos
for i in range(len(x_heun) - 1):
    # Ponto atual
    plt.scatter(x_heun[i], y_heun[i], color='green', s=80, zorder=5)
    
    # Linha do passo h
    plt.plot([x_heun[i], x_heun[i+1]], [y_heun[i], y_heun[i]], 'g--', linewidth=1.2)
    
    # Linha da inclinação
    x_tang = np.linspace(x_heun[i], x_heun[i+1], 10)
    y_tang = y_heun[i] + (x_tang - x_heun[i]) * f(x_heun[i], y_heun[i])
    plt.plot(x_tang, y_tang, 'm:', linewidth=1.5, 
             label='Inclinação em (xₙ,yₙ)' if i == 0 else "")
    
    # Linha vertical da previsão
    plt.plot([x_heun[i+1], x_heun[i+1]], [y_heun[i], y_preditor[i+1]], 
             'r--', linewidth=1.2)

# ==============================================
# ANOTAÇÕES E TEXTOS
# ==============================================
# Anotações com fontes aumentadas
plt.annotate('Previsão Euler (Preditor)',
             xy=(x_heun[1], y_preditor[1]),
             xytext=(x_heun[1]-0.3, y_preditor[1]+0.3),
             arrowprops=dict(arrowstyle='->', linewidth=1.2),
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.6),
             fontsize=12)

plt.annotate('Inclinação inicial\nf(x₀,y₀)',
             xy=(x_heun[0]+0.15, y_heun[0] + 0.15*f(x_heun[0], y_heun[0])),
             xytext=(x_heun[0]-0.5, y_heun[0]+0.5),
             arrowprops=dict(arrowstyle='->', linewidth=1.2),
             fontsize=12)

plt.annotate('Passo h',
             xy=(x_heun[0]+h/2, y_heun[0]-0.1),
             xytext=(x_heun[0]+h/2, y_heun[0]-0.4),
             arrowprops=dict(arrowstyle='->', linewidth=1.2),
             ha='center',
             fontsize=12)
# ==============================================
# FINALIZAÇÃO DO GRÁFICO
# ==============================================
plt.title('Método de Heun - Etapa Preditora', pad=15, fontsize=25)
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc='upper left', framealpha=0.9)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Salvar em alta resolução
plt.savefig('metodo_heun_preditor_cientifico.png', dpi=600, bbox_inches='tight')
plt.show()