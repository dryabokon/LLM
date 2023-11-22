import folium
import pandas as pd

# Assuming 'happiness_index.csv' is a CSV file with 'Country' and 'Happiness_Index' columns
happiness_index_data = pd.read_csv('./data/ex_datasets/happiness_index.csv')

# Path to the GeoJSON file (this must be stored locally or accessible via a URL)
geojson_path = './data/ex_datasets/world_countries.json'

# Initialize a folium map at a global scale
m = folium.Map(location=[0, 0], zoom_start=2)

# Create a Choropleth layer
folium.Choropleth(
    geo_data=geojson_path,
    name='choropleth',
    data=happiness_index_data,
    columns=['Country', 'Index'],  # replace with actual column names in your CSV
    key_on='feature.properties.name',  # replace with the key that contains country names in your GeoJSON
    fill_color='RdBu',  # Color scheme
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Happiness Index',
    water_color='gray',
).add_to(m)

# Add layer control to toggle the Choropleth layer
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('happiness_index_map.html')

