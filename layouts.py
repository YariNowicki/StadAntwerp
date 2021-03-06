from df_calls import DataCalls
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from snow_calls import SnowFlakeCalls
import callbacks

# Used to upgrade the graph (model page) that display some inputs values of the prediction
def update_point(trace, points, selector):
        c = list(scatter.marker.color)
        s = list(scatter.marker.size)
        print(trace)
        print(points)
        print(selector)
        for i in points.point_inds:
            c[i] = '#bae2be'
            s[i] = 20
            with f.batch_update():
                scatter.marker.color = c
                scatter.marker.size = s



dc = DataCalls()
snow = SnowFlakeCalls()

chart = dc.weight_chart()
df, d = snow.get_geo_data()
df_pred = df.copy()
df_pred = df_pred.reset_index()
df_pred = df_pred.drop(['index'], axis=1)
# Token to display the map Antwerpen (root page)
mapbox_token = "pk.eyJ1IjoieWFyaW5vd2lja2kiLCJhIjoiY2s3dTk4ZDV6MDE0dDNvbW93NXBjNTZ5bSJ9.6tGy4sJsG0DOBXsEiXmPEA"
px.set_mapbox_access_token(mapbox_token)

# Creates the map antwerpen (root page)
fig = callbacks.create_map(df_pred)

scatter = fig.data[0]
scatter.on_click(update_point)

# Create app layout
main_layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="./assets/datasense.png",
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Stad Antwerpen",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Fietsgebruik", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Model", id="model-button"),
                            href="/model",
                        ),
                        html.A(
                            html.Button("Descriptive", id="desc-button"),
                            href="/descriptive",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                
            ],
            className="row flex-display", style={'float':'right'}
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Button('Predict', id='btn-predictie'),
                        html.Br(),
                        dcc.Dropdown(id='choose-postcode',
                             options=[{'label': i[1], 'value': i[0]} for i in snow.get_dropdown_list()],
                             value=2000, clearable=False),
                        html.Br(),
                        html.Br(),
                        html.Button('Inwoners', id='btn-inwoners', style={'width': '100%'}),
                        html.Br(),
                        html.Div(id='inp-inwoners' ,children=[
                            html.P("Werkenden %", id="werk-0"),
                            dcc.Slider(id='werk-slider-0',min=0,max=100,step=0.01),
                            html.P("Belastingplichtigen %", id="belastplicht-0"),
                            dcc.Slider(id='belast-slider-0',min=0,max=100,step=0.01),
                            html.P("Gemiddeld netto belastbaar inkomen", id="belast-0"),
                            dcc.Input(id='belast-input-0',type='number'),
                            html.P("Dichtheid (km²)",id="dichtheid-0"),
                            dcc.Input(id='dichtheid-input-0',type='number')
                        ], style={'display': 'none'}),
                        html.Br(),
                        html.Br(),
                        html.Button('Onderwijs', id='btn-onderwijs', style={'width': '100%'}),
                        html.Br(),
                        html.Div(id='inp-onderwijs', children=[
                            html.P("Theoretisch geschoolde leerlingen %", id="so-0"),
                            dcc.Slider(id='secundair-slider-0', min=0, max=100, step=0.01),
                            html.P("Leerlingen zonder vertraging %", id="vertraging-0"),
                            dcc.Slider(id='vertraging-slider-0', min=0, max=100, step=0.01),
                            html.P("Leerlingen die naar een school gaan binnen Antwerpen %", id="school-0"),
                            dcc.Slider(id='school-slider-0', min=0, max=100, step=0.01)
                        ], style={'display': 'none'}),
                        html.Br(),
                        html.Br(),
                        html.Button('Enquête resultaten', id='btn-enq', style={'width': '100%'}),
                        html.Br(),
                        html.Div(id='inp-enq', children=[
                            html.P("Bibliotheek bezocht %", id="enq-0"),
                            dcc.Slider(id='enq-slider-0', min=0, max=100, step=0.01),
                            html.P("Boek gelezen %", id="enq-1"),
                            dcc.Slider(id='enq-slider-1', min=0, max=100, step=0.01),
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
                        ], style={'display': 'none'}), 
                        html.Br(),
                        html.Br(),
                        html.Button('parkings en velostations', id='btn-plaatsen', style={'width': '100%'}),
                        html.Br(),
                        html.Div(id='inp-plaatsen', children=[
                            html.P("Plaatsen buurtparkings", id="plaatsen-0"),
                            dcc.Input(id='plaatsen-input-0',type='number'),
                            html.P("Plaatsen fietsenstallingen", id="plaatsen-1"),
                            dcc.Input(id='plaatsen-input-1',type='number'),
                            html.P("Plaatsen velostations", id="plaatsen-2"),
                            dcc.Input(id='plaatsen-input-2',type='number'),
                        ], style={'display': 'none'}),
                        html.Br(),
                        html.Br(),  
                        html.Button('Oppenbare plaatsen', id='btn-opp', style={'width': '100%'}),
                        html.Br(),
                        html.Div(id='inp-opp', children=[
                            html.P("Oppervlakte sportterreinen %", id="opp-0"),
                            dcc.Slider(id='opp-slider-0', min=0, max=1, step=0.0001),
                            html.P("Oppervlakte pleinen %", id="opp-1"),
                            dcc.Slider(id='opp-slider-1', min=0, max=25, step=0.001),
                            html.P("Oppervlakte speelterreinen %", id="opp-2"),
                            dcc.Slider(id='opp-slider-2', min=0, max=1, step=0.0001)
                        ], style={'display': 'none'})
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options", style={'overflow-y': 'scroll', 'height': '700px'}
                ),
                html.Div(
                    [dcc.Graph(id="predicties", figure=fig)],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="beste-indicatoren-chart", figure=chart)],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display"
        ),
        
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# Model layout
model_layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="./assets/datasense.png",
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Stad Antwerpen",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Fietsgebruik", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Predicties", id="predictie-button"),
                            href="/",
                        ),
                        html.A(
                            html.Button("Descriptive", id="desc-button"),
                            href="/descriptive",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [html.H2("Model accuratie"), dcc.Graph("accuracy_graph", figure=dc.get_accuracy())],
                    className="pretty_container five columns",
                )
            ],
            className="row flex-display"
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="pie_graph")],
                    className="pretty_container seven columns",
                )
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# Descriptive layout
descriptive_layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="./assets/datasense.png",
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Stad Antwerpen",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Fiets gebruik", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Predicites", id="pred-button"),
                            href="/",
                        ),
                        html.A(
                            html.Button("Model", id="model-button"),
                            href="/model",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Selecteer één of meerdere gemeenten:",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="postcode-dropdown",
                            options=[{'label': i[1], 'value': i[0]} for i in snow.get_dropdown_list()],
                            multi=True,
                            className="dcc_control",
                            searchable=False,
                            value=[2000],
                            clearable=False
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [

                            ],
                            id="info-container",
                            className="row container-display",
                        )
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="fiets-graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="leerlingen-graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="inwoners-graph")],
                    className="pretty_container sevens columns",
                ),
                html.Div(
                    [dcc.Graph(id="status-graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display"
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)