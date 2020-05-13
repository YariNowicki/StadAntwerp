import pandas as pd
import os
import snowflake.connector
from codecs import open  # File reader/writes
import json
from columns import Columns
from datetime import datetime 

def login():
    ctx = snowflake.connector.connect(
        user='YNOWICKI',
        password=os.getenv('SNOWSQL_PWD'),
        account='datasense.eu-west-1',
        warehouse='SMALL_WH',
        role='MOBILITY_ANTWERP',
        database='DEMO_ANTWERP_CITY')
    cs = ctx.cursor()
    return cs

def login_dv():
    ctx = snowflake.connector.connect(
        user='YNOWICKI',
        password=os.getenv('SNOWSQL_PWD'),
        account='datasense.eu-west-1',
        warehouse='SMALL_WH',
        role='MOBILITY_ANTWERP',
        database='DEMO_ANTWERP_CITY')
    cs = ctx.cursor()
    return cs, ctx

class SnowFlakeCalls:
    JSON_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.GEO_POSTZONES"
    DF_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.DISPLAY_SHAPES"
    DROPDOWN_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.DROPDOWN_LIST"
    INPUT_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.DASH_INPUT"
    INWONERS_QUERY = "select postzone, aantal_inwoners from DEMO_ANTWERP_CITY.DEMO_DV_BV.INPUT_DATA WHERE jaar = 2020"
    FIETSGEBRUIK_QUERY = "select * from DEMO_ANTWERP_CITY.DEMO_DV_BV.FIETSGEBRUIK"
    SCHOOL_QUERY = "select * from DEMO_ANTWERP_CITY.DEMO_DV_BV.SCHOOL_LEERLINGEN"
    INWONER_STATUS_QUERY = "select * from DEMO_ANTWERP_CITY.DEMO_DV_BV.INWONER_STATUS"
    SCALE_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.SCALE_DATA"
    PREDICTION_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.PREDICTIONS"

    def get_geo_data(self):
        print("Getting snowflake data...(geo data)")
        cs = login()

        def link(postcode):
            links = {
                1: 2000,
                2: 2018,
                3: 2020,
                4: 2030,
                5: 2040,
                6: 2050,
                7: 2060,
                8: 2100,
                9: 2140,
                10: 2170,
                11: 2180,
                12: 2600,
                13: 2610,
                14: 2660
            }
            for k, v in links.items():
                if postcode == v:
                    return k

        cs.execute(self.DF_QUERY)
        data = cs.fetchall()

        df = pd.DataFrame(data, columns=Columns.display)
        df = df.sort_values(by=['postcode'])
        df['fiets_naar_werk_school'] = df['fiets_naar_werk_school'].str.replace(',', '.')
        df['fiets_naar_werk_school'] = pd.to_numeric(df['fiets_naar_werk_school'])
        df = df.fillna(0)
        df['id'] = range(1, 15)

        cs.execute(self.JSON_QUERY)
        j = cs.fetchall()
        d = json.loads(j[0][0])

        for feat in d['features']:
            feat['id'] = link(feat['properties']['postcode'])
        print("Done!")
        return df, d

    def get_dropdown_list(self):
        print("Getting snowflake data...(Dropdownlist)")
        cs = login()
        cs.execute(self.DROPDOWN_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=['postcode','naam'])

        out = []
        for postcode,naam in zip(df['postcode'],df['naam']):
            out.append([postcode , naam])
        print("Done!")
        return out

    def get_input_data(self):
        print("Getting snowflake data...(Input data)")
        cs = login()
        cs.execute(self.INPUT_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=Columns.total_columns)
        df = df[Columns.total_columns]
        print("Done!")
        return df

    def get_inwoners(self):
        cs = login()
        cs.execute(self.INWONERS_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=['postcode','aantal_inwoners'])
        return df

    def get_fietsgebruik(self, postcodes):
        postcodes = list(map(str, postcodes))
        cs = login()
        cs.execute(self.FIETSGEBRUIK_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=['postcode', 'jaar', 'fietsers'])
        df = df[df['postcode'].isin(postcodes)]
        df = self.apply_names(df)
        return df

    def get_inwoners_display(self, postcodes):
        postcodes = list(map(str, postcodes))
        cs = login()
        cs.execute(self.INWONERS_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=['postcode','inwoners'])
        df = df[df['postcode'].isin(postcodes)]
        df = self.apply_names(df)
        return df

    def get_school_leerlingen_display(self, postcodes):
        postcodes = list(map(str, postcodes))
        cs = login()
        cs.execute(self.SCHOOL_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=['postcode','basis_a', 'so_a'])
        df = df[df['postcode'].isin(postcodes)]
        df = self.apply_names(df)
        return df

    def get_werk_data(self, postcodes):
        postcodes = list(map(str, postcodes))
        cs = login()
        cs.execute(self.INWONER_STATUS_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=['postcode', 'jaar','loontrekkenden', 'werkzoekenden','zelfstandigen','inactieven'])
        df = df[df['postcode'].isin(postcodes)]
        df = self.apply_names(df)
        return df

    def save_prediction(self, inputs):
        cs = login()
        now = datetime.now() 
        Q = "INSERT INTO DEMO_ANTWERP_CITY.PRED_DATA.PREDICTIONS SELECT "
        for i in inputs:
            Q = Q + str(i) + ", "
        date = str(now).split()
        Q = Q + "'{}', '{}'".format(date[0],date[1])
        Q = Q + ";"
        cs.execute(Q)
        return "Done"

    def get_predictions(self):
        cs = login()
        cs.execute(self.PREDICTION_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=Columns.prediction_columns)
        return df

    def apply_names(self, df):
        names = self.get_dropdown_list()
        def f(row):
            for name in names:
                if str(name[0]) == str(row['postcode']):
                    return name[1]
            return "NOT FOUND"
        df['naam'] = df.apply(f, axis=1)
        return df

    def update_datavault(self):
        cs, ctx = login_dv()
        files = [
            '/home/ubuntu/StadAntwerp/SQL/1_EXT_PRED_PREDICTIONS_INCR.sql',
            '/home/ubuntu/StadAntwerp/SQL/2_STG_PRED_PREDICTIONS_INCR.sql',
            '/home/ubuntu/StadAntwerp/SQL/3_HUB_PRED_PREDICTIONS_INCR.sql',
            '/home/ubuntu/StadAntwerp/SQL/4_LNK_PRED_PREDICTIONS_POSTZONES_INCR.sql',
            '/home/ubuntu/StadAntwerp/SQL/5_SAT_TEMP_TGT.sql',
            '/home/ubuntu/StadAntwerp/SQL/6_SAT_INUR_TGT.sql',
            '/home/ubuntu/StadAntwerp/SQL/7_SAT_ED_TGT.sql',
        ]
        for item in files:
            print(item)
            with open(item, 'r', encoding='utf-8') as f:
                try:
                    for cur in ctx.execute_stream(f):
                        for ret in cur:
                            print(ret)
                except Exception as e: pass
        print('Datavault updated!')


