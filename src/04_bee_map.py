import os
import pandas as pd
import folium

# load cleaned data
clean_file = "data_clean/inat_bees_clean.csv"
df = pd.read_csv(clean_file)

print("Dataset loaded. Columns:", df.columns.tolist())

# create interactive map
# center map on mean latitude and longitude
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=8)

# add points
for _, row in df.iterrows():
    # use common_name if available, otherwise taxon
    popup_label = row['common_name'] if pd.notna(row['common_name']) else row['taxon']
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=3,
        color='orange',
        fill=True,
        fill_opacity=0.6,
        popup=str(popup_label)
    ).add_to(m)

# save map
map_dir = "figures"
os.makedirs(map_dir, exist_ok=True)
map_file = os.path.join(map_dir, "bee_map.html")
m.save(map_file)

print(f"Interactive map saved to {map_file}")
