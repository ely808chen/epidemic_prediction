"""
Main file to process raw weekly epidemic data to a single JSON file with epidemic data from all years 

Input: weekly epidemic data (output from data_main.py) 
Output: Single JSON file containing all infectious-disease-relevant data from all weeks in all years

Output data structure:

data = {
    "disease_1": {
        "ward_1": [
            {"2025-01-01": 5.0},
            {"2025-01-02": 3.5},
        ],
        "ward_2": [
            {"2025-01-01":4.0},
            {"2025-01-02": 3.0},
        ],
    },
    "disease_2": {
        "ward_1": [
            {"2025-01-01": 4.0},
            {"2025-01-02": 3.3},
        ],
    },
}

Usage: Simply run main()
"""

import os
import time
import platform
import pandas as pd
import glob
import json 
from datetime import date, timedelta

DATA_SOURCE_DIR = "/Users/elychen/Desktop/code_personal_project/epidemic_prediction/Data/tokyo_infectious_disease_data"
OUTPUT_DIR = "/Users/elychen/Desktop/code_personal_project/epidemic_prediction/Data/tokyo_processed_infectious_disease_data"

SPECIAL_YEARS_WITH_53_WEEKS = [2004, 2009, 2015, 2020]
WKS_UPPER_RANGE_SPECIAL_YR_INCL = 53
WKS_UPPER_RANGE_REG_YR_INCL = 52
WKS_UPPER_RANGE_CUR_YR_INCL = 49
START_YR = 2001
CURRENT_YR = 2024

DISEASE_NAMES = ['Unnamed: 0', 'インフルエンザ', '新型コロナウイルス感染症（COVID-19）', 'RSウイルス感染症', '咽頭結膜熱',
       'Ａ群溶血性レンサ球菌咽頭炎', '感染性胃腸炎', '水痘', '手足口病', '伝染性紅斑', '突発性発しん', 'ヘルパンギーナ',
       '流行性耳下腺炎', '不明発しん症', '川崎病', '急性出血性結膜炎', '流行性角結膜炎', '細菌性髄膜炎', '無菌性髄膜炎',
       'マイコプラズマ肺炎', 'クラミジア肺炎(オウム病は除く)', '感染性胃腸炎（ロタウイルス）', 'インフルエンザ入院',
       'インフルエンザ定点', '小児科定点', '眼科定点', '基幹定点', 'インフルエンザ入院定点', 'COVID-19入院定点']

# returns the date of the monday of the associated year and week (e.g. 2024-w49 is 2024-12-02)
def monday_of_calenderweek(year, week):
    first = date(year, 1, 1)
    base = 1 if first.isocalendar()[1] == 1 else 8
    return first + timedelta(days=base - first.isocalendar()[2] + 7 * (week - 1))

# Populate data from df into the data dictionary, according to the ideal structure
def populate_data_from_df(df, data, date_str):

    # The header "Unnamed: 0" represents the disease names
    diseases = df.columns[1:]  # Skip the first column ("Unnamed: 0")

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        ward = row["Unnamed: 0"]  # Get the ward name
        
        for disease in diseases:
            # Initialize disease in the dictionary if not already present
            if disease not in data:
                data[disease] = {}
            
            # Initialize ward in the disease dictionary if not already present
            if ward not in data[disease]:
                data[disease][ward] = []
            
            # Append the date-data pair to the ward
            value = row[disease]
            data[disease][ward].append({date_str: value})
    
    return data

# determine upper bound weeks based on year 
def max_weeks(year):
    max_wk = WKS_UPPER_RANGE_REG_YR_INCL
    if year in SPECIAL_YEARS_WITH_53_WEEKS:
        max_wk = WKS_UPPER_RANGE_SPECIAL_YR_INCL
    elif year == CURRENT_YR:
        max_wk = WKS_UPPER_RANGE_CUR_YR_INCL
    return max_wk

def main():

    # Initialize the dictionary
    data = {}

    # iterate thru all weekly-data-files to create one large master data dictionary
    for year in range(START_YR, CURRENT_YR + 1):

        max_wk = max_weeks(year)
        
        for wk in range(1, max_wk + 1):
            target_filename = str(year) + "_" + str(wk) + ".csv"

            # grab file 
            filepath_list = glob.glob(os.path.join(DATA_SOURCE_DIR, target_filename))
            if len(filepath_list) == 0:  
                print("filepath does not exist for year, wk:", year, wk)
            filepath = filepath_list[0]

            df = pd.read_csv(filepath)

            date_str = str(monday_of_calenderweek(year, wk))

            data = populate_data_from_df(df, data, date_str)

    output_file_path = OUTPUT_DIR + "/master_disease_data.json"

    # Write to JSON file
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

main()