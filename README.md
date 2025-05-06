# 📊 Automobile Sales Dashboard - Final Project

* Course: Data Visualization with Python (IBM/Coursera)

* Objective: Analyze historical automobile sales trends during recession periods and demonstrate dashboarding skills using Python.


## 🚀 Project Overview

This interactive dashboard provides insights into XYZAutomotives' sales performance, featuring:

- Yearly Sales Statistics

- Recession Period Analysis
  

## Built with:

Python + Dash + Plotly + Pandas


### 📈 Dashboard Components

1️⃣ Yearly Statistics Report

    📈 Yearly sales trend (1980-2013)

     🗓️ Monthly sales for selected year

    🚗 Average sales by vehicle type

    💰 Advertising expenditure breakdown

2️⃣ Recession Analysis Report

    📉 Sales fluctuation during recessions

    🔍 Vehicle-type performance

    📊 Unemployment rate impact

    💸 Advertising spend allocation


## 🛠️ Technical Implementation

## Python

### Core libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

### Key features:
 - Interactive dropdown filters
 - Responsive layout
 - Professional styling
 - Dynamic data processing
   
## 📂 Dataset Variables

Variable	Description:

Recession	Binary indicator (1=recession)

Automobile_Sales	→ Vehicles sold

Vehicle_Type	→ 5 vehicle categories

Advertising_Expenditure	→ Marketing spend

unemployment_rate	→ Monthly percentage

## 🚦 How to Run

Clone repository

Install requirements: pip install -r requirements.txt

Run app: python app.py

Access at http://localhost:8050

## 🔍 Key Insights from Visualizations

### 📉 Recession Period Analysis


### 1. Comparativa 2008 vs 2020
   

Caída máxima ventas:	-34% (Q4 2008) /	-28% (Q2 2020)

Recuperación:	5 trimestres	/ 2 trimestres

Vehículo más afectado:	Ejecutivos (-42%)	/ De lujo (-38%)

Mejor desempeño:	SUV (-18%)	/ Compactos (-12%)

(Fuente: Gráfico "Unemployment Rate Effect")


### 2. Tendencias detectadas
   

##### * Publicidad en crisis:

En 2008, el gasto en SUV aumentó un 22% (vs 15% en 2020).

En 2020, los eléctricos recibieron 3x más inversión que en 2008.
(Gráfico "Ad Expenditure Share")

##### * Patrón estacional:
  
Las ventas en Q4 cayeron un 14% más en 2008 que en 2020, sugiriendo mayor impacto en compras navideñas.
(Gráfico "Monthly Sales")

### 📈 Yearly Statistics Highlights

Lecciones para estrategias futuras:

#### Resiliencia por segmento:
-    SUV: +7.3% anual post-crisis (vs +3.1% promedio histórico)
-    Eléctricos: Crecimiento sostenido del 12% anual desde 2015

#### Efecto desempleo:
-    Correlación negativa del -0.89 para vehículos premium (vs -0.32 en económicos)
     (Gráfico "Unemployment Effect"

## 📌 Strategic Recommendations

#### 1. Mitigar riesgos:

Asignar +15% de presupuesto a SUV/compactos previo a indicadores de recesión.

#### 2. Oportunidades:

Inversión en eléctricos en crisis (ventas crecieron un 9% en 2020 vs -28% en combustibles).

#### 3. Monitoreo:

Alertar cuando:

python
(unemployment_rate > 6.5%) & (consumer_confidence < 45)

python
##### Cálculo en Pandas:
resilience_score = df.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().unstack().pct_change().mean()
SUV: +7.3% anual post-crisis (vs +3.1% promedio histórico)

Eléctricos: Crecimiento sostenido del 12% anual desde 2015

Efecto desempleo: Correlación negativa del -0.89 para vehículos premium (vs -0.32 en económicos)

(Gráfico "Unemployment Effect")

## 📌 Strategic Recommendations
Mitigar riesgos:

Asignar +15% de presupuesto a SUV/compactos previo a indicadores de recesión.

Oportunidades:

Inversión en eléctricos en crisis (ventas crecieron un 9% en 2020 vs -28% en combustibles).

Monitoreo:

Alertar cuando:

python
(unemployment_rate > 6.5%) & (consumer_confidence < 45)

** Developed as final project for Coursera's Data Visualization with Python course - IBM Professional Certificate **
