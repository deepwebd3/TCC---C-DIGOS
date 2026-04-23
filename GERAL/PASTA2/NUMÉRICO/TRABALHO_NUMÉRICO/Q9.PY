import numpy as np

# Dados fornecidos
tempo = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]) # em segundos
forca_N = np.array([0, 850, 1350, 1800, 2100, 2200, 2250, 1900, 1400, 800, 8])  # em newtons
velocidade = np.array([28.0, 25.2, 21.8, 18.4, 15.0, 12.1, 9.3, 6.9, 4.1, 1.6, 0.0])  # em m/s

# Calculando o produto F(t)*v(t) para cada ponto
potencia = forca_N * velocidade

# Método dos Trapézios para integração
def trapezoidal_integration(x, y):
    n = len(x)
    integral = 0.0
    for i in range(n-1):
        integral += (x[i+1] - x[i]) * (y[i] + y[i+1]) / 2
    return integral

# Método de Simpson para integração (requer número ímpar de pontos)
def simpson_integration(x, y):
    if len(x) % 2 == 0:
        raise ValueError("Número de pontos deve ser ímpar para a regra de Simpson")
    
    n = len(x)
    h = x[1] - x[0]  # assumindo espaçamento uniforme
    integral = y[0] + y[-1]
    
    for i in range(1, n-1):
        if i % 2 == 1:
            integral += 4 * y[i]
        else:
            integral += 2 * y[i]
    
    return integral * h / 3

# Calculando a energia dissipada com ambos os métodos
try:
    energia_trapezio = trapezoidal_integration(tempo, potencia)
    energia_simpson = simpson_integration(tempo, potencia)
    
    print(f"Energia dissipada calculada pela regra dos trapézios: {energia_trapezio:.2f} J")
    print(f"Energia dissipada calculada pela regra de Simpson: {energia_simpson:.2f} J")
    
    # Diferença percentual entre os métodos
    diferenca_percentual = 100 * abs(energia_trapezio - energia_simpson) / ((energia_trapezio + energia_simpson)/2)
    print(f"\nDiferença percentual entre os métodos: {diferenca_percentual:.2f}%")
    
except ValueError as e:
    print(f"Erro ao aplicar a regra de Simpson: {e}")
    print(f"Energia dissipada calculada pela regra dos trapézios: {trapezoidal_integration(tempo, potencia):.2f} J")

# Visualização dos dados
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

# Gráfico da força e velocidade
plt.subplot(1, 2, 1)
plt.plot(tempo, forca_N, 'r-', label='Força de Frenagem (N)')
plt.plot(tempo, velocidade, 'b-', label='Velocidade (m/s)')
plt.xlabel('Tempo (s)')
plt.ylabel('Força/Velocidade')
plt.title('Força de Frenagem e Velocidade vs Tempo')
plt.grid(True)
plt.legend()

# Gráfico da potência dissipada
plt.subplot(1, 2, 2)
plt.plot(tempo, potencia, 'g-', label='Potência Dissipada (W)')
plt.fill_between(tempo, potencia, alpha=0.2, color='green')
plt.xlabel('Tempo (s)')
plt.ylabel('Potência (W)')
plt.title('Potência Dissipada vs Tempo\n(Área = Energia Dissipada)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Considerações: 

# A regra dos trapézios é mais simples e rápida de implementar, mas pode ser menos precisa para funções não lineares;

# O método de Simpson geralmente fornece resultados mais precisos para funções suaves;

# A pequena diferença entre os métodos indica que os dados são bem comportados;

# A visualização ajuda a entender como a energia é dissipada ao longo do processo de frenagem.