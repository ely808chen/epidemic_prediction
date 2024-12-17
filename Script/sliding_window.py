"""
This script generates a sliding window preprocessing on the single-flattened-csv file that contains disease data

In particular, it generates a sliding window preprocessing for:
(1) standard deviation of each ward (for each disease), based on the sliding window weeks
(2) average of the each ward (for each disease), based on the sliding window weeks 

Returns csv file containing sliding window of SD and Avg
"""

import os
import time
import platform
import pandas as pd
import glob
import json 
from datetime import date, timedelta

#### CHANGE TO YOUR LIKINGS ####
SLIDING_WINDOW = 5  
#### END ####

OUTPUT_DIR = "/Users/elychen/Desktop/code_personal_project/epidemic_prediction/Data/tokyo_processed_infectious_disease_data"
DATA_SOURCE_FILEPATH = "/Users/elychen/Desktop/code_personal_project/epidemic_prediction/Data/tokyo_processed_infectious_disease_data/flattened_master_disease_data.csv"
NEW_OUTPUT_CSV_NAME = "SD_sliding_window_master_disease_data.csv"

def sliding_window_preprocessing(df):
    # Groupby and calculate rolling mean
    rolling_mean = (
        df.groupby(['Disease', 'Ward'])['Value']
        .rolling(window=SLIDING_WINDOW)
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )
    
    # Groupby and calculate rolling standard deviation
    rolling_sd = (
        df.groupby(['Disease', 'Ward'])['Value']
        .rolling(window=SLIDING_WINDOW)
        .std()
        .reset_index(level=[0, 1], drop=True)
    )
    
    # Assign back to the DataFrame
    df['Rolling_mean'] = rolling_mean
    df['Rolling_SD'] = rolling_sd
    
    return df

def main():
    
    df = pd.read_csv(DATA_SOURCE_FILEPATH, header=0)

    df = sliding_window_preprocessing(df)

    # Write to csv file
    output_file_path = OUTPUT_DIR + "/" + NEW_OUTPUT_CSV_NAME
    df.to_csv(output_file_path, encoding="utf-8")

main()



