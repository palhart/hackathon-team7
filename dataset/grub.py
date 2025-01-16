import pandas as pd
import os
import json

def add_json_to_csv(json_data, csv_file_path):
    # Convert JSON to DataFrame

    json_object = json.loads(json_data)

    new_data = pd.json_normalize(json_object)

    # Load existing CSV data
    if os.path.exists(csv_file_path):
        existing_data = pd.read_csv(csv_file_path)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        combined_data = new_data

    # Save back to CSV
    combined_data.to_csv(csv_file_path, index=False)