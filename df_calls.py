import pandas as pd
from sklearn import preprocessing #Used to pre process our data
import numpy as np
from columns import Columns
from snow_calls import SnowFlakeCalls
import warnings
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from keras.models import load_model
warnings.simplefilter(action='ignore', category=FutureWarning)

class DataCalls:
    snow = SnowFlakeCalls()
    df = snow.get_input_data()
    inputs = df[Columns.input_columns]
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))  # puts everything in a range between 0 and 1
    min_max_scaler.fit(inputs)

    def __init__(self):
        pass

    def get_inp_data(self, postcode):
        df_inp = self.df.copy()
        df_inp = df_inp[df_inp['postcode'] == str(postcode)]
        df_inp = df_inp[Columns.input_columns]
        return df_inp.iloc[-5] 

    def transfrom(self, inp):
        return self.min_max_scaler.transform([inp])

    def get_inwoners(self, postcode):
        df_inp = self.snow.get_inwoners()
        df_inp = df_inp[df_inp['postcode'] == str(postcode)]
        return df_inp['aantal_inwoners']

    def weight_chart(self):
        model2 = load_model('model/NewDashModel.h5')
        weight = model2.get_weights()
        df_weight = pd.DataFrame(weight[0])
        df_weight = df_weight.transpose()
        df_weight.columns = Columns.input_columns
        df_weight = df_weight.sort_values(axis=1, by=[0])
        fig = go.Figure()
        for column in df_weight.columns[-5:]:
            fig.add_trace(go.Bar(x=[column], y=[df_weight[column].loc[0]],name=column))
            fig.update_layout(title='Meest invloedrijke indicatoren',showlegend=False)
        return fig
