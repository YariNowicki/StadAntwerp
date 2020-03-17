import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import os
import DataReceiver
import snowflake.connector
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State
columns = ['postcode', 'jaar', 'aantal_loontrekkenden','aantal_werkzoekende','aantal_zelfstandigen',
        'inactieven','werkloosheidsdruk','belastingplichtigen','gemiddeld_netto_belastbaar_inkomen_per_persoon',
        'opbrengst_aanvullende_personenbelasting_per_belast','totaal_netto_inkomen','aantal_inwoners','dichtheid',
        'bibliotheek_bezocht','boek_gelezen','museum_bezocht','park_bezocht','restaurant_of_cafe_bezocht','televisie_gekeken',
        'voorstelling_bezocht','sport_beoefend','regelmatig_de_fiets_naar_werk_school',
        'regelmatig_te_voet_naar_werk_school','al_aso','al_bso','al_kso','al_tso','al_deel_bso','al_basis_binnen_a',
        'al_basis_buiten_a','al_buso','al_so_geen_vertraging', 'al_so_vertraging','al_so_meer_vertraging','al_a_stroom',
        'al_b_stroom','al_so_binnen_a','al_so_buiten_a','aantal_koten','kotdichtheid','plaatsen_buurtparkings','buurtparkings',
        'fietsenstallingen','plaatsen_fietsenstallingen','sportterreinen','speelterreinen','opp_sportterreinen','opp_gebruiksgroen_en_pleinen',
        'opp_speelterreinen','plaatsen_velo_stations','velo_stations']
mapbox_token = "pk.eyJ1IjoieWFyaW5vd2lja2kiLCJhIjoiY2s3dTk4ZDV6MDE0dDNvbW93NXBjNTZ5bSJ9.6tGy4sJsG0DOBXsEiXmPEA"
px.set_mapbox_access_token(mapbox_token)

def create_choropleth_mapbox(df, d):
    fig = px.choropleth_mapbox(data_frame=df, geojson=d, color='fiets_naar_werk_school', zoom=9,
                        locations="id", featureidkey='properties.postcode',center={"lat":51.3, "lon": 4.4})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

print("Getting data from snowflake...")
snow = DataReceiver.DataReceiver()
df, d = snow.get_geo_data()
input_data = snow.get_input_data()
print(len(input_data))
input_data = input_data[input_data['jaar'] == 2015]
print(len(input_data))
input_data = input_data[input_data['postcode'] == '2000']
print(len(input_data))
input_data = input_data[snow.COLS_INPUTS]
print(len(input_data))
print("Succeeded")
print(input_data)
display_fig = go.Figure(create_choropleth_mapbox(df, d))
for c in snow.COLS_INPUTS:
    print(input_data[c].values[0])

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Demo Antwerpen'),
    dcc.Dropdown(id='add-input',
    options=[
        {'label': '2018', 'value': 2018},
        {'label': '2017', 'value': 2017},
        {'label': '2016', 'value': 2016}
    ],value=2018),
    html.Div(id='inputs', children=[],
             style={
                 'float': 'left',
                 'width': '30%',
                 'height': '500px',
                 'overflow-y': 'scroll',
                 'margin': '10px'
            }
    ),

    html.Div(
        dcc.Graph(id='districten',figure=display_fig, style={
            'width': '30%',
            'float': 'right'
        })
    )

])


def create_todo_item(todo_text, todo_number):
    return html.Div(
        id='input-container-{}'.format(todo_number),
        children=[
            html.Span(todo_text),
            dcc.Slider(
                id='slider-{}'.format(todo_number),
                min=0,
                max=1.1,
                step=0.01,
                value=input_data[todo_text].values[0],
            )
        ]
    )

@app.callback(Output('inputs', 'children'),
              [Input('add-input', 'value')],
              [State('add-input', 'value'),
               State('inputs', 'children')])
def append_todo(n_enter_timestamp, todo_text, existing_todos):
    for c in snow.COLS_INPUTS:
        existing_todos.append(create_todo_item(
            c, len(existing_todos)
        ))
    return existing_todos


'''
@app.callback(Output('districten', 'figure'))
def create_graph():
    fig = px.choropleth_mapbox(data_frame=df, geojson=d,
                               locations="id", featureidkey='properties.postcode', center={"lat": 51.2, "lon": 4.4}
                               )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    display_fig = go.Figure(fig)
    return display_fig
'''

if __name__ == '__main__':
    app.run_server(debug=True)