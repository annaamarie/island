import json
import csv
import os
from collections import defaultdict

# Define the folder with JSON files
folder_path = "ch_artist_charts"

# Define the list of artist IDs
artistIds = [
  781320, 10281098, 3651398, 834, 384142, 1011054, 717312, 3923533,
  207335, 217633, 3167, 9990449, 3972463, 3544186, 4373808, 8812446,
  12653520, 208137, 751087, 1653887, 1525222, 1404155, 260988,
  3730441, 493676, 1348885, 691085, 4550, 4934, 538222, 3883672,
  1939, 10440582, 7946705, 4539948
]

# Prepare a dictionary to aggregate data for all artists
artist_summary = defaultdict(lambda: {
    "total_charts": set(),
    "total_tracks": 0,
    "most_popular_track": None,
    "highest_chart_rank": float("inf"),
    "regions_represented": set()
})

# Loop through all JSON files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        
        # Load JSON file
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Process each track entry
        for entry in data["obj"]["data"]["entries"]:
            artist_id = entry["cm_artist"][0] 
            chart_key = f"{entry['chart_name']}_{entry['code2']}"
            
            # Aggregate data
            artist_summary[artist_id]["total_charts"].add(chart_key)
            artist_summary[artist_id]["total_tracks"] += 1
            artist_summary[artist_id]["regions_represented"].add(entry["code2"])
            
            # Update most popular track
            if not artist_summary[artist_id]["most_popular_track"] or entry["rank"] < artist_summary[artist_id]["highest_chart_rank"]:
                artist_summary[artist_id]["most_popular_track"] = entry["name"]
                artist_summary[artist_id]["highest_chart_rank"] = entry["rank"]

# Ensure all artist IDs are included in the final CSV
for artist_id in artistIds:
    if artist_id not in artist_summary:
        artist_summary[artist_id] = {
            "total_charts": set(),
            "total_tracks": 0,
            "most_popular_track": None,
            "highest_chart_rank": "NaN",
            "regions_represented": set()
        }

# Define the output file path inside the folder
output_file = os.path.join(folder_path, "ch_artists_charts.csv")

# Write aggregated data to a CSV file
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["artist_id", "total_charts", "regions_represented", "total_tracks", "most_popular_track", "highest_chart_rank"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for artist_id in artistIds:
        summary = artist_summary[artist_id]
        writer.writerow({
            "artist_id": artist_id,
            "total_charts": len(summary["total_charts"]),
            "regions_represented": ", ".join(summary["regions_represented"]) if summary["regions_represented"] else "NaN",
            "total_tracks": summary["total_tracks"],
            "most_popular_track": summary["most_popular_track"] if summary["most_popular_track"] else "NaN",
            "highest_chart_rank": summary["highest_chart_rank"]
        })

print(f"CSV file generated and saved in folder: {output_file}")
