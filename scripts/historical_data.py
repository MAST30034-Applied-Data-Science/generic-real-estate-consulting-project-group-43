import pandas as pd
import os
import sys
import re
from pandas import to_numeric
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../../scripts/')
import price
from price import price_prepro

def prepro(path, type):
    regex = r'\d+\w\d+'
    num = re.findall(regex, path)
    df = pd.read_csv(path)
    df.dates = pd.to_datetime(df.historical_dates)
    df['year'] = df.dates.dt.year # add year column
    df['month'] = df.dates.dt.month # add month column
    df['suburb'] = df.address.str.split(" ").str[-1] # add a suburb column for each instance
    df.ncar.replace(to_replace=['none'], value=0, inplace=True) # car space 'none' -> 0
    df = df[(df.nbed != 'none') & (df.nbath != 'none') ] # drop columns with no number of bedrooms or bathrooms
    df = df.drop(columns = "Unnamed: 0") # drop useless columns
    df = df.drop_duplicates() # drop duplicates occurred due to web scraping
    df = df.rename(columns={"historical_prices":'price'})
    result = price_prepro(df,type)
    newpath = f'../../data/curated/{type}/' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    result.to_csv(f'../../data/curated/historical/{num[0]}_{type}_1st_clean.csv')