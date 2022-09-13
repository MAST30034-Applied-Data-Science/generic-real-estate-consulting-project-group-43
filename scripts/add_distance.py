import openrouteservice as ors
import numpy as np
import time

"""This function accepts a property-place merged csv, and compute the distance/time travelled by car from each property to the parks/schools/stations, 
and to Melbourne Central"""

def add_distance_time(property_place_csv, year):
    client = ors.Client('5b3ce3597851110001cf6248ce6c95ac96814219a4c3a7741f323b73') # philip's api key
    to_place_distances = []
    to_place_times = []
    to_cbd_distances = []
    to_cbd_times = []

    print(f"{len(property_place_csv['SA2_CODE'].unique())} unique SA2 codes")
    for code in property_place_csv['SA2_CODE'].unique():
        locations_coor = []
        sources_index = []
        destinations_index = []
        temp_list1 = []
        temp_list2 = []

        subset = property_place_csv[property_place_csv['SA2_CODE'] == code].reset_index(drop=True)
        count_places = subset['Place_Names'].nunique() # e.g. 10 places for 202021027
        i = 0
        while i < (len(subset) // count_places): # e.g. 210 // 10 = 21 properties for 202021027
            locations_coor.append((subset.iloc[i * count_places]['longitude_ori'], subset.iloc[i * count_places]['latitude_ori'])) # append a tuple of origin long/lat coordinates
            sources_index.append(i) # append origin indices
            i += 1
        
        locations_coor += [ (x[15], x[14]) for x in subset.iloc[:count_places].to_numpy()] # 15 is place longitude, 14 is place latitude, add all places right after property coordinates
        locations_coor += [(144.962379, -37.810454)] # add melbourne central coordinates to the end

        destinations_index += [x for x in range(i, i+count_places+1)] # destination indices right after origin indices, add uptil all places have been added 
        
        print("locations coordinates = ")
        print(locations_coor)
        print("destination index = ")
        print(destinations_index)

        time.sleep(1.5) # wait for 1.5 sec
        # add a try/except here
        # request the distance matrix for each property to all places under current SA2 code
        distance_matrix = ors.distance_matrix.distance_matrix(client=client, locations=locations_coor, 
        profile='driving-car', sources=sources_index, destinations=destinations_index, metrics=['distance', 'duration'])


        to_place_distances += [each for sublist in distance_matrix['distances'] for each in sublist[:-1]]
        to_place_times += [each for sublist in distance_matrix['durations'] for each in sublist[:-1]]
        temp_list1 += [each for sublist in distance_matrix['distances'] for each in sublist[-1:]]  # get the cbd distances
        temp_list2 += [each for sublist in distance_matrix['durations'] for each in sublist[-1:]]  # get the cbd times
        to_cbd_distances += list(np.repeat(temp_list1, count_places))  # repeat N (place count) times for each property to keep the format
        to_cbd_times += list(np.repeat(temp_list2, count_places))

    property_place_csv['dist_to_place_M'] = to_place_distances
    property_place_csv['dist_to_place_KM'] = property_place_csv['dist_to_place_M'] / 1000
    property_place_csv['time_to_place_S'] = to_place_times
    property_place_csv['time_to_place_MIN'] = property_place_csv['time_to_place_S'] / 60
    
    property_place_csv['dist_to_cbd_M'] = to_cbd_distances
    property_place_csv['dist_to_cbd_KM'] = property_place_csv['dist_to_cbd_M'] / 1000
    property_place_csv['time_to_cbd_S'] = to_cbd_times
    property_place_csv['time_to_cbd_MIN'] = property_place_csv['dist_to_cbd_S'] / 60
    
    property_place_csv.to_csv(f'../../data/featured/{year}_distance_rental_place.csv')
    return property_place_csv








"""
import geopy
from geopy.geocoders import GoogleV3
import googlemaps
import re

'''This function takes in a property csv (pandas dataframe) file, and compute distance, time for each property location to Melbourne CBD, using 
the latitude and longitude of each property, and return the imputed csv file'''
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

"""