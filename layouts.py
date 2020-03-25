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
                    html.P("loontrekkenden %", id="werk-0"),
                    dcc.Slider(id='werk-slider-0',min=0,max=1,step=0.01),
                    html.P("Werkzoekenden %", id="werk-1"),
                    dcc.Slider(id='werk-slider-1',min=0,max=1,step=0.01),
                    html.P("Zelfstandigen %", id="werk-2"),
                    dcc.Slider(id='werk-slider-2',min=0,max=1,step=0.01),
                    html.P("Inactieven %", id="werk-3"),
                    dcc.Slider(id='werk-slider-3',min=0,max=1,step=0.01)
                ], style=border_style),
                html.Div(id='inp-belastingen-plichtigen', children=[
                    html.P("Belastingplichtigen %", id="belastplicht-0"),
                    dcc.Slider(id='belast-slider-0',min=0,max=1,step=0.01),
                ], style=border_style),
                html.Div(id='inp-belasting',children=[
                    html.P("Gemiddeld netto belastbaar inkomen", id="belast-0"),
                    dcc.Input(id='belast-input-0',type='number'),
                    html.P("Opbrengst personenbelasting per persoon", id="belast-1"),
                    dcc.Input(id='belast-input-1',type='number')
                ], style=border_style),
                html.Div(id='inp-dichtheid', children=[
                    html.P("Dichtheid (km²)",id="dichtheid-0"),
                    dcc.Input(id='dichtheid-input-0',type='number')
                ], style=border_style),
                html.Div(id='inp-secundair', children=[
                    html.P("Leerlingen ASO %", id="so-0"),
                    dcc.Slider(id='secundair-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen BSO %", id="so-1"),
                    dcc.Slider(id='secundair-slider-1', min=0, max=1, step=0.01),
                    html.P("Leerlingen KSO %", id="so-2"),
                    dcc.Slider(id='secundair-slider-2', min=0, max=1, step=0.01),
                    html.P("Leerlingen TSO %", id="so-3"),
                    dcc.Slider(id='secundair-slider-3', min=0, max=1, step=0.01),
                    html.P("Leerlingen deeltijds BSO %", id="so-4"),
                    dcc.Slider(id='secundair-slider-4', min=0, max=1, step=0.01),
                    html.P("Leerlingen BUSO %", id="so-5"),
                    dcc.Slider(id='secundair-slider-5', min=0, max=1, step=0.01)
                ], style=border_style),
                html.Div(id='inp-vertraging', children=[
                    html.P("Leerlingen zonder vertraging %", id="vertraging-0"),
                    dcc.Slider(id='vertraging-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen met 1 jaar vertraging %", id="vertraging-1"),
                    dcc.Slider(id='vertraging-slider-1', min=0, max=1, step=0.01),
                    html.P("Leerlingen met meerdere jaren vertraging %", id="vertraging-2"),
                    dcc.Slider(id='vertraging-slider-2', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-stroom', children=[
                    html.P("Leerlingen A-stroom %", id="stroom-0"),
                    dcc.Slider(id='stroom-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen B-stroom %", id="stroom-1"),
                    dcc.Slider(id='stroom-slider-1', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-basis-a', children=[
                    html.P("Leerlingen die naar een basisschool gaan binnen Antwerpen %", id="basis-0"),
                    dcc.Slider(id='basis-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen die naar een basisschool gaan buiten Antwerpen %", id="basis-1"),
                    dcc.Slider(id='basis-slider-1', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-so-a', children=[
                    html.P("Leerlingen die naar een secundaire school gaan binnen Antwerpen %", id="so-a-0"),
                    dcc.Slider(id='so-slider-0', min=0, max=1, step=0.01),
                    html.P("Leerlingen die naar een secundaire school gaan buiten Antwerpen %", id="so-a-1"),
                    dcc.Slider(id='so-slider-1', min=0, max=1, step=0.01),
                ], style=border_style),
                html.Div(id='inp-kot', children=[
                    html.P("Kotdichtheid %", id="kot-0"),
                    dcc.Slider(id='kotdichtheid-input-0', min=0, max=100, step=0.01),
                ], style=border_style),
                html.Div(id='inp-enq', children=[
                    html.P("Bibliotheek bezocht %", id="enq-0"),
                    dcc.Slider(id='enq-slider-0', min=0, max=100, step=0.01),
                    html.P("Boek gelezen %", id="enq-1"),
                    dcc.Slider(id='enq-slider-1', min=0, max=100, step=0.01),
                    html.P("Museum bezocht %", id="enq-2"),
                    dcc.Slider(id='enq-slider-2', min=0, max=100, step=0.01),
                    html.P("Park bezocht %", id="enq-3"),
                    dcc.Slider(id='enq-slider-3', min=0, max=100, step=0.01),
                    html.P("Restaurant of café bezocht %", id="enq-4"),
                    dcc.Slider(id='enq-slider-4', min=0, max=100, step=0.01),
                    html.P("Televisie gekeken %", id="enq-5"),
                    dcc.Slider(id='enq-slider-5', min=0, max=100, step=0.01),
                    html.P("Voorstelling bezocht %", id="enq-6"),
                    dcc.Slider(id='enq-slider-6', min=0, max=100, step=0.01),
                    html.P("Sport beoefend %", id="enq-7"),
                    dcc.Slider(id='enq-slider-7', min=0, max=100, step=0.01)
                ], style=border_style),
                html.Div(id='inp-plaatsen', children=[
                    html.P("Plaatsen buurtparkings", id="plaatsen-0"),
                    dcc.Input(id='plaatsen-input-0',type='number'),
                    html.P("Plaatsen fietsenstallingen", id="plaatsen-1"),
                    dcc.Input(id='plaatsen-input-1',type='number'),
                    html.P("Plaatsen velostations", id="plaatsen-2"),
                    dcc.Input(id='plaatsen-input-2',type='number'),
                ], style=border_style),
                html.Div(id='inp-opp', children=[
                    html.P("Oppervlakte sportterreinen %", id="opp-0"),
                    dcc.Slider(id='opp-slider-0', min=0, max=1, step=0.01),
                    html.P("Oppervlakte pleinen %", id="opp-1"),
                    dcc.Slider(id='opp-slider-1', min=0, max=1, step=0.01),
                    html.P("Oppervlakte speelterreinen %", id="opp-2"),
                    dcc.Slider(id='opp-slider-2', min=0, max=1, step=0.01)
                ], style=border_style)])]),
    ],style=input_div_style),
    html.Div(
        dcc.Graph(id='predicties', figure=fig),
        style={'float': 'left'}
    ),
])