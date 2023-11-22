import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load the world shape map without any additional info (assuming 'world_countries.shp' is a shapefile)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Assume 'country_happiness.csv' is a CSV file with 'country' and 'happiness_index' columns
# Load Happiness Index data
happiness_index_data = pd.read_csv('country_happiness.csv')

# Merge the geodataframe with the happiness index data
# This assumes that the name of the country field is the same in both dataframes and is 'name'
world_with_happiness = world.merge(happiness_index_data, how="left", left_on="name", right_on="country")

# Plot the world map colored by happiness index
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world_with_happiness.plot(column='happiness_index', ax=ax, legend=True,
                          legend_kwds={'label': "Happiness Index by Country",
                                       'orientation': "horizontal"})

plt.show()