import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from df_calls import DataCalls
import callbacks

dc = DataCalls()
fig = callbacks.initialize_map()

border_style = {'padding': '2px','border': '1px solid'}

main = html.Div(children=[
    html.H1(id='title',
        children='Demo Antwerpen',
        style={
            'text-align': 'center',
            'font-size': '300%'}),
    html.Div(children=[
        dcc.Dropdown(id='choose-postcode',
                     options=[{'label': i[0], 'value': i[0]} for i in dc.get_dropdown_data()],
                     value=2000)
        ,
        html.Div(children=[
            html.Div(children=[
                html.Div(id='inp-werk',children=[], style=border_style),
                html.Div(id='inp-belastingen', children=[], style=border_style),
                html.Div(id='inp-belasting-plichtigen',children=[], style=border_style),
                html.Div(id='inp-dichtheid', children=[], style=border_style),
                html.Div(id='inp-secundair', children=[], style=border_style),
                html.Div(id='inp-vertraging', children=[], style=border_style),
                html.Div(id='inp-stroom', children=[], style=border_style),
                html.Div(id='inp-basis-a', children=[], style=border_style),
                html.Div(id='inp-so-a', children=[], style=border_style),
                html.Div(id='inp-kot', children=[], style=border_style),
                html.Div(id='inp-enq', children=[], style=border_style),
                html.Div(id='inp-plaatsen', children=[], style=border_style),
                html.Div(id='inp-opp', children=[], style=border_style)
                ])
            ],style={
                'height': '750px',
                'overflow-y': 'scroll',
                'margin': '1px'}),
    ],style={
         'float': 'left',
         'width': '30%',
         'height': '750px',
         'overflow-y': 'scroll',
         'margin': '10px'}),
    html.Div(
        dcc.Graph(id='predicties', figure=fig),
        style={'float': 'left'}
    ),

])