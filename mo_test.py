import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# Load the US States geometry
us_states = gpd.read_file('https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_5m.zip')

# Load the US state capitals data
capitals = pd.read_csv('us-state-capitals.csv')

# Create a GeoDataFrame for the capital cities
gdf_capitals = gpd.GeoDataFrame(capitals, geometry=gpd.points_from_xy(capitals.longitude, capitals.latitude))

# Create maps directory if it doesn't exist
os.makedirs('maps', exist_ok=True)

# Define colormap
cmap = plt.cm.get_cmap('nipy_spectral', len(us_states))

# Plot each state and save to a separate file
for i, state in enumerate(us_states['NAME'].unique()):
    state_data = us_states[us_states['NAME'] == state]
    state_capitals = gdf_capitals[gdf_capitals['name'] == state]
    fig, ax = plt.subplots(1, figsize=(5, 5))
    state_data.plot(ax=ax, color=cmap(i))
    state_capitals.plot(ax=ax, color='black', markersize=10)

    # Annotate the capital city name
    for x, y, label in zip(state_capitals.geometry.x, state_capitals.geometry.y, state_capitals['description']):
        ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

    ax.set_title(state)
    ax.axis('off')  # Remove axis
    plt.savefig(f'maps/{state}.svg', format='svg')
    plt.close(fig)  # Close the figure

# Plot all states
fig, ax = plt.subplots(1, figsize=(30, 20))  # You can adjust the figure size here
us_states.plot(ax=ax, cmap=cmap)  # Change colormap here

gdf_capitals.plot(ax=ax, color='black', markersize=10)

# Annotate the capital city names
for x, y, label in zip(gdf_capitals.geometry.x, gdf_capitals.geometry.y, gdf_capitals['description']):
    ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

ax.axis('off')  # Remove axis
plt.savefig('maps/usa.svg', format='svg')
plt.close(fig)  # Close the figure