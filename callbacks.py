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
mapbox_token = "pk.eyJ1IjoieWFyaW5vd2lja2kiLCJhIjoiY2s3dTk4ZDV6MDE0dDNvbW93NXBjNTZ5bSJ9.6tGy4sJsG0DOBXsEiXmPEA"
px.set_mapbox_access_token(mapbox_token)


def initialize_map():
    return create_map(df_pred)


def create_map(df_pred):
    # Generates map with the prediction values
    fig = px.choropleth_mapbox(data_frame=df_pred, geojson=d, color='fiets_naar_werk_school',
                               color_continuous_scale=px.colors.sequential.Blues, range_color=(35, 55), zoom=9.5,
                               locations="id", featureidkey='properties.postcode', center={"lat": 51.25, "lon": 4.4})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

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


#  Predictions
@app.callback(Output('predicties', 'figure'),
                [Input("{}".format(_), "value") for _ in Columns.min_max_columns_input])
def update_choropleth_mapbox_prediction(*vals):
    # Load prediction model
    model = load_model('model/DashModel.h5')
    postcodes = dc.get_postcodes()
    input_df = pd.DataFrame(columns=Columns.min_max_columns)  # Creates a DataFrame with input columns + postcode column
    # input_df['postcode'] = postcodes # Fills up the DataFrame with postcodes, so the amount of rows are correct
    inputs = []  # Placeholder to later place the list as a row in the DataFrame
    for v in vals:  # Loops over all the inputs and converts them to a single list
        inputs.append(v)
    print(inputs)
    inputs = dc.transfrom(inputs)
    print(inputs[0].tolist())
    row_df = pd.DataFrame(inputs, columns=Columns.min_max_columns)
    #row_df['postcode'] = vals[0]
    # row_df = row_df[Columns.input_columns]
    for i in range(len(postcodes)):  # Loops over all the DataFrame rows so each one gets filled
        input_df = input_df.append(row_df)
    input_df['postcode'] = postcodes
    input_df = input_df[Columns.input_columns]
    # input_df = input_df.drop(['postcode'], axis=1) # Replaces the placeholder with the actual postcode
    preds = model.predict(input_df.values)  # Predicts for each postcode
    df_pred['fiets_naar_werk_school'] = preds

    # Generates map with the prediction values
    fig = create_map(df_pred)

    return fig

















