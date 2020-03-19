from dash.dependencies import Input, Output, State
import pandas as pd
import src.DataReceiver as Dr
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
from app import app
from src.Main import Main

m = Main()

snow = Dr.DataReceiver()
df, d = snow.get_geo_data()
df_pred = df.copy()  # Used later for the prediction map
input_data = snow.get_input_data()
input_data = input_data[(input_data['jaar'] == 2015) & (input_data['postcode'] == '2000')][snow.COLS_INPUTS]
cols = ['postcode']
cols += snow.COLS_INPUTS

px.set_mapbox_access_token(m.mapbox_token)


def create_todo_item(todo_text, todo_number):
    return html.Div(
        id='input-container-{}'.format(todo_number),
        children=[
            html.Span(todo_text),
            dcc.Slider(
                id='slider-{}'.format(todo_number),
                min=0,
                max=1.1,
                step=0.01,
                value=input_data[todo_text].values[0],
            )
        ]
    )


@app.callback(Output('inputs', 'children'),
              [Input('add-input', 'value')],
              [State('add-input', 'value'),
               State('inputs', 'children')])
def append_todo(_, __, existing_todos):
    for c in snow.COLS_INPUTS:
        existing_todos.append(create_todo_item(c, len(existing_todos)))
    return existing_todos


# Gets all the input values and generates a prediction for each postcode
@app.callback(Output('predicties', 'figure'),[Input("slider-{}".format(i), "value") for i in range(len(snow.COLS_INPUTS))])
def create_choropleth_mapbox_prediction(*vals):
    # Load prediction model
    model = m.load()
    input_df = pd.DataFrame(columns=cols)  # Creates a DataFrame with input columns + postcode column
    input_df['postcode'] = df['postcode']  # Fills up the DataFrame with postcodes, so the amount of rows are correct
    inputs = ['postcode']  # Placeholder to later place the list as a row in the DataFrame
    for v in vals:  # Loops over all the inputs and converts them to a single list
        inputs.append(v)
    for i in range(len(input_df)):  # Loops over all the DataFrame rows so each one gets filled
        input_df.loc[i] = inputs
    input_df['postcode'] = df['postcode']  # Replaces the placeholder with the actual postcode
    preds = model.predict(input_df.values)  # Predicts for each postcode
    df_pred['fiets_naar_werk_school'] = preds

    # Generates map with the prediction values
    fig = px.choropleth_mapbox(data_frame=df_pred, geojson=d, color='fiets_naar_werk_school',color_continuous_scale=px.colors.sequential.Blues, range_color=(35, 55),zoom=9.5,
                        locations="id", featureidkey='properties.postcode',center={"lat":51.25, "lon": 4.4})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


