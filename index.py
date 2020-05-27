#!/usr/bin/env python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from app import app
from layouts import main_layout, model_layout, descriptive_layout
import callbacks

# It's needed to define a layout before the routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Routing of the website
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

# Host 0.0.0.0 to make sure to webstie is accesible from outside
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')