import numpy as np
import matplotlib.pyplot as plt


def runge_kutta_3rd_order(f, t0, y0, h, n_steps):
    """
    Implementação do método de Runge-Kutta de 3ª ordem
    """
    t_values = [t0]
    y_values = [y0]
    
    t = t0
    y = y0
    
    for i in range(n_steps):
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h, y - k1 + 2*k2)
        
        y = y + (k1 + 4*k2 + k3) / 6
        t = t + h
        
        t_values.append(t)
        y_values.append(y)
    
    return np.array(t_values), np.array(y_values)

def plot_runge_kutta_3rd_detailed():
    """
    Gráfico detalhado do método de Runge-Kutta de 3ª ordem
    """
    # Definir a EDO: y' = y - t^2 + 1
    def f(t, y):
        return y - t**2 + 1
    
    # Condição inicial
    t0, y0 = 0, 0.5
    h = 0.5  # tamanho do passo
    n_steps = 4
    
    # Solução exata para comparação
    def exact_solution(t):
        return (t + 1)**2 - 0.5 * np.exp(t)
    
    # Calcular solução numérica
    t_rk3, y_rk3 = runge_kutta_3rd_order(f, t0, y0, h, n_steps)
    
    # Calcular solução exata para plotagem suave
    t_exact = np.linspace(0, t_rk3[-1], 100)
    y_exact = exact_solution(t_exact)
    
    # Criar figura com subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Solução completa
    ax1.plot(t_exact, y_exact, 'b-', linewidth=2, label='Solução Exata', alpha=0.7)
    ax1.plot(t_rk3, y_rk3, 'ro-', linewidth=2, markersize=8, label='Runge-Kutta 3ª Ordem')
    ax1.set_xlabel('t')
    ax1.set_ylabel('y(t)')
    ax1.set_title('Método de Runge-Kutta de 3ª Ordem\nSolução Completa')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Ilustração detalhada do primeiro passo
    ax2.plot(t_exact, y_exact, 'b-', linewidth=2, label='Solução Exata', alpha=0.7)
    ax2.plot(t_rk3[:2], y_rk3[:2], 'ro-', linewidth=2, markersize=8, label='RK3')
    
    # Calcular e plotar os estágios do RK3 para o primeiro passo
    t1, y1 = t0, y0
    
    # Estágio 1: k1
    k1 = h * f(t1, y1)
    ax2.arrow(t1, y1, 0, k1/2, head_width=0.02, head_length=0.05, 
              fc='green', ec='green', linestyle='--', alpha=0.7, label='k1')
    
    # Estágio 2: k2
    k2 = h * f(t1 + h/2, y1 + k1/2)
    ax2.plot([t1, t1 + h/2], [y1, y1 + k1/2], 'g--', alpha=0.5)
    ax2.arrow(t1 + h/2, y1 + k1/2, 0, k2/2, head_width=0.02, head_length=0.05, 
              fc='orange', ec='orange', linestyle='--', alpha=0.7, label='k2')
    
    # Estágio 3: k3
    k3 = h * f(t1 + h, y1 - k1 + 2*k2)
    ax2.plot([t1 + h/2, t1 + h], [y1 + k1/2, y1 - k1 + 2*k2], 'orange', linestyle='--', alpha=0.5)
    ax2.arrow(t1 + h, y1 - k1 + 2*k2, 0, k3, head_width=0.02, head_length=0.05, 
              fc='red', ec='red', linestyle='--', alpha=0.7, label='k3')
    
    # Ponto final do passo
    y_next = y1 + (k1 + 4*k2 + k3) / 6
    ax2.plot(t1 + h, y_next, 'ro', markersize=8)
    
    ax2.set_xlabel('t')
    ax2.set_ylabel('y(t)')
    ax2.set_title('Detalhe do Primeiro Passo - Estágios do RK3')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Imprimir informações numéricas
    print("Método de Runge-Kutta de 3ª Ordem")
    print("=" * 50)
    print(f"EDO: y' = y - t² + 1")
    print(f"Condição inicial: y({t0}) = {y0}")
    print(f"Tamanho do passo: h = {h}")
    print("\nResultados:")
    print("t\t\tRK3\t\tExato\t\tErro")
    print("-" * 50)
    for i, (t, y_rk) in enumerate(t_rk3):
        y_ex = exact_solution(t)
        erro = abs(y_ex - y_rk)
        print(f"{t:.1f}\t\t{y_rk:.6f}\t{y_ex:.6f}\t{erro:.6f}")

def plot_comparison_errors():
    """
    Comparação de erros para diferentes tamanhos de passo
    """
    def f(t, y):
        return y - t**2 + 1
    
    def exact_solution(t):
        return (t + 1)**2 - 0.5 * np.exp(t)
    
    t0, y0 = 0, 0.5
    t_final = 2.0
    
    # Diferentes tamanhos de passo
    h_values = [0.5, 0.25, 0.125, 0.0625]
    colors = ['red', 'blue', 'green', 'orange']
    
    plt.figure(figsize=(12, 8))
    
    # Plot da solução exata
    t_exact = np.linspace(0, t_final, 100)
    y_exact = exact_solution(t_exact)
    plt.plot(t_exact, y_exact, 'k-', linewidth=3, label='Solução Exata', alpha=0.8)
    
    # Plot das soluções numéricas
    for h, color in zip(h_values, colors):
        n_steps = int((t_final - t0) / h)
        t_rk3, y_rk3 = runge_kutta_3rd_order(f, t0, y0, h, n_steps)
        plt.plot(t_rk3, y_rk3, 'o-', color=color, linewidth=2, 
                markersize=6, label=f'RK3 (h={h})')
    
    plt.xlabel('t')
    plt.ylabel('y(t)')
    plt.title('Comparação do Método de Runge-Kutta de 3ª Ordem\npara Diferentes Tamanhos de Passo')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

# Executar as visualizações
if __name__ == "__main__":
    plot_runge_kutta_3rd_detailed()
    plot_comparison_errors()