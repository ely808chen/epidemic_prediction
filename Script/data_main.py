"""
Main file to scrape data and process to readable csv file. 

Data Source: https://survey.tmiph.metro.tokyo.lg.jp/epidinfo/weeklyhc.do

The script (1) scrapes all epidemic data from a website (via clicking csv download button)
for each selected year and (2) process the raw data to make it readable. 

Output: Weekly epidemic data in csv format during the selected years 

Usage: 
(1) Select start_year, the year that you want to start downloading (weeks does not matter)
(2) Select End_Year, presumably the current year 
(3) Change WKS_UPPER_RANGE_CUR_YR_INCL, the most recent wk number 
(4) Simply run main() 
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import platform
import pandas as pd
import glob
from crawling import setup_chrome_driver, download_data

DOWNLOAD_DIR = "/Users/elychen/Desktop/code_personal_project/epidemic_prediction/Data/tokyo_infectious_disease_data"
END_DIR = DOWNLOAD_DIR
TARGET_URL = "https://survey.tmiph.metro.tokyo.lg.jp/epidinfo/weeklyhc.do"

SPECIAL_YEARS_WITH_53_WEEKS = [2004, 2009, 2015, 2020]
WKS_UPPER_RANGE_SPECIAL_YR_INCL = 53  
WKS_UPPER_RANGE_REG_YR_INCL = 52
WKS_UPPER_RANGE_CUR_YR_INCL = 49  #### TO DO: CHANGE THIS VAL ACC TO NEEDS ####
START_YEAR = 2024  #### TO DO: CHANGE THIS VAL ACC TO NEEDS ####
END_YEAR = 2024  #### TO DO: CHANGE THIS VAL ACC TO NEEDS ####

# retrieves raw data from crawling thru data webpage, downloading raw data in the data directory
def main():
    try:

        for year in range(START_YEAR, END_YEAR + 1):

            download_dir = DOWNLOAD_DIR
            driver = setup_chrome_driver(download_dir)
        
            url = TARGET_URL
            driver.get(url)

            week_upper_range_incl = None
            if year in SPECIAL_YEARS_WITH_53_WEEKS:
                week_upper_range_incl = WKS_UPPER_RANGE_SPECIAL_YR_INCL
            elif year == END_YEAR:
                week_upper_range_incl = WKS_UPPER_RANGE_CUR_YR_INCL
            else:
                week_upper_range_incl = WKS_UPPER_RANGE_REG_YR_INCL

            download_data(driver, year, week_upper_range_incl + 1, download_dir)

        time.sleep(1)
        
        print("All downloads completed!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()   
    
main()