import numpy as np

# Parâmetros do problema
QG = 2.0
QL = 1.0
D = 0.8
cG0 = 100.0
cL6 = 10.0

# Número de reatores
n = 6

# Inicialização das concentrações (chute inicial)
cG = np.zeros(n)
cL = np.zeros(n)

# Critério de parada
tolerancia = 1e-6
max_iter = 1000

# Método de Jacobi
for iteracao in range(max_iter):
    cG_old = cG.copy()
    cL_old = cL.copy()
    
    # Reator 1
    cG[0] = (QG * cG0 + D * cL_old[0]) / (QG + D)
    cL[0] = (QL * cL_old[1] + D * cG_old[0]) / (QL + D)
    
    # Reatores 2 a 5
    for i in range(1, 5):
        cG[i] = (QG * cG_old[i-1] + D * cL_old[i]) / (QG + D)
        cL[i] = (QL * cL_old[i+1] + D * cG_old[i]) / (QL + D)
    
    # Reator 6
    cG[5] = (QG * cG_old[4] + D * cL6) / (QG + D)
    cL[5] = (D * cG_old[5]) / (QL + D)  # cL[6] é conhecido e QL*cL[7] não existe
    
    # Verificar convergência
    erro = max(np.max(np.abs(cG - cG_old)), np.max(np.abs(cL - cL_old)))
    if erro < tolerancia:
        print(f"Convergência alcançada após {iteracao+1} iterações.")
        break

# Resultados
print("\nConcentrações finais:")
for i in range(n):
    print(f"Reator {i+1}: cG = {cG[i]:.4f}, cL = {cL[i]:.4f}")