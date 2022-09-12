import numpy as np
from scipy import stats
import pandas as pd
import re
import os

def outlier_removal(path):
    outlier_lst = []
    df_len_lst = []
    regex = r'\d+\w\d+'
    num = re.findall(regex, path)
    df = pd.read_csv(path)
    df = df.drop(columns='Unnamed: 0')
    df_removed = df[(np.abs(stats.zscore(df.weekly_rent)) < 3)]
    outlier_lst.append(len(df) - len(df_removed))
    df_len_lst.append(len(df_removed))
    print(f'{num[0]}: {len(df) - len(df_removed)} ({round((len(df) - len(df_removed))/len(df)*100,2)}%) instances were dropped from {len(df)}, {len(df_removed)} remaining')
    newpath = f'../../data/curated/property_all_no_outlier/' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    df_removed.to_csv(f'../../data/curated/property_all_no_outlier/{num[0]}_property_no_outlier.csv')