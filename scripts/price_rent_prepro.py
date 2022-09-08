import os

def price_prepro(df, type):
    df['price'] = df["price"].str.replace(",","")
    df['price'] = df["price"].str.replace(" ","_") # replacing blank space with underline will simplify code in regex

    regex_str1 = r'([$]?\d+[.]?\d+\w+[.]*\w*[/]*\w*[wW])' # $650.00 per week
    regex_str2 = r'([$]?\d+[.]?\d+$)' # $320
    regex_str3 = r'([$]?\d+[.]?\d+\w+[-]?\w+[d]$)' # $490 Fully Furnished
    regex_str4 = r'([$]?\d+[.]?\d+\w*[*]+\w)' # $750_**SPACIOUS_APARTMENT**

    df['price1']=df['price'].str.extract(regex_str1)
    df['price2']=df['price'].str.extract(regex_str2)
    df['price3']=df['price'].str.extract(regex_str3)
    df['price4']=df['price'].str.extract(regex_str4)

    df['weekly_rent'] = df['price4'].where(df['price4'].notnull(), df['price1'])
    df['weekly_rent'] = df['weekly_rent'].where(df['weekly_rent'].notnull(), df['price2'])
    df['weekly_rent'] = df['weekly_rent'].where(df['weekly_rent'].notnull(), df['price3'])
    df = df.drop(['price1','price2','price3', 'price4'],axis=1)
    df2 = df.dropna(subset = ['weekly_rent'])
    df2['weekly_rent'] = df2['weekly_rent'].str.extract('(\d+)').astype(int)

    df3 = df2[df2['weekly_rent'] > 10000] # drop the yearly rent ones.
    result =  df2[df2['weekly_rent'] < 10000]
    
    #print(f'{len(df) - len(df2)} instances were dropped as no weekly rent was demonstrated')
    #print(f'{len(df3)} instances were dropped as it was annual rent')
    return result 
    newpath = f'../../data/curated/{type}/' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    result.to_csv(f'../../data/curated/{type}/API_re_clean.csv')
