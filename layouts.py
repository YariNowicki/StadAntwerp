import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import src.DataReceiver as Dr
from src.Main import Main

m = Main()
snow = Dr.DataReceiver()
df, d = snow.get_geo_data()
px.set_mapbox_access_token(m.mapbox_token)

# Create map
display_fig = go.Figure(m.create_choropleth_mapbox(df, d))

main = html.Div(
    children=[
        html.H1(
            children='Demo Antwerpen',
            style={
                'text-align': 'center',
                'font-size': '300%'}),

        dcc.Dropdown(id='add-input',
            options=[
                {'label': '2018', 'value': 2018},
                {'label': '2017', 'value': 2017},
                {'label': '2016', 'value': 2016}],
            value=2018, style={ 'visibility': 'hidden'}),

        html.Hr(
            style={
                'display': 'block',
                'margin-bottom': '0.5em',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'border-style': 'inset',
                'border-width': '1px'}),

        html.Div(id='inputs',
                 children=[],
                 style={
                     'float': 'left',
                     'width': '30%',
                     'height': '750px',
                     'overflow-y': 'scroll',
                     'margin': '10px'}),

        html.Div(
            dcc.Graph(id='predicties'),
            style={'float': 'left'}
        ),

        html.Div(
            dcc.Graph(id='districten',
                      figure=display_fig,
                      style={
                        'width': '30%',
                        'float': 'right'})
        )

    ],
    style={'height': '100%'})