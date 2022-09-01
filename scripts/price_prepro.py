import pandas as pd
import numpy as np
import re
def prepro_price(file_path, method):
    df = pd.read_csv(file_path)
    lst = []
    for i in range(len(df)):
        price = df['price'].iloc[i].split(" ")
        lst.append(price)
    #print(lst[0:5]) 

    valid_price_lst = []
    for pricelst in lst:
        valid_price = [price for price in pricelst if ("$" in price)] # some data demonstrated two rent price e.g "$680PW, $2955.00PCM"
        valid_price_lst.append(valid_price)                           # thus we will keep both $values and drop the montly one 
    one_price_lst = []
    for price_lst in valid_price_lst:
        if price_lst:
            one_price_lst.append(price_lst[0]) # we assume that the weekly rent value will always present first
        else:
            one_price_lst.append("")
    one_price_lst
    #print(one_price_lst[0:5])
    print(f'the price list containing the weekly rent is of length {len(one_price_lst)}')

    price_num_lst = []
    for price in one_price_lst:
        if "." in price:
            price = price[:price.index(".")] # convert $450.00 and $450.99 to $450
        if "/" in price:
            price = price[:price.index("/")] # some price has no space "$690pw/$2998pcm", we slice out the later part
        if "-" in price:
            price = price[:price.index("-")] # some price looks like "$160-$200 weekly", we assume rent is the first price
        if price.count("$") == 2:
            price = price[:price.rindex("$")]# some price looks like "$425pw$1,847pcm", we slice out the later part starting with $
        price=''.join(char for char in price if char.isdigit()) # keep numbers only drop other illustration words
        if price:
            price = int(price)
            price_num_lst.append(price)
        else:
            price = np.nan # some rental price consists word only "contact manager", thus we make them as nan and drop later
            price_num_lst.append(price)
    #print(price_num_lst[0:5])
    #print(f'the price list containing the weekly rent is of length {len(price_num_lst)}')

    df['weekly_rent'] = price_num_lst
    df2 = df.dropna(subset=['weekly_rent'])
    print(f'{len(df) - len(df2)} data was dropped as no rental price was demonstrated')
    df2.to_csv(f'../data/curated/{method}_clean_price.csv')