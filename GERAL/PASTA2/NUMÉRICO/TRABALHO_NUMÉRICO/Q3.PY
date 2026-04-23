import numpy as np
import matplotlib.pyplot as plt

# Função para calcular o polinômio interpolador usando Lagrange
def interpolL(x, T):
    Soma = 0
    for i in range(len(T)):
        produto = 1.0
        for j in range(len(T)):
            if j == i:
                continue
            produto *= (x - T[j][0]) / (T[i][0] - T[j][0])
        Soma += T[i][1] * produto
    return Soma

# Pontos de amostra T

T = [(10, 498), (25, 512), (40, 537), (60, 570), (85, 610), (110, 647), (140, 672), (170, 688)]
     

# Define o polinômio interpolador p(x)
p = lambda x: interpolL(x, T)

# Gera valores para o gráfico da função interpolada
x = np.linspace(0, 170, 500)
y = [p(val) for val in x]  # Avalia ponto a ponto

# Cria o gráfico
plt.figure(figsize=(10, 6))
plt.plot(x, y, color='#FF4500', linewidth=1.5, label="Interpolação de Lagrange")
plt.scatter(*zip(*T), color='blue', s=40, marker='o', label="Pontos Tabelados")
plt.title('Variação da Temperatura ao longo do Tempo')
plt.xlabel('Angulação do satélite em graus')
plt.ylabel('Altitude do satélite em KM')
plt.grid()
plt.legend()

# Exibe o valor interpolado em x= 50, 100 e 150

print(f"Valor interpolado em x=: Altitude em do satelide em KM para o seguintes angulos 50 é de: {p(50):.3f} ")
print(f"Valor interpolado em x=: Altitude do satelide em KM para o seguintes angulos 100 é de: {p(100):.3f} ")
print(f"Valor interpolado em x=: Altitude do satelide em KM para o seguintes angulos 150 é de: {p(150):.3f} ")

# Mostra o gráfico
plt.show()