# ⚡ESTUDO DA DINÂMICA DE DESCARGA DE CIRCUITOS RC POR MÉTODOS NUMÉRICOS

## 📌 Descrição

Este projeto investiga o fenômeno de eletrização de um automóvel em movimento causado pelo atrito com o solo, modelando o sistema como um circuito **elétrico do tipo Resistor-Capacitor (RC)**. Além disso, são analisados dois circuitos RC de forma independente: o EX2, que representa um processo de descarga, e o EX3, que descreve o carregamento do circuito.

Durante o movimento, o veículo acumula carga elétrica e, ao parar, essa carga é dissipada pelos pneus. Caso a descarga não ocorra completamente, pode surgir uma diferença de potencial capaz de gerar uma centelha e inflamar o combustível.

Os problemas são descritos por **Equações Diferenciais Ordinárias (EDOs)** de primeira ordem, cujas soluções são obtidas por meio de métodos **numéricos de Runge-Kutta (RK1 a RK4)**.

## 📌 Problema : carro-eletrizado

Umautomóvel de competição em movimento pode acumular carga elétrica devido
ao atrito, comportando-se como um capacitor. Ao desacelerar, essa carga é dissipada gradualmente
pelos pneus, que atuam como resistores, conforme Figura 2. Se o abastecimento ocorrer antes da
descarga completa, a diferença de potencial pode gerar uma centelha capaz de inflamar o combustí
vel, caso a energia ultrapasse Ufogo = 50 mJ. Considerando V0 = 30 kV, C = 500 pF e resistência
dos pneus R = 25×109 Ω,queremosdeterminarotemponecessárioparaque aenergia armazenada
no circuito fique abaixo do valor crítico.

---

## 🎯 Objetivos

- Modelar a descarga elétrica do veículo como circuito RC  
- Aplicar métodos de Runge-Kutta (RK1 a RK4)  
- Comparar soluções numéricas com a solução analítica  
- Avaliar o erro relativo dos métodos  
- Determinar o tempo seguro para evitar ignição (U < 50 mJ)

---

## ⚙️ Modelo Matemático

$$
\frac{dV}{dt} = -\frac{V}{R_{eq}C}
$$

$$
V(t) = V_0 e^{-t/(R_{eq}C)}
$$

$$
U(t) = \frac{1}{2} C V(t)^2
$$

---

## 🔬 Parâmetros de EX1 >>> carro-eletrizado

| Parâmetro | Valor |
|----------|------|
| Tensão inicial (V₀) | 30 kV |
| Capacitância (C) | 500 pF |
| Resistência dos pneus (R) | 100 GΩ |
| Resistência equivalente (R_eq) | R / 4 |
| Energia crítica (U_fogo) | 50 mJ |

---

## 🧪 Métodos Numéricos Utilizados

- Euler (RK1)  
- Heun (RK2)  
- Runge-Kutta de 3ª ordem (RK3)  
- Runge-Kutta de 4ª ordem (RK4)

---

## 📊 Gráficos

### 🔹 Comparação dos métodos de RK para o EX 1 - carro-eletrizado
![Tensão](TCC_CODIGOS/GRAFICOS_PNG/grafico1.png)

### 🔹 Comparação dos métodos de RK para o EX 2 - circuito RC descarregando
![Comparação RK](TCC_CODIGOS/GRAFICOS_PNG/grafico2.png)

### 🔹 Comparação dos métodos de RK para o EX 3 - circuito RC carregando
![Energia](TCC_CODIGOS/GRAFICOS_PNG/grafico3.png)

### 🔹 Relação de tensão e energia para o EX1 - carro-eletrizado
![Tensão e Energia](TCC_CODIGOS/GRAFICOS_PNG/tensao_energia.png)

---

## 🎞️ Simulação do Circuito RC

![Simulação RC](TCC_CODIGOS/GRAFICOS_PNG/simulacao_rc.gif)

---

## 🚀 Como executar

```bash
git clone https://github.com/deepwebd3/TCC---C-DIGOS.git
cd TCC---C-DIGOS

# Criar ambiente virtual
python -m venv .venv

# Ativar (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar simulação
python TCC_CODIGOS/EX3.py