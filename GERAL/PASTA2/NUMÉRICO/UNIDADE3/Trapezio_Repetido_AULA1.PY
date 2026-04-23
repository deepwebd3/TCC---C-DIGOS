import numpy as np

def f(x):
    return (5*x + 1)/((x +1)*(x - 2))

a = float(input("Digite o intervalo inferior: "))

b = float(input("Digite o intervalo superior: "))

n = int(input("Digite o número de partições: "))

deltax = (b - a) / n

# Este código é o responsável pelo cálculo da regra do trapézio repetida
soma1 = 0
soma2 = 0
for i in range(0, n + 1):
    x = a + deltax * i
    if (i == 0 or i == n):
        soma1 = soma1 + f(x)
    else:
        soma2 = soma2 + 2 * f(x)

soma = (soma1 + soma2) * (deltax / 2)
print(f"O Valor da integral é: {soma:.6f}")