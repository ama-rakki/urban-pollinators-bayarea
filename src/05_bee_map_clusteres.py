import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import random

# load cleaned data
clean_file = "data_clean/inat_bees_clean.csv"
df = pd.read_csv(clean_file)

print("Dataset loaded. Columns:", df.columns.tolist())

# create interactive map
# center map on mean latitude and longitude
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=8)

# create a MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

# generate colors for each species
species_list = df['taxon'].dropna().unique()
colors = {}
available_colors = [
    'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige',
    'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen',
    'gray', 'black', 'lightgray'
]

# assign a color to each species, cycling if more species than colors
for i, species in enumerate(species_list):
    colors[species] = available_colors[i % len(available_colors)]

# add points to the cluster
for _, row in df.iterrows():
    popup_label = row['common_name'] if pd.notna(row['common_name']) else row['taxon']
    species_color = colors.get(row['taxon'], 'gray')
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=4,
        color=species_color,
        fill=True,
        fill_opacity=0.7,
        popup=str(popup_label)
    ).add_to(marker_cluster)

# save map
map_dir = "figures"
os.makedirs(map_dir, exist_ok=True)
map_file = os.path.join(map_dir, "bee_map_clustered.html")
m.save(map_file)

print(f"Clustered interactive map saved to {map_file}")
