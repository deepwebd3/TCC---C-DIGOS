import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# PARÂMETROS FÍSICOS DO SISTEMA
# ==============================================
CONSTANTES_MOLA = {
    'k1': 10,  # N/m
    'k2': 30,  # N/m
    'k3': 30,  # N/m
    'k4': 10   # N/m
}

MASSAS = {
    'm1': 2,  # kg
    'm2': 2,  # kg
    'm3': 2,  # kg
    'm4': 2   # kg
}
# ==============================================
# CONDIÇÕES INICIAIS
# ==============================================
DESLOCAMENTOS_INICIAIS = {
    'x1': 0.05,  # m
    'x2': 0.04,  # m
    'x3': 0.03   # m
}
VELOCIDADES_INICIAIS = {
    'v1': 0,  # m/s
    'v2': 0,  # m/s
    'v3': 0   # m/s
}
# ==============================================
# PARÂMETROS DA SIMULAÇÃO
# ==============================================
TEMPO = {
    'inicio': 0,   # s
    'final': 10,   # s
    'passos': 1000
}
# ==============================================
# DEFINIÇÃO DO SISTEMA DE EDOs
# ==============================================
def equacoes_diferenciais(Y, t):
    """Define o sistema de equações diferenciais do problema."""
    x1, v1, x2, v2, x3, v3 = Y
    
    # Coeficientes calculados uma única vez
    k1_plus_k2 = (CONSTANTES_MOLA['k1'] + CONSTANTES_MOLA['k2'])/MASSAS['m1']
    k2_over_m = CONSTANTES_MOLA['k2']/MASSAS['m1']
    k2_plus_k3 = (CONSTANTES_MOLA['k2'] + CONSTANTES_MOLA['k3'])/MASSAS['m2']
    k3_over_m = CONSTANTES_MOLA['k3']/MASSAS['m2']
    k3_plus_k4 = (CONSTANTES_MOLA['k3'] + CONSTANTES_MOLA['k4'])/MASSAS['m3']
    
    dx1dt = v1
    dv1dt = -k1_plus_k2*x1 + k2_over_m*x2
    dx2dt = v2
    dv2dt = k2_over_m*x1 - k2_plus_k3*x2 + k3_over_m*x3
    dx3dt = v3
    dv3dt = k3_over_m*x2 - k3_plus_k4*x3
    
    return np.array([dx1dt, dv1dt, dx2dt, dv2dt, dx3dt, dv3dt])

# ==============================================
# IMPLEMENTAÇÃO DO MÉTODO DE RUNGE-KUTTA 4ª ORDEM
# ==============================================
def runge_kutta_4():
    """Implementa o método de Runge-Kutta de 4ª ordem."""
    # Preparação dos vetores
    h = (TEMPO['final'] - TEMPO['inicio']) / TEMPO['passos']
    t_pontos = np.linspace(TEMPO['inicio'], TEMPO['final'], TEMPO['passos'])
    Y_pontos = np.zeros((len(t_pontos), 6))
    
    # Condições iniciais
    Y0 = np.array([
        DESLOCAMENTOS_INICIAIS['x1'], VELOCIDADES_INICIAIS['v1'],
        DESLOCAMENTOS_INICIAIS['x2'], VELOCIDADES_INICIAIS['v2'],
        DESLOCAMENTOS_INICIAIS['x3'], VELOCIDADES_INICIAIS['v3']
    ])
    Y_pontos[0] = Y0
    
    # Iteração do método
    for i in range(1, len(t_pontos)):
        Y = Y_pontos[i-1]
        t = t_pontos[i-1]
        
        k1 = h * equacoes_diferenciais(Y, t)
        k2 = h * equacoes_diferenciais(Y + 0.5*k1, t + 0.5*h)
        k3 = h * equacoes_diferenciais(Y + 0.5*k2, t + 0.5*h)
        k4 = h * equacoes_diferenciais(Y + k3, t + h)
        
        Y_pontos[i] = Y + (k1 + 2*k2 + 2*k3 + k4)/6
    
    return t_pontos, Y_pontos

# ==============================================
# EXECUÇÃO E VISUALIZAÇÃO
# ==============================================
def main():
    # Executa a simulação
    t, Y = runge_kutta_4()
    
    # Extrai resultados
    x1, v1, x2, v2, x3, v3 = Y.T
    
    # Cálculo preciso das acelerações
    a1 = np.gradient(v1, t)
    a2 = np.gradient(v2, t)
    a3 = np.gradient(v3, t)
    
    # Resultados iniciais
    print("\nAcelerações iniciais calculadas:")
    print(f"Massa 1: {a1[0]:.4f} m/s²")
    print(f"Massa 2: {a2[0]:.4f} m/s²")
    print(f"Massa 3: {a3[0]:.4f} m/s²")
    
    # Visualização
    plt.figure(figsize=(14, 10))
    
    # Gráfico dos deslocamentos
    plt.subplot(3, 1, 1)
    plt.plot(t, x1, 'b-', linewidth=2, label='Massa 1')
    plt.plot(t, x2, 'r-', linewidth=2, label='Massa 2')
    plt.plot(t, x3, 'g-', linewidth=2, label='Massa 3')
    plt.title('Deslocamentos das Massas ao Longo do Tempo', fontsize=14)
    plt.xlabel('Tempo (s)', fontsize=12)
    plt.ylabel('Deslocamento (m)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    # Gráfico das velocidades
    plt.subplot(3, 1, 2)
    plt.plot(t, v1, 'b-', linewidth=2, label='Massa 1')
    plt.plot(t, v2, 'r-', linewidth=2, label='Massa 2')
    plt.plot(t, v3, 'g-', linewidth=2, label='Massa 3')
    plt.title('Velocidades das Massas ao Longo do Tempo', fontsize=14)
    plt.xlabel('Tempo (s)', fontsize=12)
    plt.ylabel('Velocidade (m/s)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    # Gráfico das acelerações
    plt.subplot(3, 1, 3)
    plt.plot(t, a1, 'b-', linewidth=2, label='Massa 1')
    plt.plot(t, a2, 'r-', linewidth=2, label='Massa 2')
    plt.plot(t, a3, 'g-', linewidth=2, label='Massa 3')
    plt.title('Acelerações das Massas ao Longo do Tempo', fontsize=14)
    plt.xlabel('Tempo (s)', fontsize=12)
    plt.ylabel('Aceleração (m/s²)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()