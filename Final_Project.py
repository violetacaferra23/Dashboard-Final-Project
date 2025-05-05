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
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': '...........', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': '.........'}
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

# Create the layout of the app
app.layout =  dbc.Container([

    #Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'fontSize': '30px',
            'marginTop': '20px', 
            'marginBottom': '30px'
        }
    ),

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
        
#Create and display graphs for Recession Report Statistics

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Sales During Recession")
        fig1.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Avg Sales by Vehicle Type During Recession")
        fig2.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig3 = px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title="Ad Expenditure Share During Recession")
        fig3.update_layout(title={'x': 0.5}, paper_bgcolor='#ffffff')

        unemp_data = recession_data.groupby(['Vehicle_Type', 'Year'])['Automobile_Sales'].mean().reset_index()
        fig4 = px.bar(unemp_data, x='Year', y='Automobile_Sales', color='Vehicle_Type', title="Unemployment Rate Effect")
        fig4.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')

        return [
            html.Div(children=[dcc.Graph(figure=fig1)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig2)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig3)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig4)], style=graph_style)
        ]

#Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots
    # Check for Yearly Statistics.                             
    elif selected_statistics == 'Yearly Statistics' and selected_year:
        yearly_data = data[data['Year'] == selected_year]

                              
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Sales Over Time")
        fig1.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')

        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        fig2 = px.line(mas, x='Month', y='Automobile_Sales', title="Monthly Sales Total")
        fig2.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig3 = px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f"Avg Sales by Vehicle Type in {selected_year}")
        fig3.update_layout(title={'x': 0.5}, plot_bgcolor='#f0f4f8', paper_bgcolor='#ffffff')

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig4 = px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title="Ad Expenditure by Vehicle")
        fig4.update_layout(title={'x': 0.5}, paper_bgcolor='#ffffff')

#Returning the graphs for displaying Yearly data
        return [
            html.Div(children=[dcc.Graph(figure=fig1)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig2)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig3)], style=graph_style),
            html.Div(children=[dcc.Graph(figure=fig4)], style=graph_style)
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)



