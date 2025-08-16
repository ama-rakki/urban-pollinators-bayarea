import os
import pandas as pd
import matplotlib.pyplot as plt
import folium

#load raw data
raw_file = "data_raw/inat_bees.csv"
df = pd.read_csv(raw_file)

print("First few rows of the dataset:")
print(df.head())
print("\nDataset info:")
print(df.info())

#clean data

# drop duplicates
df = df.drop_duplicates()

# convert columns to correct types
if 'observed_on' in df.columns:
    df['observed_on'] = pd.to_datetime(df['observed_on'], errors='coerce')

if 'lat' in df.columns:
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
if 'lon' in df.columns:
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

# drop rows missing coordinates
df = df.dropna(subset=['lat', 'lon'])

# filter for bees only if there's a 'taxon_rank' or 'family' column
if 'family' in df.columns:
    df = df[df['family'].str.contains("Apidae|Halictidae|Megachilidae|Andrenidae|Colletidae|Melittidae|Stenotritidae", na=False)]

# exploartory analysis

# top 10 species observed
if 'species_guess' in df.columns:
    print("\nTop 10 species observed:")
    print(df['species_guess'].value_counts().head(10))

# top 10 genera observed
if 'genus' in df.columns:
    print("\nTop 10 genera observed:")
    print(df['genus'].value_counts().head(10))

# bbservations per year
if 'observed_on' in df.columns:
    df['year'] = df['observed_on'].dt.year
    yearly_counts = df['year'].value_counts().sort_index()
    print("\nObservations per year:")
    print(yearly_counts)

    # plot yearly observations
    plt.figure(figsize=(10,6))
    yearly_counts.plot(kind='bar', color='skyblue')
    plt.xlabel("Year")
    plt.ylabel("Number of Observations")
    plt.title("Bee Observations by Year")
    plt.tight_layout()
    plt.show()

# observations per city if column exists
if 'place_guess' in df.columns:
    city_counts = df['place_guess'].value_counts().head(10)
    print("\nTop 10 cities/locations observed:")
    print(city_counts)

    plt.figure(figsize=(10,6))
    city_counts.plot(kind='barh', color='lightgreen')
    plt.xlabel("Number of Observations")
    plt.ylabel("City/Location")
    plt.title("Top Cities for Bee Observations")
    plt.tight_layout()
    plt.show()

# interactive map with Folium
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=8)

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=3,
        color='orange',
        fill=True,
        fill_opacity=0.6,
        popup=str(row.get('common_name', 'Western Honey Bee'))
    ).add_to(m)

map_file = "data_clean/bee_map.html"
os.makedirs("data_clean", exist_ok=True)
m.save(map_file)
print(f"\nInteractive map saved to {map_file}")

# save cleaned data
clean_file = "data_clean/inat_bees_clean.csv"
df.to_csv(clean_file, index=False)
print(f"Cleaned data saved to {clean_file}")
