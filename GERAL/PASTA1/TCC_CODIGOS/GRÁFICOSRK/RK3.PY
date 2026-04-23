import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
def f(t, y):
    """Exemplo: dy/dt = -y + t (equação linear)"""
    return -y + t

# Solução analítica para dy/dt = -y + t, y(0) = 1
def solucao_analitica(t):
    return t - 1 + 2*np.exp(-t)

# Método de Runge-Kutta de 3ª ordem
def runge_kutta_3ordem(f, t0, y0, h, n_passos):
    t = np.zeros(n_passos + 1)
    y = np.zeros(n_passos + 1)
    t[0] = t0
    y[0] = y0
    
    # Armazenar pontos intermediários para visualização
    pontos_k1 = []
    pontos_k2 = []
    pontos_k3 = []
    
    for i in range(n_passos):
        # Estágios do RK3
        k1 = f(t[i], y[i])
        pontos_k1.append((t[i] + h/2, y[i] + (h/2)*k1))
        
        k2 = f(t[i] + h/2, y[i] + (h/2)*k1)
        pontos_k2.append((t[i] + h/2, y[i] + (h/2)*k2))
        
        k3 = f(t[i] + h, y[i] - h*k1 + 2*h*k2)
        pontos_k3.append((t[i] + h, y[i] + h*k3))
        
        # Atualização final
        y[i+1] = y[i] + (h/6) * (k1 + 4*k2 + k3)
        t[i+1] = t[i] + h
    
    return t, y, pontos_k1, pontos_k2, pontos_k3

# Parâmetros da simulação
t0 = 0
y0 = 1
h = 0.5  # Tamanho do passo (grande para visualização)
n_passos = 6
t_final = t0 + n_passos * h

# Executar método RK3
t_rk3, y_rk3, pontos_k1, pontos_k2, pontos_k3 = runge_kutta_3ordem(f, t0, y0, h, n_passos)

# Solução analítica para comparação
t_analitico = np.linspace(t0, t_final, 1000)
y_analitico = solucao_analitica(t_analitico)

# Método de Euler simples para comparação
def euler_simples(f, t0, y0, h, n_passos):
    t = np.zeros(n_passos + 1)
    y = np.zeros(n_passos + 1)
    t[0] = t0
    y[0] = y0
    
    for i in range(n_passos):
        y[i+1] = y[i] + h * f(t[i], y[i])
        t[i+1] = t[i] + h
    
    return t, y

t_euler, y_euler = euler_simples(f, t0, y0, h, n_passos)

# Criar figura
plt.figure(figsize=(12, 8))

# GRÁFICO PRINCIPAL: Visualização do Método RK3
# Solução analítica
plt.plot(t_analitico, y_analitico, 'b-', linewidth=2, label='Solução Analítica', alpha=0.8)

# Pontos do RK3
plt.plot(t_rk3, y_rk3, 'ro-', linewidth=1.5, markersize=8, 
         label='Runge-Kutta 3ª Ordem (Pontos Finais)')

# Euler simples para comparação
plt.plot(t_euler, y_euler, 'g--', linewidth=1.2, markersize=4, 
         label='Euler Simples')

# Adicionar setas e pontos intermediários do RK3
for i in range(n_passos):
    t_atual = t_rk3[i]
    y_atual = y_rk3[i]
    t_prox = t_rk3[i+1]
    
    # Pontos k1, k2, k3
    t_k1, y_k1 = pontos_k1[i]
    t_k2, y_k2 = pontos_k2[i]
    t_k3, y_k3 = pontos_k3[i]
    
    # Linha e ponto k1
    plt.plot([t_atual, t_k1], [y_atual, y_k1], 'orange', 
             linestyle=':', linewidth=1.5, alpha=0.7, 
             label='Estágio k1' if i == 0 else "")
    plt.plot(t_k1, y_k1, 's', color='orange', markersize=6, 
             label='Ponto k1' if i == 0 else "")
    
    # Linha e ponto k2
    plt.plot([t_k1, t_k2], [y_k1, y_k2], 'purple', 
             linestyle=':', linewidth=1.5, alpha=0.7,
             label='Estágio k2' if i == 0 else "")
    plt.plot(t_k2, y_k2, '^', color='purple', markersize=6, 
             label='Ponto k2' if i == 0 else "")
    
    # Linha e ponto k3
    plt.plot([t_k2, t_k3], [y_k2, y_k3], 'brown', 
             linestyle=':', linewidth=1.5, alpha=0.7,
             label='Estágio k3' if i == 0 else "")
    plt.plot(t_k3, y_k3, 'D', color='brown', markersize=5, 
             label='Ponto k3' if i == 0 else "")
    
    # Linha final (média ponderada)
    plt.plot([t_k3, t_prox], [y_k3, y_rk3[i+1]], 'red', 
             linestyle=':', linewidth=1.5, alpha=0.7,
             label='Correção Final' if i == 0 else "")
    
    # Setas explicativas
    plt.arrow(t_atual, y_atual, h/2, (h/2)*f(t_atual, y_atual), 
              head_width=0.02, head_length=0.02, fc='orange', ec='orange', alpha=0.6)
    
    plt.arrow(t_k1, y_k1, 0, y_k2 - y_k1, 
              head_width=0.015, head_length=0.015, fc='purple', ec='purple', alpha=0.6)
    
    plt.arrow(t_k2, y_k2, h/2, y_k3 - y_k2, 
              head_width=0.015, head_length=0.015, fc='brown', ec='brown', alpha=0.6)

plt.xlabel('t', fontsize=12)
plt.ylabel('y(t)', fontsize=12)
plt.title('Método de Runge-Kutta de 3ª Ordem - Visualização Detalhada', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.ylim(0.5, 1.8)

# Adicionar texto explicativo
plt.text(0.02, 0.98, 'RK3: $y_{n+1} = y_n + \\frac{h}{6}(k_1 + 4k_2 + k_3)$\n'
                     '$k_1 = f(t_n, y_n)$\n'
                     '$k_2 = f(t_n + h/2, y_n + hk_1/2)$\n'
                     '$k_3 = f(t_n + h, y_n - hk_1 + 2hk_2)$',
         transform=plt.gca().transAxes, fontsize=9, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.show()

# Cálculo do erro para comparação
erro_euler = np.abs(y_euler - solucao_analitica(t_euler))
erro_rk3 = np.abs(y_rk3 - solucao_analitica(t_rk3))

print("Comparação de Erros:")
print(f"Erro máximo Euler: {np.max(erro_euler):.6f}")
print(f"Erro máximo RK3: {np.max(erro_rk3):.6f}")