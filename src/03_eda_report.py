import os
import pandas as pd
import matplotlib.pyplot as plt

# load cleaned data
clean_file = "data_clean/inat_bees_clean.csv"
df = pd.read_csv(clean_file)
os.makedirs("reports", exist_ok=True)

print("Dataset loaded. Columns:", df.columns.tolist())

# general summary
summary_file = "reports/general_summary.txt"
with open(summary_file, 'w') as f:
    f.write("General Dataset Summary\n")
    f.write("====================\n")
    f.write(str(df.describe(include='all')))
    f.write("\n\nMissing Values:\n")
    f.write(str(df.isna().sum()))
print(f"General summary saved to {summary_file}")

# species level summary
if 'taxon' in df.columns:
    species_counts = df['taxon'].value_counts()
    species_counts.to_csv("reports/species_counts.csv")
    
    # Plot top 10 species
    plt.figure(figsize=(12,6))
    species_counts.head(10).plot(kind='bar', color='lightgreen')
    plt.xlabel("Species")
    plt.ylabel("Number of Observations")
    plt.title("Top 10 Bee Species")
    plt.tight_layout()
    plt.savefig("reports/top_10_species.png")
    plt.close()

# yearly trends
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    
    yearly_counts = df.groupby('year').size()
    yearly_counts.to_csv("reports/yearly_counts.csv")
    
    # Plot yearly trends
    plt.figure(figsize=(10,6))
    yearly_counts.plot(marker='o', color='skyblue')
    plt.xlabel("Year")
    plt.ylabel("Number of Observations")
    plt.title("Yearly Observation Trends")
    plt.tight_layout()
    plt.savefig("reports/yearly_observations.png")
    plt.close()

# top locations
if 'common_name' in df.columns:  # If you want to summarize by common name
    top_locations = df.groupby(['taxon','common_name']).size().reset_index(name='count')
    top_locations.to_csv("../data_reports/top_locations_per_species.csv")

print("EDA report generation complete. All outputs are in the 'data_reports' folder.")
