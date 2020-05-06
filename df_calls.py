import pandas as pd
from sklearn import preprocessing #Used to pre process our data
from columns import Columns
from snow_calls import SnowFlakeCalls
import warnings
import plotly.graph_objects as go
import plotly.express as px
from keras.models import load_model
warnings.simplefilter(action='ignore', category=FutureWarning)

class DataCalls:
    snow = SnowFlakeCalls()
    df = snow.get_input_data()
    df['school_binnen_antwerpen'] = df[['al_basis_binnen_a', 'al_so_binnen_a']].mean(axis=1)
    df = df.drop(['al_basis_binnen_a', 'al_so_binnen_a','al_a_stroom','opbrengst_aanvullende_personenbelasting_per_belast','opbrengst_aanvullende_personenbelasting_per_belast'], axis=1)
    inputs = df[Columns.input_columns]
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))  # puts everything in a range between 0 and 1
    min_max_scaler.fit(inputs)

    def __init__(self):
        pass

    def get_inp_data(self, postcode):
        df_inp = self.df.copy()
        df_inp = df_inp[df_inp['postcode'] == postcode]
        df_inp = df_inp[Columns.input_columns]
        return df_inp.iloc[-5] 

    def transfrom(self, inp):
        return self.min_max_scaler.transform([inp])

    def get_inwoners(self, postcode):
        df_inp = self.snow.get_inwoners()
        df_inp = df_inp[df_inp['postcode'] == postcode]
        return df_inp['aantal_inwoners']


    # TODO: Feature importance: "Individuele toebrengst bij een waarde van 1 (100%)"
    def weight_chart(self):
        values = [  5.3445067,  6.405532 , 10.086257 , 10.751836 ,  9.21963  ,
                    8.687151 ,  8.410953 ,  2.2411668,  5.0256376,  9.957881 ,
                    10.121722 ,  8.532995 , 10.114749 ,  4.348169 ,  6.762181 ,
                    12.746373 , 11.036478 ,  9.031443 , 12.229608 ,
                    9.355006 ]
        columns = ['werkenden', 'belastingsplichtigen',
                    'gemiddeld_netto_belastbaar_inkomen_per_persoon', 'dichtheid',
                    'bibliotheek_bezocht', 'boek_gelezen', 'park_bezocht',
                    'restaurant_of_cafe_bezocht', 'televisie_gekeken',
                    'voorstelling_bezocht', 'sport_beoefend', 'theoretisch_geschoolden',
                    'al_so_geen_vertraging', 'plaatsen_buurtparkings',
                    'plaatsen_fietsenstallingen', 'plaatsen_velo_stations',
                    'opp_sportterreinen', 'opp_gebruiksgroen_en_pleinen',
                    'opp_speelterreinen',
                    'school_binnen_antwerpen']
        df_weight = pd.DataFrame(values)
        df_weight = df_weight.transpose()
        df_weight.columns = columns
        df_weight = df_weight.sort_values(axis=1, by=[0])
        fig = go.Figure()
        for column in df_weight.columns[-5:]:
            fig.add_trace(go.Bar(x=[column], y=[df_weight[column].loc[0]],name=column))
            fig.update_layout(title='Meest invloedrijke indicatoren',showlegend=False)
        return fig
    

    def get_accuracy(self):
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

