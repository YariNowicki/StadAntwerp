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
from dash.dependencies import Output, Input

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
print("Succeeded")

display_fig = go.Figure(create_choropleth_mapbox(df, d))


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Demo Antwerpen'),

    html.Div(
        dcc.Graph(id='districten',figure=display_fig, style={
            'width': '30%'
        })
    )
])

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