import requests
import pandas as pd
from tqdm import tqdm

# Bay Area bounding box (west=-123, east=-121, south=36.9, north=38.6)
bbox = [-123.0, 36.9, -121.0, 38.6]

# Bee taxon ID on iNat = 630955
taxon_id = 630955

base_url = "https://api.inaturalist.org/v1/observations"

def fetch_inat_data(taxon_id, bbox, per_page=200, max_pages=10):
    records = []
    for page in tqdm(range(1, max_pages + 1)):
        params = {
            "taxon_id": taxon_id,
            "quality_grade": "research",
            "geo": "true",
            "identified": "true",
            "per_page": per_page,
            "page": page,
            "nelat": bbox[3], "nelng": bbox[2],
            "swlat": bbox[1], "swlng": bbox[0]
        }
        r = requests.get(base_url, params=params)
        r.raise_for_status()
        data = r.json()["results"]
        if not data:
            break
        for obs in data:
            records.append({
                "id": obs["id"],
                "date": obs.get("observed_on"),
                "lat": obs["geojson"]["coordinates"][1],
                "lon": obs["geojson"]["coordinates"][0],
                "taxon": obs["taxon"]["name"] if obs.get("taxon") else None,
                "common_name": obs["taxon"].get("preferred_common_name") if obs.get("taxon") else None,
                "user": obs["user"]["login"]
            })
    return pd.DataFrame(records)

if __name__ == "__main__":
    df = fetch_inat_data(taxon_id, bbox, max_pages=20)
    df.to_csv("data_raw/inat_bees.csv", index=False)
    print(f"Saved {len(df)} observations.")
