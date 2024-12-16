import os
import time
import platform
import pandas as pd
import glob

DOWNLOAD_DIR = "/Users/elychen/Desktop/code_personal_project/epidemic_prediction/Data/tokyo_infectious_disease_data"

SPECIAL_YEARS_WITH_53_WEEKS = [2004, 2009, 2015, 2020]
WKS_UPPER_RANGE_SPECIAL_YR_INCL = 53
WKS_UPPER_RANGE_REG_YR_INCL = 52
WKS_UPPER_RANGE_CUR_YR_INCL = 49

df = pd.read_csv(DOWNLOAD_DIR + "/" + "2018_24.csv")
print(df["インフルエンザ定点"])
