"""
Objective: python script to download flu data from web crawling 

Target website: https://survey.tmiph.metro.tokyo.lg.jp/epidinfo/csvinfo.do
Target website 1: https://survey.tmiph.metro.tokyo.lg.jp/epidinfo/weeklyhc.do (go here to select year first)
Target website 2: Then, click the above with the selected year (and week), and continuously download from there

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
import platform
import pandas as pd
import glob
from process_japanese_csv import process_to_formatted_csv
import time

DEFAULT_DOWNLOAD_NAME = "csvwzone.csv"

def get_platform_architecture():
    system = platform.system()
    machine = platform.machine()
    
    if system == "Darwin":
        if machine == "arm64":
            return "mac-arm64"
        else:
            return "mac64"
    return "mac64"

def setup_chrome_driver(download_dir):
    chrome_options = Options()
    
    # Create the directory if it doesn't exist
    if not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir)
            print(f"Created download directory: {download_dir}")
        except Exception as e:
            print(f"Error creating directory: {str(e)}")
            raise
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        arch = get_platform_architecture()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"Files will be downloaded to: {download_dir}")
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {str(e)}")
        raise

def wait_for_file(filename, directory, timeout=30):
    """
    Waits for a specific file to appear in a directory.

    :param filename: Name of the file to wait for.
    :param directory: Directory to look for the file.
    :param timeout: Maximum time (in seconds) to wait before raising an exception.
    :return: Full path of the file when it appears.
    :raises TimeoutError: If the file doesn't appear within the timeout period.
    """
    start_time = time.time()
    full_path = os.path.join(directory, filename)
    print(full_path)
    
    while True:
        # Check if the file exists
        if os.path.exists(full_path):
            print(f"File found: {full_path}")
            return full_path
        
        # Check if the timeout has been exceeded
        if time.time() - start_time > timeout:
            raise TimeoutError(f"File did not appear in {directory} within {timeout} seconds.")
        
        # Wait for a short interval before checking again
        time.sleep(1)  # Check every second

# rename the file to yr_wk.csv
def get_last_filename_and_rename(new_filename, download_dir):
    files = glob.glob(os.path.join(download_dir, '*.csv'))
    print(files)
    max_file = max(files, key=os.path.getmtime)
    new_path = os.path.join(download_dir, f"{new_filename}.csv")
    os.rename(max_file, new_path)
    return new_path

def download_data(driver, year, week, download_dir):
    try:
        initial_year = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, "val(year)"))
        )
        Select(initial_year).select_by_value(str(year))

        initial_week = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, "val(week)"))
        )
        Select(initial_week).select_by_value(str(1))

        # click the downloading-link-generator button to generate the JS link to the data source
        intermediate_update_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='更新']"))
        )
        intermediate_update_button.click()

        download_button_to_next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'javascript:document.gocsv.submit();')]"))
        )
        download_button_to_next_page.click()

        # # Wait for and select start year
        # start_year = WebDriverWait(driver, 2).until(
        #     EC.presence_of_element_located((By.NAME, "val(startYear)"))
        # )
        # Select(start_year).select_by_value(str(year))

        # repeat below for each week 
        for wk in range(1, week):

            # Wait for and select start year
            start_year = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.NAME, "val(startYear)"))
            )
            Select(start_year).select_by_value(str(year))

            # Wait for and select end year (same as start year)
            end_year = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.NAME, "val(endYear)"))
            )
            Select(end_year).select_by_value(str(year))
            
            # Wait for and select start week
            start_week = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.NAME, "val(startSubPeriod)"))
            )
            Select(start_week).select_by_value(str(wk))
            
            # Wait for and select end week (same as start week)
            end_week = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.NAME, "val(endSubPeriod)"))
            )
            Select(end_week).select_by_value(str(wk))
            
            # click the downloading-link-generator button to generate the JS link to the data source
            intermediate_download_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='cmd'][value='ダウンロード要求を送信する']"))
            )
            intermediate_download_button.click()

            download_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'javascript:toCsv')]"))
            )
            download_link.click()    

            new_filename = f"{year}_{wk}"

            wait_for_file(DEFAULT_DOWNLOAD_NAME, download_dir)

            print("success in downloading: ", new_filename)

            new_path = get_last_filename_and_rename(new_filename, download_dir)

            wait_for_file(new_filename + ".csv", download_dir)

            print("success in renaming file to:", new_path, new_filename)

            process_to_formatted_csv(new_path, new_filename + ".csv", download_dir)

    except Exception as e:
        print(f"Error selecting date range for Year {year} Week {week}: {str(e)}")     
