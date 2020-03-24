import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from df_calls import DataCalls
from snow_calls import SnowFlakeCalls
import callbacks

dc = DataCalls()
snow = SnowFlakeCalls()
fig = callbacks.initialize_map()

border_style = {'padding': '2px','border': '1px solid'}
input_div_style = {'float': 'left', 'width': '30%','height': '750px',
         'overflow-y': 'scroll',
         'margin': '10px'}
main = html.Div(children=[
    html.H1(id='title',
        children='Demo Antwerpen',
        style={
            'text-align': 'center',
            'font-size': '300%'}),
    html.Div(children=[
        html.Button('Predict', id='btn-predictie'),
        dcc.Dropdown(id='choose-postcode',
                     options=[{'label': i[1], 'value': i[0]} for i in snow.get_dropdown_list()],
                     value=2000),
        html.Div(children=[

            html.Div(children=[
                html.Div(id='inp-werk',children=[
                    html.P("loontrekkenden %"),
                    dcc.Slider(id='werk-slider-0',min=0,max=1,step=0.01),
                    html.P("Werkzoekenden %"),
                    dcc.Slider(id='werk-slider-1',min=0,max=1,step=0.01),
                    html.P("Zelfstandigen %"),
                    dcc.Slider(id='werk-slider-2',min=0,max=1,step=0.01),
                    html.P("Inactieven %"),
                    dcc.Slider(id='werk-slider-3',min=0,max=1,step=0.01)
                ], style=border_style),
                html.Div(id='inp-belastingen-plichtigen', children=[
                    html.P("Belastingplichtigen %"),
                    dcc.Slider(id='belast-slider-0',min=0,max=1,step=0.01),
                ], style=border_style),
                html.Div(id='inp-belasting',children=[
                    html.P("Gemiddeld netto belastbaar inkomen"),
                    dcc.Input(id='belast-input-0',type='number'),
                    html.P("Opbrengst personenbelasting per persoon"),
                    dcc.Input(id='belast-input-1',type='number')
                ], style=border_style),
                html.Div(id='inp-dichtheid', children=[
                    html.P("Dichtheid (km²)"),
                    dcc.Input(id='dichtheid-input-0',type='number')
                ], style=border_style),
                html.Div(id='inp-secundair', children=[
                    html.P("Leerlingen ASO %"),
                    dcc.Slider(id='secundair-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen BSO %"),
                    dcc.Slider(id='secundair-slider-1', min=0, max=1, step=0.01),
                    html.P("Leerlingen KSO %"),
                    dcc.Slider(id='secundair-slider-2', min=0, max=1, step=0.01),
                    html.P("Leerlingen TSO %"),
                    dcc.Slider(id='secundair-slider-3', min=0, max=1, step=0.01),
                    html.P("Leerlingen deeltijds BSO %"),
                    dcc.Slider(id='secundair-slider-4', min=0, max=1, step=0.01),
                    html.P("Leerlingen BUSO %"),
                    dcc.Slider(id='secundair-slider-5', min=0, max=1, step=0.01)
                ], style=border_style),
                html.Div(id='inp-vertraging', children=[
                    html.P("Leerlingen zonder vertraging %"),
                    dcc.Slider(id='vertraging-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen met 1 jaar vertraging %"),
                    dcc.Slider(id='vertraging-slider-1', min=0, max=1, step=0.01),
                    html.P("Leerlingen met meerdere jaren vertraging %"),
                    dcc.Slider(id='vertraging-slider-2', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-stroom', children=[
                    html.P("Leerlingen A-stroom %"),
                    dcc.Slider(id='stroom-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen B-stroom %"),
                    dcc.Slider(id='stroom-slider-1', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-basis-a', children=[
                    html.P("Leerlingen die naar een basisschool gaan binnen Antwerpen %"),
                    dcc.Slider(id='basis-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen die naar een basisschool gaan buiten Antwerpen %"),
                    dcc.Slider(id='basis-slider-1', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-so-a', children=[
                    html.P("Leerlingen die naar een secundaire school gaan buiten Antwerpen %"),
                    dcc.Slider(id='so-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen die naar een secundaire school gaan buiten Antwerpen %"),
                    dcc.Slider(id='so-slider-1', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-kot', children=[
                    html.P("Kotdichtheid %"),
                    dcc.Slider(id='kotdichtheid-input-0', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-enq', children=[
                    html.P("Bibliotheek bezocht %"),
                    dcc.Slider(id='enq-slider-0', min=0, max=100, step=0.01),
                    html.P("Boek gelezen %"),
                    dcc.Slider(id='enq-slider-1', min=0, max=100, step=0.01),
                    html.P("Museum bezocht %"),
                    dcc.Slider(id='enq-slider-2', min=0, max=100, step=0.01),
                    html.P("Park bezocht %"),
                    dcc.Slider(id='enq-slider-3', min=0, max=100, step=0.01),
                    html.P("Restaurant of café bezocht %"),
                    dcc.Slider(id='enq-slider-4', min=0, max=100, step=0.01),
                    html.P("Televisie gekeken %"),
                    dcc.Slider(id='enq-slider-5', min=0, max=100, step=0.01),
                    html.P("Voorstelling bezocht %"),
                    dcc.Slider(id='enq-slider-6', min=0, max=100, step=0.01),
                    html.P("Sport beoefend %"),
                    dcc.Slider(id='enq-slider-7', min=0, max=100, step=0.01)
                ], style=border_style),
                html.Div(id='inp-plaatsen', children=[
                    html.P("Plaatsen buurtparkings"),
                    dcc.Input(id='plaatsen-input-0',type='number'),
                    html.P("Plaatsen fietsenstallingen"),
                    dcc.Input(id='plaatsen-input-1',type='number'),
                    html.P("Plaatsen velostations"),
                    dcc.Input(id='plaatsen-input-2',type='number'),
                ], style=border_style),
                html.Div(id='inp-opp', children=[
                    html.P("Oppervlakte sportterreinen %"),
                    dcc.Slider(id='opp-slider-0', min=0, max=1, step=0.01),
                    html.P("Oppervlakte pleinen %"),
                    dcc.Slider(id='opp-slider-1', min=0, max=1, step=0.01),
                    html.P("Oppervlakte speelterreinen %"),
                    dcc.Slider(id='opp-slider-2', min=0, max=1, step=0.01)
                ], style=border_style)])]
            ,style={
                'height': '750px',
                'overflow-y': 'scroll',
                'margin': '1px'}),
    ],style=input_div_style),
    html.Div(
        dcc.Graph(id='predicties', figure=fig),
        style={'float': 'left'}
    ),

])