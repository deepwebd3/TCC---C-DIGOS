# ⚡ Circuito Solver + Métodos de Runge-Kutta

## 📌 Descrição

Este projeto investiga o fenômeno de eletrização de um automóvel em movimento causado pelo atrito com o solo, modelando o sistema como um circuito elétrico do tipo **Resistor-Capacitor (RC)**.

Durante o movimento, o veículo acumula carga elétrica e, ao parar, essa carga é dissipada pelos pneus. Caso a descarga não seja completa, pode ocorrer uma centelha capaz de inflamar combustível.

O problema é modelado por uma **Equação Diferencial Ordinária (EDO)** resolvida por métodos de **Runge-Kutta (RK1 a RK4)**.

---

## 🎯 Objetivos

- Modelar a descarga elétrica do veículo  
- Aplicar métodos de Runge-Kutta  
- Comparar solução numérica e analítica  
- Avaliar erro relativo  
- Determinar tempo seguro (U < 50 mJ)

---

## ⚙️ Modelo Matemático

dV/dt = -V / (R_eq * C)

V(t) = V0 * exp(-t / (R_eq * C))

U(t) = (1/2) * C * V(t)^2

---

## 🔬 Parâmetros

- V₀ = 30 kV  
- C = 500 pF  
- R = 100 GΩ  
- R_eq = R/4  
- U_fogo = 50 mJ  

---

## 🧪 Métodos

- Euler (RK1)  
- Heun (RK2)  
- RK3  
- RK4  

---

## 📊 Resultados

### Tensão
![Tensão](TCC_CODIGOS/GRAFICOS_PNG/grafico1.png)

### Comparação RK
![Comparação RK](TCC_CODIGOS/GRAFICOS_PNG/grafico2.png)

### Energia
![Energia](TCC_CODIGOS/GRAFICOS_PNG/grafico3.png)

### Tensão e Energia
![Tensão e Energia](TCC_CODIGOS/GRAFICOS_PNG/tensao_energia.png)

---

## 🎞️ Simulação do circuito RC

![Simulação RC](TCC_CODIGOS/GRAFICOS_PNG/simulacao_rc.gif)
---

## 🚀 Como executar

```bash
git clone https://github.com/deepwebd3/TCC---C-DIGOS.git
cd TCC---C-DIGOS
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python TCC_CODIGOS/EX3.py

🛠️ Tecnologias
Python
NumPy
Matplotlib
📚 Referências
Chapra & Canale — Numerical Methods for Engineers
Halliday & Resnick — Fundamentals of Physics
👨‍💻 Autor

deepw3b3D
https://github.com/deepwebd3

⚠️ Observação

Projeto acadêmico voltado ao estudo de métodos numéricos aplicados a sistemas físicos.
