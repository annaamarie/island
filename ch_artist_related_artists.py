import pandas as pd
import json
import glob
import os
import re

# Define the desired fields and ranks
desired_fields = [
    ("obj[0].name", "artist_name", 1),
    ("obj[0].sp_followers", "artist_followers", 1),
    ("obj[0].popularity", "artist_popularity", 1),
    ("obj[0].image_url", "artist_image_url", 1),
    ("obj[0].cm_artist_rank", "artist_cm_rank", 1),
    ("obj[0].genres.primary.name", "artist_primary_genre", 1),
    ("obj[0].code2", "artist_country_code", 1),
    ("obj[1].name", "artist_name", 2),
    ("obj[1].sp_followers", "artist_followers", 2),
    ("obj[1].popularity", "artist_popularity", 2),
    ("obj[1].image_url", "artist_image_url", 2),
    ("obj[1].cm_artist_rank", "artist_cm_rank", 2),
    ("obj[1].genres.primary.name", "artist_primary_genre", 2),
    ("obj[1].code2", "artist_country_code", 2),
    ("obj[2].name", "artist_name", 3),
    ("obj[2].sp_followers", "artist_followers", 3),
    ("obj[2].popularity", "artist_popularity", 3),
    ("obj[2].image_url", "artist_image_url", 3),
    ("obj[2].cm_artist_rank", "artist_cm_rank", 3),
    ("obj[2].genres.primary.name", "artist_primary_genre", 3),
    ("obj[2].code2", "artist_country_code", 3),
    ("obj[3].name", "artist_name", 4),
    ("obj[3].sp_followers", "artist_followers", 4),
    ("obj[3].popularity", "artist_popularity", 4),
    ("obj[3].image_url", "artist_image_url", 4),
    ("obj[3].cm_artist_rank", "artist_cm_rank", 4),
    ("obj[3].genres.primary.name", "artist_primary_genre", 4),
    ("obj[3].code2", "artist_country_code", 4),
    ("obj[4].name", "artist_name", 5),
    ("obj[4].sp_followers", "artist_followers", 5),
    ("obj[4].popularity", "artist_popularity", 5),
    ("obj[4].image_url", "artist_image_url", 5),
    ("obj[4].cm_artist_rank", "artist_cm_rank", 5),
    ("obj[4].genres.primary.name", "artist_primary_genre", 5),
    ("obj[4].code2", "artist_country_code", 5),
]

# Function to extract data for desired fields
def extract_data_with_rank(json_data, fields):
    extracted_records = []
    for field, column_name, rank in fields:
        keys = field.split('.')
        value = json_data
        try:
            for key in keys:
                if '[' in key and ']' in key:  # Handle list indexing
                    key, index = key[:-1].split('[')
                    value = value[key][int(index)]
                else:
                    value = value[key]
        except (KeyError, IndexError, TypeError):  # Handle missing or malformed data
            value = None

        extracted_records.append({"column_name": column_name, "value": value, "rank": rank})
    return extracted_records

# Function to extract artist ID from file name
def extract_artist_id(filename):
    match = re.search(r"artist_(\d+)_", filename)
    return int(match.group(1)) if match else None

# Path to the folder containing JSON files
input_folder = "ch_artist_related_artists"

# Process all JSON files in the folder
json_files = glob.glob(os.path.join(input_folder, "*.json"))

data = []
for file in json_files:
    with open(file, 'r') as f:
        json_data = json.load(f)
        artist_id = extract_artist_id(os.path.basename(file))  # Extract artist ID
        if artist_id is None:
            continue  # Skip files with missing artist IDs
        records = extract_data_with_rank(json_data, desired_fields)
        for record in records:
            record["artist_id"] = artist_id
        data.extend(records)

# Convert the data to a DataFrame and pivot it
df = pd.DataFrame(data)
df = df.pivot(index=["artist_id", "rank"], columns="column_name", values="value").reset_index()

# Reorder columns
if "artist_id" in df.columns:
    columns_order = ["artist_id", "rank"] + [col for col in df.columns if col not in ["artist_id", "rank"]]
    df = df[columns_order]

# Save the final DataFrame to a CSV file in the same folder
output_file = os.path.join(input_folder, "ch_related_artists.csv")
df.to_csv(output_file, index=False)
print(f"Data saved to '{output_file}'.")