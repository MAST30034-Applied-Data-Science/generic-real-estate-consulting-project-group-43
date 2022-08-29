import requests
import json
from bs4 import BeautifulSoup
from csv import writer

client_id = 'client_1e4da44af583b72acc2aae9f28fb6a5a'
client_secret = 'secret_9283eb6fb4b36255c9909351999d742d'
scopes = ['api_listings_read']
auth_url = 'https://auth.domain.com.au/v1/connect/token'
url_endpoint = 'https://api.domain.com.au/v1/listings/residential/_search'

# def get_property_info():
#     response = requests.post(auth_url, data = {
#                         'client_id':client_id,
#                         'client_secret':client_secret,
#                         'grant_type':'client_credentials',
#                         'scope':scopes,
#                         'Content-Type':'text/json'
#                         })
#     json_res = response.json()
#     access_token=json_res['access_token']
#     print(access_token)
#     auth = {'Authorization':'Bearer ' + access_token}
#     url = url_endpoint
#     res1 = requests.get(url, headers=auth)    
#     r = res1.json()
#     print(r)
# get_property_info()

response = requests.post(auth_url, data = {
                        'client_id':client_id,
                        'client_secret':client_secret,
                        'grant_type':'client_credentials',
                        'scope':scopes,
                        'Content-Type':'text/json'
                        })
json_res = response.json()
access_token=json_res['access_token']
print(access_token)
auth = {'Authorization':'Bearer ' + access_token}
url = url_endpoint

areas = ["Melbourne City Council - Greater Area",
                  "Port Philip City Council - Greater Area",
                  "Stonnington City Council - Greater Area",
                  "Yarra City Council - Greater Area"]

post_fields = {
      "listingType":"Rent",
      "pageSize":200,
      "propertyTypes":"",
      "minBedrooms":1,
      "minBathrooms":1,
      "maxPrice": 400,
      "sort": {
          "sortKey": "Default"
      },
      "locations":[
        {
          "state":"VIC",
          "region":"",
          "area":areas[3],
                  
          "suburb":"",
          "postCode":"",
          "includeSurroundingSuburbs":False
        }
      ]
}

# Request content
res1 = requests.post(url,headers=auth,json=post_fields)
print(res1)
content = json.loads(res1.text)
len(content)

# # reset csv
# header = ['Address', 'Suburb', 'Postcode', 'Area', 'Type', 'Bed', 'Bath', 'Car', 'Price']
# f = open('listings.csv', 'w')
# thewriter = writer(f)
# thewriter.writerow(header)

# Get request for each property ID and extract attributes
for i in content:
    # id = str(i['listing']['id'])
    # url = "https://api.domain.com.au/v1/listings/"+ id
    # auth = {"Authorization":"Bearer "+access_token}
    # request = requests.get(url,headers=auth)
    # r=request.json()

    #get details
    # address_parts=r['addressParts']
    # street_address=address_parts['streetNumber'] + " " + address_parts['street']
    # suburb=address_parts['suburb']
    # postcode=da['postcode']
    # property_type=r['propertyTypes'][0]
    # bathrooms=r['bathrooms']
    # bedrooms=r['bedrooms']
    # carspaces=r['carspaces']
    # price=r['priceDetails']['displayPrice'][1:4]
    
    #get details
    r = i['listing']['propertyDetails']
    street_address=r['displayableAddress']
    suburb=r['suburb']
    postcode=r['postcode']
    area=r['area']
    property_type=r['propertyType']
    bathrooms=r['bathrooms']
    bedrooms=r['bedrooms']
    
    if(str(i).find('carspaces'))>0:
        carspaces=i['listing']['propertyDetails']['carspaces']
    else:
        carspaces=0
    
    price=i['listing']['priceDetails']['displayPrice'][1:4]
    
    print(street_address, suburb, postcode, area, property_type, bedrooms, bathrooms, carspaces, price)
    info = [street_address, suburb, postcode, area, property_type, bedrooms, bathrooms, carspaces, price]
    
    with open('listings.csv', 'a', newline='') as g:
        thewriter = writer(g)        
        thewriter.writerow(info)

