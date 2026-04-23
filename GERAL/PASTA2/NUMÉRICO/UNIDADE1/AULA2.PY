# Definido a Função

import numpy as np

def f(x):
  valor = np.exp(x)
  return valor

a = 0
b = 2
n = 1000000
deltax = (b-a)/n
integral = 0

for i in range(1,n+1):
  x = a + i*deltax
  integral = integral + f(x)*deltax

print("O valor da integral é: ", integral)
valor_exato = (np.exp(2)-1)

erro_percentual = (abs(valor_exato-integral)/integral)*100
print("erro_percentual é: ", erro_percentual)