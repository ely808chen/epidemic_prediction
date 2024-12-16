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
WKS_UPPER_RANGE_CUR_YR_INCL = 49
START_YEAR = 2003
END_YEAR = 2024

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