# src/02_clean_explore.py

import os
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# 1. Load the raw data
# -------------------------
raw_file = "data_raw/inat_bees.csv"
df = pd.read_csv(raw_file)

print("First few rows of the dataset:")
print(df.head())
print("\nDataset info:")
print(df.info())
print("\nMissing values per column:")
print(df.isna().sum())

# -------------------------
# 2. Clean the data
# -------------------------

# Drop duplicate rows
df = df.drop_duplicates()

# Convert columns to correct types
if 'observed_on' in df.columns:
    df['observed_on'] = pd.to_datetime(df['observed_on'], errors='coerce')

if 'lat' in df.columns:
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
if 'lon' in df.columns:
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

# Optionally remove rows with missing coordinates
df = df.dropna(subset=['lat', 'lon'])

# -------------------------
# 3. Exploratory analysis
# -------------------------

# Top 10 species observed
if 'species_guess' in df.columns:
    print("\nTop 10 species observed:")
    print(df['species_guess'].value_counts().head(10))

# Basic scatter map of observations
plt.figure(figsize=(8,6))
plt.scatter(df['lon'], df['lat'], s=5, alpha=0.5)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("iNaturalist Bee Observations")
plt.tight_layout()
plt.show()

# Observations per year
if 'observed_on' in df.columns:
    df['year'] = df['observed_on'].dt.year
    yearly_counts = df['year'].value_counts().sort_index()
    print("\nObservations per year:")
    print(yearly_counts)
    
    # Plot observations per year
    plt.figure(figsize=(8,6))
    yearly_counts.plot(kind='bar')
    plt.xlabel("Year")
    plt.ylabel("Number of Observations")
    plt.title("Bee Observations by Year")
    plt.tight_layout()
    plt.show()

# -------------------------
# 4. Save cleaned data
# -------------------------
clean_dir = "../data_clean"
os.makedirs(clean_dir, exist_ok=True)
clean_file = os.path.join(clean_dir, "inat_bees_clean.csv")
df.to_csv(clean_file, index=False)
print(f"\nCleaned data saved to {clean_file}")
