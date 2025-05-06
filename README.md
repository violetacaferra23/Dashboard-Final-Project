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
Automobile_Sales	Vehicles sold
Vehicle_Type	5 vehicle categories
Advertising_Expenditure	Marketing spend
unemployment_rate	Monthly percentage

## 🚦 How to Run

Clone repository

Install requirements: pip install -r requirements.txt

Run app: python app.py

Access at http://localhost:8050


## 🔍 Key Insights

SUV sales showed most resilience during recessions

Advertising spend shifted to economy vehicles in downturns

2008 recession had most severe impact on executive cars



Developed as final project for Coursera's Data Visualization with Python course - IBM Professional Certificate
