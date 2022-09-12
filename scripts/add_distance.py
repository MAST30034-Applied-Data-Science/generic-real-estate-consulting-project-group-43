import geopy
from geopy.geocoders import GoogleV3
import googlemaps
import re

"""This function takes in a property csv (pandas dataframe) file, and compute distance, time for each property location to Melbourne CBD, using 
the latitude and longitude of each property, and return the imputed csv file"""
def add_distance_time(property_csv):
    # convert to dict for faster computation
    #property_dict = property_csv[['latitude', 'longitude', 'street_address']].to_dict('records')
    property_list = property_csv[['latitude', 'longitude', 'street_address']].to_numpy()
    pattern = re.compile(r'\d+.?\d?') # get only numeric distance or time value
    destination_latitude, destination_longitude = -37.810454, 144.962379 # melbourne central latitude and longitude
    gmaps = googlemaps.Client(key='some API') # Philip's api, please don't overuse
    driving_distance_list_km = []
    driving_time_list_secs = []
    walking_distance_list_km = []
    walking_time_list_secs = []        
    i=0
    while i < len(property_list):
        print(f"Row {i}, location {property_list[i][2]}")

        if(i+25 < len(property_list)):
            origins = [str(origin[0])+" "+str(origin[1]) for origin in property_list[i:i+25]]
        else:
            origins = [str(origin[0])+" "+str(origin[1]) for origin in property_list[i:len(property_list)]]
            
        driving_distance_matrix = gmaps.distance_matrix(origins, [str(destination_latitude) + " " + str(destination_longitude)], mode='driving')
        walking_distance_matrix = gmaps.distance_matrix(origins, [str(destination_latitude) + " " + str(destination_longitude)], mode='walking')
        
        # individual batch of 25 values
        driving_distance_km = [float(pattern.findall(x['elements'][0]['distance']['text'])[0]) for x in driving_distance_matrix['rows']]
        driving_time_sec = [int(x['elements'][0]['duration']['value']) for x in driving_distance_matrix['rows']]
        walking_distance_km = [float(pattern.findall(x['elements'][0]['distance']['text'])[0]) for x in walking_distance_matrix['rows']]
        walking_time_sec = [int(x['elements'][0]['duration']['value']) for x in walking_distance_matrix['rows']]

        # store batches to corresponding list
        driving_distance_list_km += driving_distance_km
        driving_time_list_secs += driving_time_sec
        walking_distance_list_km += walking_distance_km
        walking_time_list_secs += walking_time_sec

        i += 25
    property_csv['dri_dist_km'] = driving_distance_list_km
    property_csv['dri_time_sec'] = driving_time_list_secs
    property_csv['dri_time_min'] = property_csv['dri_time_sec'] / 60
    property_csv['walk_dist_km'] = walking_distance_list_km
    property_csv['walk_time_sec'] = walking_time_list_secs
    property_csv['walk_time_min'] = property_csv['walk_time_sec'] / 60
    
    return property_csv