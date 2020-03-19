import plotly.express as px
from keras.models import load_model


class Main:
    mapbox_token = "pk.eyJ1IjoieWFyaW5vd2lja2kiLCJhIjoiY2s3dTk4ZDV6MDE0dDNvbW93NXBjNTZ5bSJ9.6tGy4sJsG0DOBXsEiXmPEA"

    def __init__(self):
        print("created")

    def create_choropleth_mapbox(self, df, d):
        fig = px.choropleth_mapbox(data_frame=df,
                                   geojson=d,
                                   color='fiets_naar_werk_school',
                                   range_color=(0, 55),
                                   color_continuous_scale=px.colors.sequential.Blues,
                                   zoom=9.5,
                                   locations="id",
                                   featureidkey='properties.postcode',
                                   center={"lat": 51.25, "lon": 4.4})

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def load(self):
        return load_model('./model/DashModel.h5')
