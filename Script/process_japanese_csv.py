import pandas as pd 
import glob 
import os
import csv 

import pandas as pd

def process_to_formatted_csv(csv_file, new_filename, download_dir):

    # Define your column names
    col_names_default = [
        "インフルエンザ", "新型コロナウイルス感染症（COVID-19）", "RSウイルス感染症", "咽頭結膜熱", "Ａ群溶血性レンサ球菌咽頭炎", "感染性胃腸炎", "水痘", "手足口病",
        "伝染性紅斑", "突発性発しん", "ヘルパンギーナ", "流行性耳下腺炎", "不明発しん症", "川崎病", "急性出血性結膜炎", "流行性角結膜炎", "細菌性髄膜炎",
        "無菌性髄膜炎", "マイコプラズマ肺炎", "クラミジア肺炎(オウム病は除く)", "感染性胃腸炎（ロタウイルス）", "インフルエンザ入院", "COVID-19入院",
        "インフルエンザ定点", "小児科定点", "眼科定点", "基幹定点", "インフルエンザ入院定点", "COVID-19入院定点"
    ]

    # Step 1: Identify starting line for the actual data
    start_linenum = None
    with open(csv_file, encoding="shift_jis") as f:
        rows = 0
        for i, line in enumerate(f):
            rows += 1
            if "男女合計" in line:  # Adjust this keyword as necessary
                start_linenum = rows
                break
    
    col_names = None
    # Extract the column names from the next line
    if start_linenum is not None:
        with open(csv_file, encoding="shift_jis") as f:
            for i, line in enumerate(f):
                if i == start_linenum+1:  # The row immediately after start_linenum
                    col_names = line.strip().split(",")  # Split by comma to extract columns
                    break

    # Raise an error if column names couldn't be found
    if not col_names:
        raise ValueError("Could not extract column names from the file.")
    
    # clean the column names
    clean_col_names = [col.strip('"') for col in col_names if col.strip('"')]

    print(clean_col_names)

    In, not_in = 0,0
    for col_n in col_names_default:
        if col_n in clean_col_names:
            In += 1
        else:
            not_in += 1
    print(In, not_in)

    # Read the CSV file, skipping unwanted rows (81 rows of header data)
    # df = pd.read_csv(csv_file, encoding="shift_jis", header=81, names=col_names, engine='python', sep=',')
    # df = pd.read_csv(csv_file, encoding="shift_jis", header=start_linenum, names=col_names, engine='python', sep=',')
    df = pd.read_csv(csv_file, encoding="shift_jis", header=0, skiprows=start_linenum, names=clean_col_names, engine='python', sep=',')

    df.to_csv(download_dir + "/" + new_filename)

