import pandas as pd
from sklearn import preprocessing #Used to pre process our data
import numpy as np
from columns import Columns


class DataCalls:
    df = pd.read_csv('data/df_avg.csv')
    inputs = df[Columns.min_max_columns]
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))  # puts everything in a range between 0 and 1
    min_max_scaler.fit(inputs)

    def __init__(self):
        pass

    def get_input_data(self):
        df_inp = self.df.copy()
        df_inp = df_inp[df_inp['jaar'] == 2017].dropna(axis=0, how='any')
        return df_inp

    def get_dropdown_data(self):
        df_drop = self.df.copy()
        df_drop = df_drop.drop(['Unnamed: 0'], axis=1)
        df_drop = df_drop[df_drop['jaar'] == 2017].dropna(axis=0, how='any')
        out = []
        for p in df_drop['postcode']:
            out.append([str(p),p])
        return out

    def get_inp_data(self, postcode):
        out = pd.DataFrame(columns=self.df.columns)
        df_inp_werk = self.df.copy()
        for i in range(len(df_inp_werk)):
            if int(df_inp_werk.loc[i]['postcode']) == int(postcode):
                out.loc[i] = df_inp_werk.loc[i]
        out = out.drop(['Unnamed: 0'], axis=1)
        return out.iloc[-1]

    def get_postcodes(self):
        out = self.df.copy()
        out = out['postcode'].sort_values().unique()
        return out

    def transfrom(self, inp):
        return self.min_max_scaler.transform([inp])

