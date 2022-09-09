import pandas as pd
import os
import sys
import re
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../../scripts/')
import price
from price import price_prepro

def prepro(path, type):
    regex = r'\d+\w\d+'
    num = re.findall(regex, path)
    df = pd.read_csv(path)
    df.dates = pd.to_datetime(df.historical_dates)
    df['suburb'] = df.address.str.split(" ").str[-1]
    df.ncar.replace(to_replace=['none'], value=0, inplace=True)
    df = df.drop(columns = "Unnamed: 0")
    df = df.rename(columns={"historical_prices":'price'})
    result = price_prepro(df,type)
    newpath = f'../../data/curated/{type}/' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    result.to_csv(f'../../data/curated/historical/{num[0]}_{type}_1st_clean.csv')