# Import required libraries
from app import app
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from df_calls import DataCalls
from columns import Columns
from keras.models import load_model
from snow_calls import SnowFlakeCalls
import plotly.express as px
import warnings
import statistics
import plotly.graph_objects as go
warnings.simplefilter(action='ignore', category=FutureWarning)
mapbox_token = "pk.eyJ1IjoieWFyaW5vd2lja2kiLCJhIjoiY2s3dTk4ZDV6MDE0dDNvbW93NXBjNTZ5bSJ9.6tGy4sJsG0DOBXsEiXmPEA"
px.set_mapbox_access_token(mapbox_token)

dc = DataCalls()
snow = SnowFlakeCalls()
df_weight = pd.read_csv('assets/weights.csv')
df, d = snow.get_geo_data()
df_pred = df.copy()
df_pred = df_pred.reset_index()
df_pred = df_pred.drop(['index'], axis=1)

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


def get_encoding_data(postcode, inputs):
    if postcode == 2000:
        inputs = np.append(np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2018:
        inputs = np.append(np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2020:
        inputs = np.append(np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2050:
        inputs = np.append(np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2060:
        inputs = np.append(np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2100:
        inputs = np.append(np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2140:
        inputs = np.append(np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2170:
        inputs = np.append(np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2180:
        inputs = np.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2600:
        inputs = np.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]).reshape(-1, 1), (inputs))
    elif postcode == 2610:
        inputs = np.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]).reshape(-1, 1), (inputs))
    else:
        inputs = np.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(-1, 1), (inputs))
    return inputs


def get_key(val):
    for key, value in links.items():
         if val == value:
             return key

def initialize_map():
    return create_map(df_pred)


def create_map(df_pred):
    # Generates map with the prediction values
    fig = px.choropleth_mapbox(data_frame=df_pred, geojson=d, color='fiets_naar_werk_school', hover_data=["naam","postcode"],
                               color_continuous_scale=px.colors.sequential.Blues, range_color=(20, 60), zoom=9.5,
                               locations="id", featureidkey='properties.postcode', center={"lat": 51.25, "lon": 4.4})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, title='Antwerpen')
    return fig


@app.callback(Output('fiets-graph', 'figure'),
              [Input('postcode-dropdown', 'value')])
def display_fietsgebruik(value):
    df = snow.get_fietsgebruik(value)
    df = df.sort_values(by=['jaar'])
    fig = px.line(df, x="jaar", y="fietsers", color='naam')
    fig.update_layout(title='% regelmatige fietsgebruikers naar het werk/school')
    return fig

@app.callback(Output('inwoners-graph', 'figure'),
              [Input('postcode-dropdown', 'value')])
def display_inwoners(value):
    df = snow.get_inwoners_display(value)
    fig = go.Figure(data=[go.Pie(labels=df["naam"], values=df["inwoners"], hole=.3)])
    fig.update_layout(title='Aantal inwoners')
    return fig


@app.callback(Output('leerlingen-graph', 'figure'),
              [Input('postcode-dropdown', 'value')])
def display_leerlingen(value):
    df = snow.get_school_leerlingen_display(value)
    fig = go.Figure(data=[
        go.Bar(name='Basisonderwijs', x=df["naam"], y=df["basis_a"]),
        go.Bar(name='Secundair onderwijs', x=df["naam"], y=df["so_a"])
    ])
    fig.update_layout(title="% Leerlingen die naar school gaan binnen Antwerpen (2018)")
    return fig


@app.callback(Output('status-graph', 'figure'),
              [Input('postcode-dropdown', 'value')])
def display_leerlingen(value):
    df = snow.get_werk_data(value)
    data = []
    for index, row in df.iterrows():
        r = [row['naam'], row['jaar'], 'loontrekkenden', int(row['loontrekkenden'])]
        r2 = [row['naam'], row['jaar'], 'werkzoekenden', int(row['werkzoekenden'])]
        r3 = [row['naam'], row['jaar'], 'zelfstandigen', int(row['zelfstandigen'])]
        r4 = [row['naam'], row['jaar'], 'inactieven', int(row['inactieven'])]
        data.append(r)
        data.append(r2)
        data.append(r3)
        data.append(r4)
    display = pd.DataFrame(data, columns=['naam', 'jaar', 'label', 'value'])
    df = display.copy()
    '''
    fig = px.sunburst(display, path=['naam', 'label'], values='value')
    fig.update_layout(title="Status inwoners")
    '''
    fig = px.sunburst(df, path=['naam','label'], values='value')
    fig.update_layout(title="Status inwoners (2016)")
    return fig



#  Predictions
@app.callback(Output('predicties', 'figure'),
              [Input('btn-predictie', 'n_clicks')],
              [State("{}".format(_), "value") for _ in Columns.min_max_columns_input])
def update_choropleth_mapbox_prediction(*vals):
    if vals[0] is not None:
        # Load prediction model
        model = load_model('model/r957mse5.h5')
        inputs = []  # Placeholder to later place the list as a row in the DataFrame
        for v in vals[2:]:  # Loops over all the inputs and converts them to a single list
            if v is not None:
                inputs.append(v)
            else:
                inputs.append(-1)
        inwoners = dc.get_inwoners(vals[1])
        inputs[-6] = inputs[-6]/inwoners.values[0]
        inputs[-5] = inputs[-5]/inwoners.values[0]
        inputs[-4] = inputs[-4]/inwoners.values[0]
        inputs = dc.transfrom(inputs)
        inputs = get_encoding_data(vals[1], inputs)
        new_order = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,0,1,2,3,4,5,6,7,8,9,10,11,12,30]
        inputs = inputs[new_order]
        preds = model.predict(inputs.reshape(1,-1))  # Predicts for each postcode
        df_pred.at[get_key(int(vals[1])), 'fiets_naar_werk_school'] = preds[0][0]
        # Generates map with the prediction values
        fig = create_map(df_pred)
        return fig
    else:
        return initialize_map()


