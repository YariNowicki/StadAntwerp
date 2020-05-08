#!/usr/bin/python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from app import app
from layouts import main_layout, model_layout, descriptive_layout
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return main_layout
    elif pathname == '/model':
        return model_layout
    elif pathname == '/descriptive':
        return descriptive_layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')