"""
File to flatten json file, outputting into a CSV file
"""

import os
import time
import platform
import pandas as pd
import glob
import json 
from datetime import date, timedelta

OUTPUT_DIR = "/Users/elychen/Desktop/code_personal_project/epidemic_prediction/Data/tokyo_processed_infectious_disease_data"
JSON_SOURCE_FILEPATH = "/Users/elychen/Desktop/code_personal_project/epidemic_prediction/Data/tokyo_processed_infectious_disease_data/master_disease_data.json"
NEW_OUTPUT_CSV_NAME = "flattened_master_disease_data.csv"

def main():
    # Open and read the JSON file
    data = None

    with open(JSON_SOURCE_FILEPATH, 'r') as file:
        data = json.load(file)
    
    # Flatten JSON into a DataFrame
    rows = []
    for disease, wards in data.items():
        for ward, records in wards.items():
            for record in records:
                for date, value in record.items():
                    rows.append({"Disease": disease, "Ward": ward, "Date": date, "Value": value})

    df = pd.DataFrame(rows)
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure date is in datetime format

    # Write to csv file
    output_file_path = OUTPUT_DIR + "/" + NEW_OUTPUT_CSV_NAME
    df.to_csv(output_file_path, encoding="utf-8")

main()
    
