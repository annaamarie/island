import pandas as pd
import json
import glob
import os
import re

# Define the desired fields
desired_fields = [
    # Top countries
    "obj.top_countries[0].name",  # tt_top_1_country_name
    "obj.top_countries[0].code",  # tt_top_1_country_code
    "obj.top_countries[0].percent",  # tt_top_1_country_percent
    "obj.top_countries[0].followers",  # tt_top_1_country_followers
    "obj.top_countries[1].name",  # tt_top_2_country_name
    "obj.top_countries[1].code",  # tt_top_2_country_code
    "obj.top_countries[1].percent",  # tt_top_2_country_percent
    "obj.top_countries[1].followers",  # tt_top_2_country_followers
    "obj.top_countries[2].name",  # tt_top_3_country_name
    "obj.top_countries[2].code",  # tt_top_3_country_code
    "obj.top_countries[2].percent",  # tt_top_3_country_percent
    "obj.top_countries[2].followers",  # tt_top_3_country_followers
    # Age stats
    "obj.audience_genders_per_age[0].code",  # age_13_17
    "obj.audience_genders_per_age[0].male",  # age_13_17_male_percent
    "obj.audience_genders_per_age[0].female",  # age_13_17_female_percent
    "obj.audience_genders_per_age[1].code",  # age_18_24
    "obj.audience_genders_per_age[1].male",  # age_18_24_male_percent
    "obj.audience_genders_per_age[1].female",  # age_18_24_female_percent
    "obj.audience_genders_per_age[2].code",  # age_25_34
    "obj.audience_genders_per_age[2].male",  # age_25_34_male_percent
    "obj.audience_genders_per_age[2].female",  # age_25_34_female_percent
    "obj.audience_genders_per_age[3].code",  # age_35_44
    "obj.audience_genders_per_age[3].male",  # age_35_44_male_percent
    "obj.audience_genders_per_age[3].female",  # age_35_44_female_percent
    "obj.audience_genders_per_age[4].code",  # age_45_64
    "obj.audience_genders_per_age[4].male",  # age_45_64_male_percent
    "obj.audience_genders_per_age[4].female",  # age_45_64_female_percent
    "obj.audience_genders_per_age[5].code",  # age_65_plus
    "obj.audience_genders_per_age[5].male",  # age_65_plus_male_percent
    "obj.audience_genders_per_age[5].female",  # age_65_plus_female_percent
    # Gender stats
    "obj.audience_genders[0].code",  # male
    "obj.audience_genders[0].weight",  # male_percent
    "obj.audience_genders[1].code",  # female
    "obj.audience_genders[1].weight",  # female_percent
    # Other stats
    "obj.followers",  # tt_followers
    "obj.avg_likes_per_post",  # tt_avg_likes_per_post
    "obj.avg_comments_per_post",  # tt_avg_comments_per_post
    "obj.engagement_rate",  # tt_engagement_rate
]

# Function to extract data for desired fields
def extract_data(json_data, fields):
    extracted = {}
    for field in fields:
        keys = field.split('.')
        value = json_data
        try:
            for key in keys:
                if '[' in key and ']' in key:  # Handle list indexing
                    key, index = key[:-1].split('[')
                    value = value[key][int(index)]
                else:
                    value = value[key]
            extracted[field] = value
        except (KeyError, IndexError, TypeError):  # Handle missing or malformed data
            extracted[field] = None
    return extracted

# Function to extract artist ID from file name
def extract_artist_id(filename):
    print(f"Processing file: {filename}")  # Debugging log
    match = re.search(r"artist_(\d+)_", filename)
    if not match:
        print(f"Could not extract artist ID from file: {filename}")
    return int(match.group(1)) if match else None

# Path to the root directory containing subfolders for each month
root_path = "ch_artist_tt_audience_data"

# Directory to save CSV files
output_dir = os.path.join(root_path, "processed_csvs")
os.makedirs(output_dir, exist_ok=True)

