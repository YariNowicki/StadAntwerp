import pandas as pd
import os
import snowflake.connector
import json
from columns import Columns

class SnowFlakeCalls:
    JSON_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.GEO_POSTZONES"
    DF_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.DISPLAY_SHAPES"
    DROPDOWN_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.DROPDOWN_LIST"
    INPUT_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.INPUT_AVG"


    def get_geo_data(self):
        print("Getting snowflake data...(geo data)")
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
        print("Done!")
        return out

    def get_input_data(self):
        print("Getting snowflake data...(Input data)")
        ctx = snowflake.connector.connect(
            user='YNOWICKI',
            password=os.getenv('SNOWSQL_PWD'),
            account='datasense.eu-west-1',
            warehouse='SMALL_WH',
            role='MOBILITY_ANTWERP',
            database='DEMO_ANTWERP_CITY')
        cs = ctx.cursor()
        cs.execute(self.INPUT_QUERY)
        data = cs.fetchall()
        df = pd.DataFrame(data, columns=Columns.total_columns)
        print("Done!")
        return df