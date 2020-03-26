import pandas as pd
from sklearn import preprocessing #Used to pre process our data
import numpy as np
from columns import Columns
from snow_calls import SnowFlakeCalls


class DataCalls:
    snow = SnowFlakeCalls()
    df = snow.get_input_data()
    inputs = df[Columns.min_max_columns]
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))  # puts everything in a range between 0 and 1
    min_max_scaler.fit(inputs)

    def __init__(self):
        pass

    def get_inp_data(self, postcode):
        df_inp = self.df.copy()
        df_inp = df_inp[(df_inp['jaar'] == 2016) & (df_inp['postcode'] == str(postcode))]
        df_inp = df_inp[Columns.min_max_columns]
        return df_inp.iloc[-1]

    def transfrom(self, inp):
        return self.min_max_scaler.transform([inp])

    def get_inwoners(self, postcode):
        df_inp = self.df.copy()
        df_inp = df_inp[(df_inp['jaar'] == 2020) & (df_inp['postcode'] == str(postcode))]
        return df_inp['aantal_inwoners']