# Iterate through each subfolder (month)
for folder in os.listdir(root_path):
    folder_path = os.path.join(root_path, folder)
    if os.path.isdir(folder_path):
        json_files = glob.glob(os.path.join(folder_path, "*.json"))
        
        data = []
        for file in json_files:
            with open(file, 'r') as f:
                json_data = json.load(f)
                artist_id = extract_artist_id(os.path.basename(file))  # Extract artist ID
                if artist_id is None:
                    continue  # Skip files with missing artist IDs
                record = extract_data(json_data, desired_fields)
                record["artist_id"] = artist_id  # Add artist ID to the record
                data.append(record)
        
        # Convert the data to a DataFrame
        df = pd.DataFrame(data)

        # Debugging: Print DataFrame columns
        print(f"Available columns in DataFrame for folder '{folder}': {df.columns}")

        # Rename columns
        df.rename(columns={
            # Top countries
            "obj.top_countries[0].name": "tt_top_1_country_name",
            "obj.top_countries[0].code": "tt_top_1_country_code",
            "obj.top_countries[0].percent": "tt_top_1_country_percent",
            "obj.top_countries[0].followers": "tt_top_1_country_followers",
            "obj.top_countries[1].name": "tt_top_2_country_name",
            "obj.top_countries[1].code": "tt_top_2_country_code",
            "obj.top_countries[1].percent": "tt_top_2_country_percent",
            "obj.top_countries[1].followers": "tt_top_2_country_followers",
            "obj.top_countries[2].name": "tt_top_3_country_name",
            "obj.top_countries[2].code": "tt_top_3_country_code",
            "obj.top_countries[2].percent": "tt_top_3_country_percent",
            "obj.top_countries[2].followers": "tt_top_3_country_followers",
            
            # Age stats
            "obj.audience_genders_per_age[0].code": "age_13_17",
            "obj.audience_genders_per_age[0].male": "age_13_17_male_percent",
            "obj.audience_genders_per_age[0].female": "age_13_17_female_percent",
            "obj.audience_genders_per_age[1].code": "age_18_24",
            "obj.audience_genders_per_age[1].male": "age_18_24_male_percent",
            "obj.audience_genders_per_age[1].female": "age_18_24_female_percent",
            "obj.audience_genders_per_age[2].code": "age_25_34",
            "obj.audience_genders_per_age[2].male": "age_25_34_male_percent",
            "obj.audience_genders_per_age[2].female": "age_25_34_female_percent",
            "obj.audience_genders_per_age[3].code": "age_35_44",
            "obj.audience_genders_per_age[3].male": "age_35_44_male_percent",
            "obj.audience_genders_per_age[3].female": "age_35_44_female_percent",
            "obj.audience_genders_per_age[4].code": "age_45_64",
            "obj.audience_genders_per_age[4].male": "age_45_64_male_percent",
            "obj.audience_genders_per_age[4].female": "age_45_64_female_percent",
            "obj.audience_genders_per_age[5].code": "age_65_plus",
            "obj.audience_genders_per_age[5].male": "age_65_plus_male_percent",
            "obj.audience_genders_per_age[5].female": "age_65_plus_female_percent",
            
            # Gender stats
            "obj.audience_genders[0].code": "male",
            "obj.audience_genders[0].weight": "male_percent",
            "obj.audience_genders[1].code": "female",
            "obj.audience_genders[1].weight": "female_percent",
            
            # Other stats
            "obj.followers": "tt_followers",
            "obj.avg_likes_per_post": "tt_avg_likes_per_post",
            "obj.avg_comments_per_post": "tt_avg_comments_per_post",
            "obj.engagement_rate": "tt_engagement_rate"
        }, inplace=True)

        # Reorder columns to have `artist_id` as the first column
        if "artist_id" in df.columns:
            columns_order = ["artist_id"] + [col for col in df.columns if col != "artist_id"]
            df = df[columns_order]
        else:
            print(f"'artist_id' column is missing for folder '{folder}'!")

        # Save the DataFrame to a CSV file named after the folder
        output_file = os.path.join(output_dir, f"{folder}.csv")
        df.to_csv(output_file, index=False)
        print(f"Data from folder '{folder}' saved to '{output_file}'.")

print("Data processing complete.")