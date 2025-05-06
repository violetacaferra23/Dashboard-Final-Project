#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc

# Load the data using pandas
try:
    data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')
except Exception as e:
    print(f"Error loading data: {e}")
    data = pd.DataFrame()  # Create an empty DataFrame on error

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# General style for the plots
graph_style = {
    'backgroundColor': '#f5f7fa',
    'padding': '20px',
    'fontFamily': 'Poppins, sans-serif',
    'color': '#333'
}

# Custom theme for all plots
custom_theme = {
    'layout': {
        'plot_bgcolor': '#ffffff',
        'paper_bgcolor': '#ffffff',
        'font': {'family': 'Poppins, sans-serif', 'color': '#333333'},
        'margin': dict(l=20, r=20, t=40, b=20),
        'hoverlabel': {
            'bgcolor': 'white',
            'font_size': 12,
            'font_family': 'Poppins'
        }
    },
    'config': {
        'displayModeBar': False  # Oculta la barra de herramientas de Plotly
    }
}

# Create the layout of the app
app.layout =  dbc.Container([

    html.Div([
        html.H1("Automobile Market Intelligence Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '20px 0'}),
        html.P("Data-driven insights into automotive sales performance", 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '30px'})
    ], style={'background': '#f8f9fa', 'padding': '20px', 'borderRadius': '5px'}),

    #Include style for title
    #Add two dropdown menus
    dbc.Row([
        dbc.Col([
            html.Label("Select Statistics:"),
            dcc.Dropdown(
                id='dropdown-statistics',
                options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
                placeholder='Select a report type',
                style={'fontSize': '16px'}
            )
        ], width=6),
        
        dbc.Col([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id='select-year',
                options=[{'label': i, 'value': i} for i in year_list],
                placeholder='Select a year',
                style={'fontSize': '16px'}
            )
        ], width=6),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='output-container')
        ])
    ])
], fluid=True)

#Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_select_year_disabled(selected_statistics):
    if selected_statistics is None:
        return True  # Deshabilitar
    else:
        return False  # Habilitar

# Common settings for all charts
COMMON_LAYOUT = {
    'title': {'x': 0.5, 'font': {'size': 20}},
    'plot_bgcolor': '#ffffff',
    'paper_bgcolor': '#ffffff',
    'font': {'family': 'Poppins', 'color': '#2c3e50'},
    'hovermode': 'x unified'
}

# Callback
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Chart 1: Trend during recession 
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(
            yearly_rec, 
            x='Year', 
            y='Automobile_Sales',
            title="<b>Automobile Sales Trend During Recession</b>",
            color_discrete_sequence=['#FF6B6B']
        )
        fig1.update_layout(**COMMON_LAYOUT, height=400)
        fig1.update_traces(line_width=3, hovertemplate='%{y:,.0f} units')

        # Chart 2: Avg sales by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = px.bar(
            average_sales, 
            x='Vehicle_Type', 
            y='Automobile_Sales',
            title="<b>Average Sales by Vehicle Type</b>",
            color='Vehicle_Type',
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig2.update_layout(
            **COMMON_LAYOUT,
            showlegend=False,
            height=400,
            yaxis_title="Sales Volume (units)"
        )
        fig2.update_traces(
            hovertemplate='%{y:,.0f} units',
            texttemplate='%{y:,.0f}',
            textposition='outside',
            textfont_size=12
        )

        # Chart 3: 3D Pie Chart
        exp_data = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig3 = px.pie(
            exp_data,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title="<b>Advertising Expenditure by vehicle </b>",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig3.update_layout(**COMMON_LAYOUT, height=400)
        fig3.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='%{label}: $%{value:,.0f}',
            pull=[0, 0, 0, 0],  # Efecto 3D
            rotation=45,
            marker=dict(line=dict(color='#ffffff', width=1))
        )

        # Chart 4: Unemployment Rate Effect (Stacked Bars)
        unemp_data = recession_data.groupby(['Vehicle_Type', 'Year'])['Automobile_Sales'].mean().reset_index()
        fig4 = px.bar(
            unemp_data,
            x='Year',
            y='Automobile_Sales',
            color='Vehicle_Type',
            title="<b>Unemployment Rate Effect (Stacked)</b>",
            color_discrete_sequence=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'],  # Colores personalizados
            barmode='stack', 
            height=450
        )
        fig4.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(family="Poppins", color='#2c3e50'),
            title={
                'text': "<b>Unemployment Rate Effect (Stacked View)</b>",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            xaxis=dict(
                showline=True,
                linecolor='#bdc3c7',
                tickangle=45 
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#ecf0f1',
                showline=True,
                linecolor='#bdc3c7'
            ),
            legend=dict(
                title_text='Vehicle Type',
                orientation='h',
                yanchor='bottom',
                y=-0.5,  
                xanchor='center',
                x=0.5
            ),
            margin=dict(l=50, r=50, t=80, b=120),  # Ajuste clave para el espacio
            hovermode='x unified'
        )  

        # Add value labels for each segment
        fig4.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='inside',
            textfont_size=10,
            marker_line_width=0.5,
            marker_line_color='white'
        )
        return [html.Div(dcc.Graph(figure=fig), style=graph_style) for fig in [fig1, fig2, fig3, fig4]]

    elif selected_statistics == 'Yearly Statistics':
        if not selected_year:
            return html.Div("Please select a year", style=graph_style)
            
        yearly_data = data[data['Year'] == selected_year]
        
        # Chart 1: Yearly trend 
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(
            yas,
            x='Year',
            y='Automobile_Sales',
            title=f"<b>Automobile Sales Trend</b>",
            color_discrete_sequence=['#FF6B6B']
        )
        fig1.update_layout(**COMMON_LAYOUT, height=400)
        fig1.update_traces(line_width=3, hovertemplate='%{y:,.0f} units')

        # Chart 2: Monthly sales
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        fig2 = px.line(
            mas,
            x='Month',
            y='Automobile_Sales',
            title=f"<b>Monthly Sales ({selected_year})</b>",
            color_discrete_sequence=['#4ECDC4']
        )
        fig2.update_layout(**COMMON_LAYOUT, height=400)
        fig2.update_traces(line_width=3, hovertemplate='%{y:,.0f} units')

        # Chart 3: Average sales per vehicle
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig3 = px.bar(
            avr_vdata,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title=f"<b>Average Sales by Vehicle Type ({selected_year})</b>",
            color='Vehicle_Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig3.update_layout(**COMMON_LAYOUT, showlegend=False, height=400)
        fig3.update_traces(
            hovertemplate='%{y:,.0f} units',
            texttemplate='%{y:,.0f}',
            textposition='outside',
            textfont_size=12
        )

        # Chart 4: 3D Pie Chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig4 = px.pie(
            exp_data,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title=f"<b>Advertising Expenditure by Vehicle</b>",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig4.update_layout(**COMMON_LAYOUT, height=400)
        fig4.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='%{label}: $%{value:,.0f}',
            pull=[0.1, 0, 0, 0],
            rotation=45
        )

        return [html.Div(dcc.Graph(figure=fig), style=graph_style) for fig in [fig1, fig2, fig3, fig4]]  
    
    return html.Div("Select a report type from the dropdown", style=graph_style)

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
