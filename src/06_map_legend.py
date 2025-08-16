import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# load cleaned data
clean_file = "data_clean/inat_bees_clean.csv"
df = pd.read_csv(clean_file)
print("Dataset loaded. Columns:", df.columns.tolist())

# create interactive cluster 
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=8)

# marker cluster
marker_cluster = MarkerCluster().add_to(m)

# generate colors for each species
species_list = df['taxon'].dropna().unique()
colors = {}
available_colors = [
    'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige',
    'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen',
    'gray', 'black', 'lightgray'
]

for i, species in enumerate(species_list):
    colors[species] = available_colors[i % len(available_colors)]

# add points
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

# add legend
legend_html = """
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: auto; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;">
     <b>Species Legend</b><br>
"""
for species, color in colors.items():
    legend_html += f'<i style="background:{color};width:10px;height:10px;display:inline-block;margin-right:5px;"></i>{species}<br>'
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

# save map
map_dir = "figures"
os.makedirs(map_dir, exist_ok=True)
map_file = os.path.join(map_dir, "bee_map_clustered_legend.html")
m.save(map_file)

print(f"Clustered interactive map with legend saved to {map_file}")
