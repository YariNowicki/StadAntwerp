import pandas as pd
import os
import snowflake.connector
import json
from sklearn import preprocessing #Used to pre process our data

class DataReceiver:
    JSON_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.GEO_POSTZONES"
    DF_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.DISPLAY_SHAPES"
    INPUT_QUERY = "SELECT * FROM DEMO_ANTWERP_CITY.DEMO_DV_BV.INPUT_DATA WHERE JAAR > 2005"
    DISPLAY_COLUMNS = ['postcode', 'jaar', 'fiets_naar_werk_school', 'naam', 'shape_area', 'shape_length']
    COLUMNS = ['postcode', 'jaar', 'aantal_loontrekkenden', 'aantal_werkzoekende', 'aantal_zelfstandigen',
               'inactieven', 'werkloosheidsdruk', 'belastingplichtigen',
               'gemiddeld_netto_belastbaar_inkomen_per_persoon',
               'opbrengst_aanvullende_personenbelasting_per_belast', 'totaal_netto_inkomen', 'aantal_inwoners',
               'dichtheid',
               'bibliotheek_bezocht', 'boek_gelezen', 'museum_bezocht', 'park_bezocht', 'restaurant_of_cafe_bezocht',
               'televisie_gekeken',
               'voorstelling_bezocht', 'sport_beoefend', 'tevredenheid_staat_wegen', 'tevreden_met_fiets_en_voetpaden',
               'voldoende_bussen_trams', 'voldoende_parkeerplaatsen_voor_bewoners',
               'regelmatig_de_fiets_naar_werk_school',
               'regelmatig_te_voet_naar_werk_school', 'al_aso', 'al_bso', 'al_kso', 'al_tso', 'al_deel_bso',
               'al_basis_binnen_a',
               'al_basis_buiten_a', 'al_buso', 'al_so_geen_vertraging', 'al_so_vertraging', 'al_so_meer_vertraging',
               'al_a_stroom',
               'al_b_stroom', 'al_so_binnen_a', 'al_so_buiten_a', 'aantal_koten', 'kotdichtheid',
               'plaatsen_buurtparkings', 'buurtparkings',
               'fietsenstallingen', 'plaatsen_fietsenstallingen', 'sportterreinen', 'speelterreinen',
               'opp_sportterreinen', 'opp_gebruiksgroen_en_pleinen',
               'opp_speelterreinen', 'plaatsen_velo_stations', 'velo_stations']
    COLS_CHANGED = ['bibliotheek_bezocht', 'boek_gelezen',
                    'museum_bezocht',
                    'park_bezocht',
                    'restaurant_of_cafe_bezocht',
                    'televisie_gekeken',
                    'voorstelling_bezocht',
                    'sport_beoefend',
                    'regelmatig_de_fiets_naar_werk_school',
                    'regelmatig_te_voet_naar_werk_school']
    COLS_INPUTS = ['aantal_loontrekkenden', 'aantal_werkzoekende', 'aantal_zelfstandigen',
                   'inactieven', 'werkloosheidsdruk', 'belastingplichtigen',
                   'gemiddeld_netto_belastbaar_inkomen_per_persoon',
                   'opbrengst_aanvullende_personenbelasting_per_belast', 'dichtheid',
                   'bibliotheek_bezocht', 'boek_gelezen', 'museum_bezocht', 'park_bezocht',
                   'restaurant_of_cafe_bezocht', 'televisie_gekeken',
                   'voorstelling_bezocht', 'sport_beoefend',
                   'regelmatig_te_voet_naar_werk_school', 'al_aso', 'al_bso', 'al_kso', 'al_tso', 'al_deel_bso',
                   'al_basis_binnen_a',
                   'al_basis_buiten_a', 'al_buso', 'al_so_geen_vertraging', 'al_so_vertraging', 'al_so_meer_vertraging',
                   'al_a_stroom',
                   'al_b_stroom', 'al_so_binnen_a', 'al_so_buiten_a', 'aantal_koten', 'kotdichtheid',
                   'plaatsen_buurtparkings', 'buurtparkings',
                   'fietsenstallingen', 'plaatsen_fietsenstallingen', 'sportterreinen', 'speelterreinen',
                   'opp_sportterreinen', 'opp_gebruiksgroen_en_pleinen',
                   'opp_speelterreinen', 'plaatsen_velo_stations', 'velo_stations']
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

    def get_input_data(self):
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
        df = pd.DataFrame(data, columns=self.COLUMNS)
        output = df['regelmatig_de_fiets_naar_werk_school']
        output = output.str.replace(',', '.')
        output = pd.to_numeric(output)
        df = df.drop(['tevredenheid_staat_wegen', 'tevreden_met_fiets_en_voetpaden',
                      'voldoende_bussen_trams', 'voldoende_parkeerplaatsen_voor_bewoners'], axis=1)
        for col in self.COLS_CHANGED:
            df[col] = df[col].str.replace(',', '.')
            df[col] = pd.to_numeric(df[col])
        min_max_scaler = preprocessing.MinMaxScaler() # puts everything in a range between 0 and 1
        for col in self.COLS_INPUTS:
            null_index = df[col].isnull()
            df.loc[~null_index, [col]] = min_max_scaler.fit_transform(df.loc[~null_index, [col]])
        df = df.fillna(-1)
        return df