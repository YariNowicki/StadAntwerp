import pandas as pd
import os
import snowflake.connector
import json
from sklearn import preprocessing #Used to pre process our data

class SnowFlakeCalls:
    JSON_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.GEO_POSTZONES"
    DF_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.DISPLAY_SHAPES"
    DROPDOWN_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.DROPDOWN_LIST"
    DISPLAY_COLUMNS = ['postcode', 'jaar', 'fiets_naar_werk_school', 'naam', 'shape_area', 'shape_length']

    def get_geo_data(self):
        ctx = snowflake.connector.connect(
            user='YNOWICKI',
            password=os.getenv('SNOWSQL_PWD'),
            account='datasense.eu-west-1',
            warehouse='SMALL_WH',
            role='MOBILITY_ANTWERP',
            database='DEMO_ANTWERP_CITY')
        cs = ctx.cursor()

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

        df = pd.DataFrame(data, columns=self.DISPLAY_COLUMNS)
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
        return df, d

    def get_dropdown_list(self):
        ctx = snowflake.connector.connect(
            user='YNOWICKI',
            password=os.getenv('SNOWSQL_PWD'),
            account='datasense.eu-west-1',
            warehouse='SMALL_WH',
            role='MOBILITY_ANTWERP',
            database='DEMO_ANTWERP_CITY')
        cs = ctx.cursor()

        cs.execute(self.DROPDOWN_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=['postcode','naam'])

        out = []
        for postcode,naam in zip(df['postcode'],df['naam']):
            out.append([postcode , naam])
        return out