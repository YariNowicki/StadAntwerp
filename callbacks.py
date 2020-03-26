from dash.dependencies import Input, Output, State
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from app import app
from df_calls import DataCalls
from columns import Columns
from keras.models import load_model
from snow_calls import SnowFlakeCalls


dc = DataCalls()
snow = SnowFlakeCalls()

df, d = snow.get_geo_data()
df_pred = df.copy()
df_pred = df_pred.reset_index()
df_pred = df_pred.drop(['index'], axis=1)
mapbox_token = "pk.eyJ1IjoieWFyaW5vd2lja2kiLCJhIjoiY2s3dTk4ZDV6MDE0dDNvbW93NXBjNTZ5bSJ9.6tGy4sJsG0DOBXsEiXmPEA"
px.set_mapbox_access_token(mapbox_token)

links = {
    0: 2000,
    1: 2018,
    2: 2020,
    3: 2030,
    4: 2040,
    5: 2050,
    6: 2060,
    7: 2100,
    8: 2140,
    9: 2170,
    10: 2180,
    11: 2600,
    12: 2610,
    13: 2660
}

def get_key(val):
    for key, value in links.items():
         if val == value:
             return key

def initialize_map():
    return create_map(df_pred)


def create_map(df_pred):
    # Generates map with the prediction values
    fig = px.choropleth_mapbox(data_frame=df_pred, geojson=d, color='fiets_naar_werk_school', hover_data=["naam","postcode"],
                               color_continuous_scale=px.colors.sequential.Blues, range_color=(35, 55), zoom=9.5,
                               locations="id", featureidkey='properties.postcode', center={"lat": 51.25, "lon": 4.4})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


#  Predictions
@app.callback(Output('predicties', 'figure'),
              [Input('btn-predictie', 'n_clicks')],
              [State("{}".format(_), "value") for _ in Columns.min_max_columns_input])
def update_choropleth_mapbox_prediction(*vals):
    if vals[0] is not None:
        # Load prediction model
        model = load_model('model/DashModel.h5')
        inputs = []  # Placeholder to later place the list as a row in the DataFrame
        for v in vals[2:]:  # Loops over all the inputs and converts them to a single list
            inputs.append(v)
        inputs = dc.transfrom(inputs)
        row_df = pd.DataFrame(inputs, columns=Columns.min_max_columns)
        row_df['postcode'] = vals[1]
        row_df = row_df[Columns.input_columns]

        preds = model.predict(row_df.values)  # Predicts for each postcode

        df_pred.at[get_key(int(vals[1])), 'fiets_naar_werk_school'] = preds[0][0]
        # Generates map with the prediction values
        fig = create_map(df_pred)
        return fig
    else:
        return initialize_map()


