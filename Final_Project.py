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


#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Define all necessary variables
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        exp_data = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        unemp_data = recession_data.groupby(['Vehicle_Type', 'Year'])['Automobile_Sales'].mean().reset_index()

        # Create and display graphs for Recession Report Statistics
        fig1 = px.line(
            yearly_rec, 
            x='Year', 
            y='Automobile_Sales',
            title="<b>Automobile Sales Trend During Recession</b>",
            color_discrete_sequence=['#FF6B6B']
        )
        fig1.update_layout(
            hovermode='x unified',
            title_font=dict(size=20),
            xaxis_title="",
            yaxis_title="Sales Volume",
            height=400
        )
        fig1.update_traces(line_width=3, hovertemplate='%{y:,.0f} units')
        fig2 = px.bar(
            average_sales, 
            x='Vehicle_Type', 
            y='Automobile_Sales',
            title="<b>Average Sales by Vehicle Type</b>",
            color='Vehicle_Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig2.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Average Sales",
            height=400
        )
        fig2.update_traces(hovertemplate='%{y:,.0f} units')
        fig3 = px.pie(
            exp_data, 
            values='Advertising_Expenditure', 
            names='Vehicle_Type',
            title="<b>Marketing Budget Allocation</b>",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig3.update_layout(
            uniformtext_minsize=12,
            uniformtext_mode='hide',
            height=400
        )
        fig3.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='%{label}: $%{value:,.0f}'
        )
        fig4 = px.bar(
            unemp_data, 
            x='Year',         
            y='Automobile_Sales', 
            color='Vehicle_Type',
            title="<b>Unemployment Rate Effect on Automobile Sales</b>",
            color_discrete_sequence=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6'],
            labels={'Automobile_Sales': 'Sales Volume (units)', 'Year': 'Recession Period'},
            height=450
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Poppins", color='#2c3e50'),
            title={
                'text': "<b>Unemployment Rate Effect on Automobile Sales</b>",
                'y': 0.95,
                'x': 0.5,
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
            )
        )

        return [
            html.Div(children=[dcc.Graph(figure=fig1)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig2)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig3)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig4)], style=graph_style)
        ]

#Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots
    # Check for Yearly Statistics.                             
    elif selected_statistics == 'Yearly Statistics':
        if not selected_year:
            return html.Div("Please select a year to view Yearly Statistics.", style=graph_style)

        # Filter data for the selected year
        yearly_data = data[data['Year'] == selected_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Sales Over Time")
        fig1.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')

        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        fig2 = px.line(mas, x='Month', y='Automobile_Sales', title=f"Monthly Sales in {selected_year}")
        fig2.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')
     
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig3 = px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f"Avg Sales by Vehicle Type in {selected_year}")
        fig3.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig4 = px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title=f"Ad Expenditure by Vehicle in {selected_year}")
        fig4.update_layout(title={'x': 0.5}, paper_bgcolor='#ffffff')

#Returning the graphs for displaying Yearly data
        return [
            html.Div(dcc.Graph(figure=fig1)), 
            html.Div(dcc.Graph(figure=fig2)),
            html.Div(dcc.Graph(figure=fig3)),
            html.Div(dcc.Graph(figure=fig4))
        ]
    
    return html.Div("Select a report type from the dropdown", style=graph_style)

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
