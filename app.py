import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Output, Input
import urllib.request



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

mapbox_token = "pk.eyJ1IjoieWFyaW5vd2lja2kiLCJhIjoiY2s3dTk4ZDV6MDE0dDNvbW93NXBjNTZ5bSJ9.6tGy4sJsG0DOBXsEiXmPEA"
px.set_mapbox_access_token(mapbox_token)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('geodata/postzone.csv')

with open('D://Github//StadAntwerp//geodata//postzone.json') as json_file:
    data = json.load(json_file)

fig = px.choropleth_mapbox(data_frame=df, geojson=data, color='naam',
                    locations="id", featureidkey='properties.naam',center={"lat":51.2, "lon": 4.4}
                    )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
display_fig = go.Figure(fig)

app.layout = html.Div(children=[
    html.H1(children='Demo Antwerpen'),

    html.Div(children='''
        First test
    '''),
    html.Div(
        dcc.Graph(id='r',figure=display_fig)
    )


    # fig.show()
])

'''
@app.callback(Output('districten', 'figure'))
def create_graph():
    df = pd.read_csv('geodata/postzone.csv')
    with open('D://Github//StadAntwerp//geodata//postzone.json') as json_file:
        data = json.load(json_file)
    fig = px.choropleth(data_frame=df, geojson=data,
                        locations="naam", featureidkey="properties.postcode",
                        projection="mercator"
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, mapbox=mapbox_token)
    display_fig = go.Figure(fig)
    display_fig.show()
    return display_fig
'''

if __name__ == '__main__':
    app.run_server(debug=True)