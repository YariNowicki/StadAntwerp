import pandas as pd
from sklearn import preprocessing #Used to pre process our data
from columns import Columns
from snow_calls import SnowFlakeCalls
import warnings
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


    # TODO: Feature importance
    '''
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
    '''

    def get_accuracy():
        data = [[47.98647689819336, 31.554601669311523, 30.945764541625977, 51.00542449951172, 27.1306095123291, 
                59.93107604980469, 50.98125457763672, 41.13679504394531, 35.689308166503906, 32.51605987548828, 
                52.912109375],
                [46.6, 30.3, 32.8, 49.1, 28.2, 60.3, 54.3, 40.8, 34.2, 27.3, 51.0]]
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data[0], x=list(range(len(data[0]))), name='Predicted values',
                                line = dict(color='royalblue')))
        fig.add_trace(go.Scatter(y=data[1], x=list(range(len(data[1]))), name='Actual values',
                                line = dict(color='green')))
        return fig
