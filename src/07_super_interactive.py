import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import requests
from tqdm import tqdm

# Load cleaned data
clean_file = "data_clean/inat_bees_clean.csv"
df = pd.read_csv(clean_file)
print("Dataset loaded. Columns:", df.columns.tolist())

# Set up cache
cache_file = "reports/image_cache.csv"
os.makedirs("reports", exist_ok=True)

if os.path.exists(cache_file):
    cache_df = pd.read_csv(cache_file)
    image_cache = dict(zip(cache_df['id'], cache_df['image_url']))
else:
    image_cache = {}

# Function to fetch image URL with caching
def fetch_image_url(observation_id):
    if observation_id in image_cache:
        return image_cache[observation_id]
    url = f"https://api.inaturalist.org/v1/observations/{observation_id}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            photos = data.get('results', [{}])[0].get('photos', [])
            if photos:
                # Use the original URL field if available
                image_url = photos[0].get('original_url')
                if image_url:
                    image_cache[observation_id] = image_url
                    return image_url
    except requests.RequestException:
        pass
    image_cache[observation_id] = None
    return None

# Create map
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=8)
marker_cluster = MarkerCluster().add_to(m)

# Assign species colors
species_list = df['taxon'].dropna().unique()
colors = {}
available_colors = [
    'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige',
    'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen',
    'gray', 'black', 'lightgray'
]
for i, species in enumerate(species_list):
    colors[species] = available_colors[i % len(available_colors)]

# Add points with popups and progress bar
for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing observations"):
    species = row['taxon']
    common = row['common_name'] if pd.notna(row['common_name']) else ""
    date = row['date'] if pd.notna(row['date']) else ""
    user = row['user'] if pd.notna(row['user']) else ""
    observation_id = row['id']

    # Fetch image URL (cached)
    image_url = fetch_image_url(observation_id)
    if not image_url:
        image_url = "https://via.placeholder.com/150"

    html = f"""
    <b>{species}</b> ({common})<br>
    Date: {date}<br>
    Observer: {user}<br>
    <img src="{image_url}" width="150"><br>
    """
    popup = folium.Popup(folium.IFrame(html=html, width=180, height=220), max_width=220)

    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=4,
        color=colors.get(species, 'gray'),
        fill=True,
        fill_opacity=0.7,
        popup=popup
    ).add_to(marker_cluster)

# Add legend
legend_html = """
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 220px; height: auto; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px; overflow: auto;">
     <b>Species Legend</b><br>
"""
for species, color in colors.items():
    legend_html += f'<i style="background:{color};width:10px;height:10px;display:inline-block;margin-right:5px;"></i>{species}<br>'
legend_html += "</div>"
m.get_root().html.add_child(folium.Element(legend_html))

# Save updated cache
pd.DataFrame(list(image_cache.items()), columns=['id', 'image_url']).to_csv(cache_file, index=False)

# Save map
os.makedirs("figures", exist_ok=True)
map_file = "figures/bee_map_super_interactive.html"
m.save(map_file)

print(f"Super interactive map with cached images saved to {map_file}")
