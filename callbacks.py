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
from snow_calls import SnowFlakeCalls
warnings.simplefilter(action='ignore', category=FutureWarning)
mapbox_token = "pk.eyJ1IjoieWFyaW5vd2lja2kiLCJhIjoiY2s3dTk4ZDV6MDE0dDNvbW93NXBjNTZ5bSJ9.6tGy4sJsG0DOBXsEiXmPEA"
px.set_mapbox_access_token(mapbox_token)

dc = DataCalls()
snow = SnowFlakeCalls()
df_weight = pd.read_csv('/home/ubuntu/StadAntwerp/assets/weights.csv')
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

# Displays fietsers (descriptive graph)
@app.callback(Output('fiets-graph', 'figure'),
              [Input('postcode-dropdown', 'value')])
def display_fietsgebruik(value):
    df = snow.get_fietsgebruik(value)
    df = df.sort_values(by=['jaar'])
    fig = px.line(df, x="jaar", y="fietsers", color='naam')
    fig.update_layout(title='% regelmatige fietsgebruikers naar het werk/school')
    return fig

# Displays inwoners (descriptive graph)
@app.callback(Output('inwoners-graph', 'figure'),
              [Input('postcode-dropdown', 'value')])
def display_inwoners(value):
    df = snow.get_inwoners_display(value)
    fig = go.Figure(data=[go.Pie(labels=df["naam"], values=df["inwoners"], hole=.3)])
    fig.update_layout(title='Aantal inwoners')
    return fig

# Descriptive graph
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

# Descriptive Graph
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
    fig = px.sunburst(df, path=['naam','label'], values='value')
    fig.update_layout(title="Status inwoners (2016)")
    return fig



#  Predictions
@app.callback(Output('predicties', 'figure'),
              [Input('btn-predictie', 'n_clicks')],
              [State("{}".format(_), "value") for _ in Columns.min_max_columns_input])
def update_choropleth_mapbox_prediction(*vals):
    if vals[0] is not None:
        pred = [vals[1]]
        # Load prediction model
        model = load_model('/home/ubuntu/StadAntwerp/model/r957mse5.h5')
        inputs = []  # Placeholder to later place the list as a row in the DataFrame
        for v in vals[2:]:  # Loops over all the inputs and converts them to a single list
            if v is not None:
                pred.append(v)
                inputs.append(v)
            else:
                inputs.append(-1)
                pred.append(-1)      
        inwoners = dc.get_inwoners(vals[1])
        
        # Changes totaal parkings spaces to parking spaces/total inwoners
        inputs[-7] = inputs[-7]/inwoners.values[0]
        inputs[-6] = inputs[-6]/inwoners.values[0]
        inputs[-5] = inputs[-5]/inwoners.values[0]
        
        # Minmaxscaling
        inputs = dc.transfrom(inputs)
        inputs = get_encoding_data(vals[1], inputs)
        
        # Converts lists to the right order
        new_order = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,0,1,2,3,4,5,6,7,8,9,10,11,12,30]
        pred_index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,20,14,15,16,17,18,19]
        pred = [pred[i] for i in pred_index]
        inputs = inputs[new_order]

        preds = model.predict(inputs.reshape(1,-1))  # Predicts for each postcode
        df_pred.at[get_key(int(vals[1])), 'fiets_naar_werk_school'] = preds[0][0]
        pred.append(preds[0][0])
        snow.save_prediction(pred)
        print('updating datavault...')
        snow.update_datavault()
        # Generates map with the prediction values
        fig = create_map(df_pred)
        return fig
    else:
        return initialize_map()

# Prediction graph
@app.callback(Output('main_graph','figure'),
              [Input('output-clientside', 'children')])
def dot_plot_predictions(s):
    s = SnowFlakeCalls()
    df = s.get_predictions()
    df['postcode'] = df['postcode'].astype(str)
    fig = px.scatter(df, x="postcode", y="fiets_percentage",
                title="Predicties")
    return fig

# Prediction graph
@app.callback(Output('pie_graph','figure'),
              [Input('main_graph', 'hoverData')])
def dot_plot_predictions(s):
    postcode = s['points'][0]['x']
    fiets = s['points'][0]['y']
    s = SnowFlakeCalls()
    df = s.get_predictions()
    df['postcode'] = df['postcode'].astype(str)
    df = df[(df['postcode'] == str(postcode)) & (df['fiets_percentage'] == fiets)].head(1)
    fig = go.Figure()
    for c in Columns.percentage_display:
        fig.add_trace(go.Bar(x=[c],y=df[c]))
    fig.update_layout(showlegend=False, title='Indicatoren')
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
    return df['dichtheid']


# Theoretisch geschoolden
@app.callback(Output('secundair-slider-0','value'),
              [Input('choose-postcode', 'value')])
def fill_werk_inputs(postcode):
    df = dc.get_inp_data(postcode)
    return df['theorestisch_geschoolden']

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
    return df['al_so_geen_vertraging']


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