import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests import get
import re
import pickle
import os

def get_urls_daily(start, end):
    with open("HIS_url_links", "rb") as fp:
        result_urls = pickle.load(fp)
    result_urls_partial = result_urls[start:end]
    houses = []
    posts = []
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"}

    for i in range(len(result_urls_partial)):
        soup = BeautifulSoup(requests.get(result_urls_partial[i], headers=headers).text, 'html.parser')
        # in the html of the page, find all the bins with <li> and class:
        print(f'{i}.getting data from {result_urls_partial[i]}')
        house_data = soup.find_all("div", {"class":re.compile("property (odd|even) clearfix")})
        regex = r'(\d{4})'
        post = re.findall(regex, result_urls_partial[i])
        # random wait times
        value = random()
        scaled_value = 1 + (value * (9 - 5))
        # print(scaled_value)
        time.sleep(scaled_value)

        # no need this
        #for link in result_urls_partial:
        #    post = re.findall(regex, link)
        #    postcode = post[0][0:4]

        houses.extend(house_data)
        for c in range(len(house_data)):
            posts.append(post)
        
        
    count = 0
    data = pd.DataFrame()
    first = True

    count_p = 0
    for num in houses:
        # getting the price: make sure to test this code a few times by itself to understand exactly which parameters will work 
        current_priceTag = num.find_all('section', {"class":"grid-35 tablet-grid-35 price"})
        priceSection = num.find_all('section',{"class":"grid-100 historical-price"})
        priceTags = []
        rent_prices = []
        rent_dates = []

        try:
            current_price = re.search(r'\<h3\>(.*)\<\/h3\>', str(current_priceTag))
            current_date = re.search(r'\:[ ](.*)\<\/span\>', str(current_priceTag))
            rent_prices.append(current_price.group(1))
            rent_dates.append(current_date.group(1))
        except:
            print("Current rent value exception")

        priceTags = priceSection[0].find_all('li')
        for ps in priceTags:
            try:
                rent = re.search(r'\<\/span\>(.*)\<\/li\>', str(ps))
                rent_prices.append(rent.group(1))
                date = re.search(r'\<span\>(.*)\<\/span\>', str(ps))
                rent_dates.append(date.group(1))
            except:
                print("Historical values exception")

        try:
            lat = re.search(r'data\-lat\=\"(.*\d)\"[ ]', str(num)) 
            lng = re.search(r'data\-lng\=\"(.*\d)\"\>', str(num)) 
            latitude = lat.group(1)
            longitude = lng.group(1)
        except:
            print("Location values exception")

        try:
            nbed = num.find_all('p', {"class": "property-meta bed"})[0].text
            nbed = re.search(r'[A-Za-z][ ]:[ ](.*)', nbed).group(1)
        except IndexError:
            nbed = 'none'
        try:
            nbath = num.find_all('p', {"class": "property-meta bath"})[0].text
            nbath = re.search(r'[A-Za-z][ ]:[ ](.*)', nbath).group(1)
        except IndexError:
            nbath = 'none'
        try:
            ncar = num.find_all('p', {"class": "property-meta car"})[0].text
            ncar = re.search(r'[A-Za-z][ ]:[ ](.*)', ncar).group(1)
        except IndexError:
            ncar = 'none'
        try:
            type = num.find_all('p', {"class": "property-meta type"})[0].text
            type = re.search(r'[A-Za-z][ ]:[ ](.*)', type).group(1)
        except IndexError:
            type = 'none'
        try:
            address = num.find_all('h2', {"class":"address"})[0].text
        except IndexError:
            address = 'none'

        for z in zip(rent_prices, rent_dates):
            d = {"address":[address], "latitude":[latitude], "longitude":[longitude], 
                "nbed":[nbed], "nbath":[nbath], "ncar":[ncar], "historical_prices":[z[0]], 
                "type":[type],
                "historical_dates":[z[1]],
                "postcode":posts[count_p]}

            if first:
                first = False
                data = pd.DataFrame.from_dict(d)
            else:
                data = pd.concat([data, pd.DataFrame.from_dict(d)])

        count_p += 1
    print(data.head(10))
    data.to_csv(f'../../data/raw/historical_data/{start}_{end}_historical.csv')