# Aantal loontrekkenden
@app.callback(Output('werk-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.werk[0]]


@app.callback(Output('werk-0','children'),
              [Input('werk-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Loontrekkenden: {}%".format(round(val,2))


# Aantal werkzoekenden
@app.callback(Output('werk-slider-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.werk[1]]


@app.callback(Output('werk-1','children'),
              [Input('werk-slider-1', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Werkzoekenden: {}%".format(round(val,2))


# Aantal zelfstandigen
@app.callback(Output('werk-slider-2','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.werk[2]]


@app.callback(Output('werk-2','children'),
              [Input('werk-slider-2', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Zelfstandigen: {}%".format(round(val,2))


# Inactieven
@app.callback(Output('werk-slider-3','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.werk[3]]


@app.callback(Output('werk-3','children'),
              [Input('werk-slider-3', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Inactieven: {}%".format(round(val,2))


# Belastingplichtigen
@app.callback(Output('belast-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_belast_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.belastingplichtigen[0]]


@app.callback(Output('belastplicht-0','children'),
              [Input('belast-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Belastingplichtigen: {}%".format(round(val,2))


# Gemiddeld netto belastbaar inkomen
@app.callback(Output('belast-input-0','value'),
              [Input('choose-postcode', 'value')])
def fill_belast_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.belasting[0]]


# Opbrengst personenbelasting per persoon
@app.callback(Output('belast-input-1','value'),
              [Input('choose-postcode', 'value')])
def fill_belast_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.belasting[1]]


# Dichtheid
@app.callback(Output('dichtheid-input-0','value'),
              [Input('choose-postcode', 'value')])
def fill_dichtheid_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.dichtheid[0]]


# AS0
@app.callback(Output('secundair-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.secundair[0]]

@app.callback(Output('so-0','children'),
              [Input('secundair-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen ASO: {}%".format(round(val,2))


# BSO
@app.callback(Output('secundair-slider-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.secundair[1]]


@app.callback(Output('so-1','children'),
              [Input('secundair-slider-1', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen BSO: {}%".format(round(val,2))


# KSO
@app.callback(Output('secundair-slider-2','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.secundair[2]]


@app.callback(Output('so-2','children'),
              [Input('secundair-slider-2', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen KSO: {}%".format(round(val,2))


# TSO
@app.callback(Output('secundair-slider-3','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.secundair[3]]


@app.callback(Output('so-3','children'),
              [Input('secundair-slider-3', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen TSO: {}%".format(round(val,2))


# Deeltijds BSO
@app.callback(Output('secundair-slider-4','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.secundair[4]]


@app.callback(Output('so-4','children'),
              [Input('secundair-slider-4', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen deeltijds BSO: {}%".format(round(val,2))


# BUSO
@app.callback(Output('secundair-slider-5','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.secundair[5]]


@app.callback(Output('so-5','children'),
              [Input('secundair-slider-5', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen BUSO: {}%".format(round(val,2))


# Geen vertraging
@app.callback(Output('vertraging-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.vertraging[0]]


@app.callback(Output('vertraging-0','children'),
              [Input('vertraging-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen zonder vertraging: {}%".format(round(val,2))


# Leerlingen met 1 jaar vertraging
@app.callback(Output('vertraging-slider-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.vertraging[1]]


@app.callback(Output('vertraging-1','children'),
              [Input('vertraging-slider-1', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen met 1 jaar vertraging: {}%".format(round(val,2))


# Leerlingen meerdere jaren vertraging
@app.callback(Output('vertraging-slider-2','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.vertraging[2]]


@app.callback(Output('vertraging-2','children'),
              [Input('vertraging-slider-2', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen meerdere jaren vertraging: {}%".format(round(val,2))


# Leerlingen A-stroom
@app.callback(Output('stroom-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.stroom[0]]


@app.callback(Output('stroom-0','children'),
              [Input('stroom-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen A-stroom: {}%".format(round(val,2))


# Leerlingen B-stroom
@app.callback(Output('stroom-slider-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.stroom[1]]


@app.callback(Output('stroom-1','children'),
              [Input('stroom-slider-1', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen B-stroom: {}%".format(round(val,2))


# Leerlingen die naar een basisschool gaan binnen Antwerpen
@app.callback(Output('basis-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.basis[0]]


@app.callback(Output('basis-0','children'),
              [Input('basis-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen die naar een basisschool gaan binnen Antwerpen: {}%".format(round(val,2))


# Leerlingen die naar een basisschool gaan buiten Antwerpen
@app.callback(Output('basis-slider-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.basis[1]]


@app.callback(Output('basis-1','children'),
              [Input('basis-slider-1', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen die naar een basisschool gaan buiten Antwerpen: {}%".format(round(val,2))


# Leerlingen die naar een secundaire school gaan binnen Antwerpen %
@app.callback(Output('so-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.so[0]]


@app.callback(Output('so-a-0','children'),
              [Input('so-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen die naar een secundaire school gaan binnen Antwerpen: {}%".format(round(val,2))


# Leerlingen die naar een secundaire school gaan buiten Antwerpen %
@app.callback(Output('so-slider-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.so[1]]


@app.callback(Output('so-a-1','children'),
              [Input('so-slider-1', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen die naar een secundaire school gaan buiten Antwerpen: {}%".format(round(val,2))


#  Kotdichtheid
@app.callback(Output('kotdichtheid-input-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.kot[0]]


@app.callback(Output('kot-0','children'),
              [Input('kotdichtheid-input-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Kotdichtheid: {}%".format(val)


# Bibliotheek bezocht
@app.callback(Output('enq-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.enq[0]]


@app.callback(Output('enq-0','children'),
              [Input('enq-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Bibliotheek bezocht: {}%".format(val)


# Boek gelezen
@app.callback(Output('enq-slider-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.enq[1]]


@app.callback(Output('enq-1','children'),
              [Input('enq-slider-1', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Boek gelezen: {}%".format(val)


# Museum bezocht
@app.callback(Output('enq-slider-2','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.enq[2]]


@app.callback(Output('enq-2','children'),
              [Input('enq-slider-2', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Museum bezocht: {}%".format(val)

# Park bezocht
@app.callback(Output('enq-slider-3','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.enq[3]]


@app.callback(Output('enq-3','children'),
              [Input('enq-slider-3', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Park bezocht: {}%".format(val)


# Restaurant of café bezocht
@app.callback(Output('enq-slider-4','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.enq[4]]


@app.callback(Output('enq-4','children'),
              [Input('enq-slider-4', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Restaurant of café bezocht: {}%".format(val)


# Televisie gekeken
@app.callback(Output('enq-slider-5','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.enq[5]]


@app.callback(Output('enq-5','children'),
              [Input('enq-slider-5', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Televisie gekeken: {}%".format(val)


# Voorstelling bezocht
@app.callback(Output('enq-slider-6','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.enq[6]]


@app.callback(Output('enq-6','children'),
              [Input('enq-slider-6', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Voorstelling bezocht: {}%".format(val)


# Sport beoefend
@app.callback(Output('enq-slider-7','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.enq[7]]


@app.callback(Output('enq-7','children'),
              [Input('enq-slider-7', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Sport beoefend: {}%".format(val)


# Plaatsen buurtparkings
@app.callback(Output('plaatsen-input-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.plaatsen[0]]


# Plaatsen fietsenstallingen
@app.callback(Output('plaatsen-input-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.plaatsen[1]]


# Plaatsen velostations
@app.callback(Output('plaatsen-input-2','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.plaatsen[2]]


# Oppervlakte sportterreinen
@app.callback(Output('opp-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.opp[0]]


@app.callback(Output('opp-0','children'),
              [Input('opp-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Oppervlakte sportterreinen (tot 1% van het totaal oppervlakte): {}%".format(round(val,2))

# Oppervlakte pleinen
@app.callback(Output('opp-slider-1','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.opp[1]]


@app.callback(Output('opp-1','children'),
              [Input('opp-slider-1', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Oppervlakte pleinen (tot 25% van het totaal oppervlakte): {}%".format(round(val,2))

# Oppervlate speelterreinen
@app.callback(Output('opp-slider-2','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.opp[2]]


@app.callback(Output('opp-2','children'),
              [Input('opp-slider-2', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Oppervlate speelterreinen (tot 1% van het totaal oppervlakte): {}%".format(round(val,2))














'''
def create_work_slider(text, number, inp):
    return html.Div(
        id='inp-werk-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='werk-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp,
            )
        ]
    )


def create_belasting_input(text, number, inp):
    return html.Div(
        id='inp-belast-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Input(
                id='belast-input-{}'.format(number),
                type='number',
                value=inp
            )
        ]
    )


def create_belast_plichtigen_slider(text, number, inp):
    return html.Div(
        id='inp-belast_plichtigen-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='belast-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp,
            )
        ]
    )


def create_dichtheid_input(text, number, inp):
    return html.Div(
        id='inp-dichtheid-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Input(
                id='dichtheid-input-{}'.format(number),
                type='number',
                value=inp[0]
            )
        ]
    )


def create_secundair_slider(text, number, inp):
    return html.Div(
        id='inp-secundair-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='secundair-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp,
            )
        ]
    )


def create_vertraging_slider(text, number, inp):
    return html.Div(
        id='inp-vertraging-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='vertraging-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp,
            )
        ]
    )


def create_stroom_slider(text, number, inp):
    return html.Div(
        id='inp-stroom-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='stroom-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp,
            )
        ]
    )


def create_basis_slider(text, number, inp):
    return html.Div(
        id='inp-basis-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='basis-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp,
            )
        ]
    )


def create_so_slider(text, number, inp):
    return html.Div(
        id='inp-so-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='so-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp,
            )
        ]
    )


def create_kotdichtheid_input(text, number, inp):
    return html.Div(
        id='inp-kotdichtheid-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='kotdichtheid-input-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp[0],
            )
        ]
    )


def create_enq_slider(text, number, inp):
    return html.Div(
        id='inp-enq-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='enq-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp,
            )
        ]
    )


def create_plaatsen_input(text, number, inp):
    return html.Div(
        id='inp-plaatsen-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Input(
                id='plaatsen-slider-{}'.format(number),
                type='number',
                value=inp
            )
        ]
    )


def create_opp_slider(text, number, inp):
    return html.Div(
        id='inp-opp-container-{}'.format(number),
        children=[
            html.P(text),
            dcc.Slider(
                id='opp-slider-{}'.format(number),
                min=0,
                max=1,
                step=0.01,
                value=inp
            )
        ]
    )

#  CALLBACKS


@app.callback(Output('inp-werk', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-werk', 'children')])
def werk_inp(_, postcode, inputs):
    inp = dc.get_inp_data(postcode)
    inputs = []
    for c in Columns.werk:
        div = create_work_slider(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-belastingen', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-belastingen', 'children')])
def belastingen_inp(_, postcode, inputs):
    inp = dc.get_inp_data(postcode)
    inputs = []
    for c in Columns.belasting:
        div = create_belasting_input(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-belasting-plichtigen', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-belasting-plichtigen', 'children')])
def belasting_plichtigen_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    div = create_belast_plichtigen_slider('belastingplichtigen', len(inputs), inp['belastingplichtigen'])
    inputs.append(div)
    return inputs


@app.callback(Output('inp-dichtheid', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-dichtheid', 'children')])
def dichtheid_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    div = create_dichtheid_input('dichtheid', len(inputs), inp[Columns.dichtheid])
    inputs.append(div)
    return inputs


@app.callback(Output('inp-secundair', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-secundair', 'children')])
def secundair_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    for c in Columns.secundair:
        div = create_secundair_slider(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-vertraging', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-vertraging', 'children')])
def vertraging_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    for c in Columns.vertraging:
        div = create_vertraging_slider(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-stroom', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-stroom', 'children')])
def stroom_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    for c in Columns.stroom:
        div = create_stroom_slider(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-basis-a', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-basis-a', 'children')])
def basis_a_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    for c in Columns.basis:
        div = create_basis_slider(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-so-a', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-so-a', 'children')])
def so_a_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    for c in Columns.so:
        div = create_so_slider(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-kot', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-kot', 'children')])
def kot_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    inp = inp[Columns.kot] / 100
    div = create_kotdichtheid_input('kotdichtheid', len(inputs), inp)
    inputs.append(div)
    return inputs


@app.callback(Output('inp-enq', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-enq', 'children')])
def enq_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    inp[Columns.enq] = inp[Columns.enq] / 100
    for c in Columns.enq:
        div = create_enq_slider(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-plaatsen', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-plaatsen', 'children')])
def plaatsen_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    for c in Columns.plaatsen:
        div = create_plaatsen_input(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs


@app.callback(Output('inp-opp', 'children'),
              [Input('choose-postcode', 'value')],
              [State('choose-postcode', 'value'),
               State('inp-opp', 'children')])
def opp_inp(_, postcode, inputs):
    inputs = []
    inp = dc.get_inp_data(postcode)
    for c in Columns.opp:
        div = create_opp_slider(c, len(inputs), inp[c])
        inputs.append(div)
    return inputs
'''