# epidemic_prediction

Data Source: https://survey.tmiph.metro.tokyo.lg.jp/epidinfo/weeklyhc.do

File Usage:

(1) run data_main.py to download all raw data via web scraping  
(2) run disease_data_to_single_file.py to consolidate all raw data into a single master JSON file
(3) run flatten_json.py to generate new JSON file that has the flattened version of the above JSON file
(4) run sliding_window.py to generate new csv file that has the sliding_windowed SD and Mean data
for each ward for each disease
