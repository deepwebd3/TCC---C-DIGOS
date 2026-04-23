# Este código é o responsável pelo cálculo da regra de 1/3 de Simpson repetida

import numpy as np

# Define a função f(x) = 1 - e^(-2x)
def f(x):
    return np.exp(x)

# Entrada dos limites de integração e número de partições
a = float(input("Digite o intervalo inferior: "))
b = float(input("Digite o intervalo superior: "))
n = int(input("Digite o número de partições: "))

# Calcula o tamanho de cada subintervalo
deltax = (b - a) / n

# Inicializa as somas parciais
soma1 = 0  # Soma dos extremos f(a) e f(b)
soma2 = 0  # Soma dos termos com coeficiente 2 (índices pares, exceto extremos)
soma3 = 0  # Soma dos termos com coeficiente 4 (índices ímpares)

# Laço que percorre todos os pontos do intervalo
for i in range(0, n + 1, 1):
    x = a + deltax * i
    if (i == 0 or i == n):
        soma1 = soma1 + f(x)       # Extremos: coeficiente 1
    elif (i % 2 == 0):
        soma2 = soma2 + 2 * f(x)   # Índices pares (exceto extremos): coeficiente 2
    else:
        soma3 = soma3 + 4 * f(x)   # Índices ímpares: coeficiente 4

# Aplica a fórmula de Simpson 1/3:
# Integral ≈ (Δx / 3) * [f(x0) + 4*f(x1) + 2*f(x2) + 4*f(x3) + ... + f(xn)]
soma = (soma1 + soma2 + soma3) * (deltax / 3)

# Exibe o resultado
print(f"A aproximação da integral pelo método de Simpson 1/3 no intervalo [{a}, {b}] é: {soma:.6f}")