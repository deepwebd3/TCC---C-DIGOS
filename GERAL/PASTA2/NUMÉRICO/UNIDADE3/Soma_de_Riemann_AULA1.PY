import numpy as np

def f(x):
    return 1/(1 + x**2)  # Define a função f(x) = e^(x²)

# Entrada de dados
a = float(input('Digite o ponto inicial (a): '))
b = float(input('Digite o ponto final (b): '))
n = int(input('Digite a quantidade de divisões do intervalo (n): '))

if n <= 0 or b <= a:
    print("Erro: certifique-se de que b > a e n > 0.")
    exit()

# Calcula a largura de cada subintervalo
deltax = (b - a) / n
print(f"O valor de (Δx) é: {deltax:.6f}")

# Soma usando o método da esquerda
soma = 0
for i in range(n):
    x = a + deltax * i
    soma += f(x) * deltax

print(f"O Valor da Integral é: {soma:.6f}")
#Esse código calcula a integral definida de f(x) = 1/(1 + x²) no intervalo [a, b] usando a soma de Riemann com n subintervalos.