import folium
import pandas as pd


data = {    'Country': ['Argentina','Colombia','United States','Spain','South Africa','Sweden','Japan','Italy','Brazil','United Kingdom','Netherlands','France','Mexico','South Korea','Germany','Australia','Canada','Thailand','Nigeria','Ireland','Kenya','India','United Arab Emirates','Singapore','Saudi Arabia','China','Malaysia','Indonesia'],
            'score':[164,136,133,133,132,130,122,120,120,119,118,117,117,116,116,109,109,98,98,96,86,71,66,64,61,59,55,55]
        }


df = pd.DataFrame(data)
if __name__ == '__main__':
    world_geo = './world_countries.json'  # Replace with the path to your GeoJSON file
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')


    folium.Choropleth(
        geo_data=world_geo,
        data=df,
        columns=['Country', 'score'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Polarization score',
        smooth_factor=0,
        Highlight=True,
        line_color="#0000",
        name='Index',
        show=True,
        overlay=True,
        nan_fill_color="White",
        water_color='gray'
    ).add_to(m)

    m.save('./data/output/Polarization_score.html')