def get_ci(z):
    box_data = []
    for c in df_weight.columns:
        ci_minus = df_weight[c].mean() - (z * (statistics.stdev(df_weight[c].tolist())/10))
        ci_max = df_weight[c].mean() + (z * (statistics.stdev(df_weight[c].tolist())/10))
        mean = df_weight[c].mean()
        box_data.append([c, ci_minus, mean, ci_max])
    df_ci = pd.DataFrame(box_data, columns=['indicator', 'ci_min', 'waarde', 'ci_max'])
    df_ci = df_ci.sort_values(by=['waarde']).reset_index()
    df_ci = df_ci.drop(['index'], axis=1)
    df_ci['difference'] = df_ci['ci_max'] - df_ci['waarde']
    
    df_ci = df_ci.reset_index()
    return df_ci


def get_z(perc):
    z = 0
    if perc == 90:
        z = 1.645
    elif perc == 95:
        z = 1.96
    elif perc == 98:
        z = 2.326
    elif perc == 99:
        z = 2.576
    return z

# Main graph
@app.callback(Output('main_graph','figure'),
              [Input('year-slider', 'value')])
def sign_bad(value):
    z = get_z(value[0]) 
    if z != 0:
        df = get_ci(z)
    fig = px.scatter(df[:3], x="indicator", y="waarde", color="indicator",
                 error_y="difference", error_y_minus="difference")
    fig.update_layout(
        width = 800,
        height = 500,
        title = "Betrouwbaarheid van de meest negatieve indicatoren",
        showlegend=True,
        yaxis = dict(
        scaleanchor = "x",
        scaleratio = 1,
        ),
        xaxis= dict(
            autorange=True,
            showgrid=False,
            ticks='',
            showticklabels=False
        ),
    )
    return fig


# Pie graph
@app.callback(Output('pie_graph','figure'),
              [Input('year-slider', 'value')])
def sign_bad(value):
    z = get_z(value[0]) 
    if z != 0:
        df = get_ci(z)  
    fig = px.scatter(df.reset_index()[-3:], x="indicator", y="waarde", color="indicator",
                 error_y="difference", error_y_minus="difference")
    fig.update_layout(
        width = 800,
        height = 500,
        title = "Betrouwbaarheid van de meest positieve indicatoren",
        showlegend=False,
        yaxis = dict(
        scaleanchor = "x",
        scaleratio = 1,
        ),
        xaxis= dict(
            autorange=True,
            showgrid=False,
            ticks='',
            showticklabels=False
        )
    )
    return fig
    

# Button inwoners
@app.callback(Output('inp-inwoners','style'),
              [Input('btn-inwoners', 'n_clicks')])
def inwoners(value):
    if value is not None:
        if (value % 2) != 0:
            return {}
    return {'display': 'none'}

# Button onderwijs
@app.callback(Output('inp-onderwijs','style'),
              [Input('btn-onderwijs', 'n_clicks')])
def inwoners(value):
    if value is not None:
        if (value % 2) != 0:
            return {}
    return {'display': 'none'}

# Button enq
@app.callback(Output('inp-enq','style'),
              [Input('btn-enq', 'n_clicks')])
def inwoners(value):
    if value is not None:
        if (value % 2) != 0:
            return {}
    return {'display': 'none'}

# Button opp
@app.callback(Output('inp-opp','style'),
              [Input('btn-opp', 'n_clicks')])
def inwoners(value):
    if value is not None:
        if (value % 2) != 0:
            return {}
    return {'display': 'none'}


# Button plaatsen
@app.callback(Output('inp-plaatsen','style'),
              [Input('btn-plaatsen', 'n_clicks')])
def inwoners(value):
    if value is not None:
        if (value % 2) != 0:
            return {}
    return {'display': 'none'}

#
# All callbacks below are used to either display the value of sliders in the UI or to fill the values in the sliders
#

# Aantal werkenden
@app.callback(Output('werk-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df['werkenden']


@app.callback(Output('werk-0','children'),
              [Input('werk-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Werkenden: {}%".format(round(val,2))

# Belastingplichtigen
@app.callback(Output('belast-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_belast_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df['belastingplichtigen']


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
    return df['gemiddeld_netto_belastbaar_inkomen_per_persoon']


# Dichtheid
@app.callback(Output('dichtheid-input-0','value'),
              [Input('choose-postcode', 'value')])
def fill_dichtheid_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df[Columns.dichtheid[0]]


# Theoretisch geschoolden
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
    return "Aantal theoretisch geschoolden: {}%".format(round(val,2))


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



# Leerlingen die naar een school gaan binnen Antwerpen
@app.callback(Output('school-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df['school_binnen_antwerpen']


@app.callback(Output('school-0','children'),
              [Input('school-slider-0', 'value')])
def fill_werk_inputs(val):
    if val is None:
        val = 0
    return "Leerlingen die naar een school gaan binnen Antwerpen: {}%".format(round(val,2))



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