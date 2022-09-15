from http import client
from operator import index
import openrouteservice as ors
import numpy as np
import time

"""This function accepts a property-place merged csv, and compute the distance/time travelled by car from each property to the parks/schools/stations, 
and to Melbourne Central"""

def add_distance_time(property_place_csv, year, client, mode):
    #client = ors.Client('5b3ce3597851110001cf6248ce6c95ac96814219a4c3a7741f323b73') # Phikho-caz's api key 2500
    to_place_distances = []
    to_place_times = []
    to_cbd_distances = []
    to_cbd_times = []

    for code in property_place_csv['SA2_CODE'].unique():  # loop through SA2 Code
        print(f"Executing SA2 Code {code}", flush=True)
        time.sleep(0.2)
        locations_coor = []
        sources_index = []
        destinations_index = []

        subset = property_place_csv[property_place_csv['SA2_CODE'] == code].reset_index(drop=True)
        count_places = len(subset.drop_duplicates(subset=['Place_Names','latitude_des'])) # make sure places are unique, e.g. 10 places for 202021027
        print(f"Subset size = {len(subset)}, Places count = {count_places}, Property count = {len(subset) // count_places}", flush=True)
        time.sleep(0.2)
        i = 0
        while i < (len(subset) // count_places): # e.g. 210 // 10 = 21 properties for 202021027
            locations_coor.append((subset.iloc[i * count_places]['longitude_ori'], subset.iloc[i * count_places]['latitude_ori'])) # append a tuple of origin long/lat coordinates
                                                                                                                                   # of each property (once)
            sources_index.append(i) # append origin indices
            i += 1
        
        locations_coor += [ (x[15], x[14]) for x in subset.iloc[:count_places].to_numpy()] # 15 is place longitude, 14 is place latitude, add all places right after property coordinates
        locations_coor += [(144.962379, -37.810454)] # add melbourne central coordinates to the end

        destinations_index += [x for x in range(i, i+count_places+1)] # destination indices right after origin indices, add uptil all places have been added 
        
        #print("locations coordinates = ", flush=True)
        #time.sleep(0.5) # wait for 1.3 sec
        #print(locations_coor, flush=True)
        #time.sleep(0.5) # wait for 1.3 sec
        #print("destination index = ", flush=True)
        #time.sleep(0.5) # wait for 1.3 sec
        #print(destinations_index, flush=True)
        #time.sleep(0.5) # wait for 1.3 sec
        # Less than the maximum allowed routes in one request, normal execution
        if (i * (count_places+1) < 3500):
            temp_list1 = [] # temporary lists to store unique to cbd distance
            temp_list2 = [] # temporary lists to store unique to cbd time
            try:
                # add a try/except here
                # request the distance matrix for each property to all places under current SA2 code
                distance_matrix = ors.distance_matrix.distance_matrix(client=client, locations=locations_coor, 
                profile='driving-car', sources=sources_index, destinations=destinations_index, metrics=['distance', 'duration'])
                time.sleep(2.3)
                
                matrix_checker = [each for sublist in distance_matrix['distances'] for each in sublist[:-1]]
                # new matrix must have same length as the subset each time
                if (len(matrix_checker) == len(subset)):
                    to_place_distances += matrix_checker
                    to_place_times += [each for sublist in distance_matrix['durations'] for each in sublist[:-1]]
                    temp_list1 += [each for sublist in distance_matrix['distances'] for each in sublist[-1:]]  # get the cbd distances
                    temp_list2 += [each for sublist in distance_matrix['durations'] for each in sublist[-1:]]  # get the cbd times
                    to_cbd_distances += list(np.repeat(temp_list1, count_places))  # repeat N (place count) times for each property to keep the format
                    to_cbd_times += list(np.repeat(temp_list2, count_places))
                    print(f"To Place Distance Grand List, Normal Branch, length = {len(to_place_distances)}", flush=True)
                    #time.sleep(2.5)
                    #print(to_place_distances)
                    #print(f"To CBD Distance Grand List, Normal Branch, length = {len(to_cbd_distances)}")
                    #print(to_cbd_distances)
                
                else:
                    print(f"Normal branch failed to match dimension due to random error, matrix size = {len(matrix_checker)}")
                    # dimension unmatched due to random error
                    to_place_distances += [0 for i in range(len(subset))]
                    to_place_times += [0 for i in range(len(subset))]
                    to_cbd_distances += [0 for i in range(len(subset))]
                    to_cbd_times += [0 for i in range(len(subset))]     
                                               
            except:
                to_place_distances += [0 for i in range(len(subset))]
                to_place_times += [0 for i in range(len(subset))]
                to_cbd_distances += [0 for i in range(len(subset))]  # repeat N (place count) times for each property to keep the format
                to_cbd_times += [0 for i in range(len(subset))]
                client = ors.Client('5b3ce3597851110001cf6248ce6c95ac96814219a4c3a7741f323b73') # Phikho-caz's api key 2500
                print('Quota Exceeded daily limit or (less than 3500 branch) timeout')
        
        else:
            # iteratively cut into sublists to make requests
            j = 0
            factor = i*(count_places+1) // 3500  # assumes it's properties that exceed by a factor, so reduce them
            slicer = i // (factor+1)
            while (j < factor+1):
                temp_list1 = [] # temporary lists to store sliced lists of unique to cbd distance, reset at each iteration
                temp_list2 = [] # temporary lists to store sliced lists of unique to cbd time, reset at each iteration
                if (j==factor):
                    partial_sources_index = sources_index[j*slicer:i] # from the last slicer to the end (of source)
                else:
                    partial_sources_index = sources_index[j*slicer:(j+1)*slicer] # slice in between
                
                try:
                    distance_matrix = ors.distance_matrix.distance_matrix(client=client, locations=locations_coor, 
                    profile='driving-car', sources=partial_sources_index, destinations=destinations_index, metrics=['distance', 'duration'])
                    time.sleep(2.3)
                    
                    #print("partial sources index = ", flush=True)
                    #time.sleep(0.5) # wait for 1.3 sec
                    #print(partial_sources_index, flush=True)
                    #time.sleep(0.5) # wait for 1.3 sec
                    #print("destination index = ", flush=True)
                    #time.sleep(0.5) # wait for 1.3 sec
                    #print(destinations_index, flush=True)
                    #time.sleep(0.5) # wait for 1.3 sec                    
                    
                    matrix_checker = [each for sublist in distance_matrix['distances'] for each in sublist[:-1]]
                    if (len(matrix_checker) == slicer*count_places or len(matrix_checker) == (i-j*slicer)*count_places):
                        to_place_distances += matrix_checker
                        to_place_times += [each for sublist in distance_matrix['durations'] for each in sublist[:-1]]
                        temp_list1 += [each for sublist in distance_matrix['distances'] for each in sublist[-1:]]  # get the cbd distances
                        temp_list2 += [each for sublist in distance_matrix['durations'] for each in sublist[-1:]]  # get the cbd times
                        to_cbd_distances += list(np.repeat(temp_list1, count_places))  # repeat N (place count) times for each property to keep the format
                        to_cbd_times += list(np.repeat(temp_list2, count_places))
                        print(f"To Place Distance Grand List, Slice Branch, length = {len(to_place_distances)}", flush=True)
                        #time.sleep(2.5)
                        #print(to_place_distances)
                        #print(f"To CBD Distance Grand List, Slice, Branch, length = {len(to_cbd_distances)}")
                        #print(to_cbd_distances)   

                    # dimension unmatched due to random error
                    else:
                        print(f"Slice branch failed to match dimension due to random error, matrix size = {len(matrix_checker)}")
                        to_place_distances += [0 for i in range(len(partial_sources_index) * count_places)]
                        to_place_times += [0 for i in range(len(partial_sources_index) * count_places)]
                        to_cbd_distances += [0 for i in range(len(partial_sources_index) * count_places)]
                        to_cbd_times += [0 for i in range(len(partial_sources_index) * count_places)]    
                    
                    j += 1
                except:
                    to_place_distances += [0 for i in range(len(partial_sources_index) * count_places)]
                    to_place_times += [0 for i in range(len(partial_sources_index) * count_places)]
                    to_cbd_distances += [0 for i in range(len(partial_sources_index) * count_places)]
                    to_cbd_times += [0 for i in range(len(partial_sources_index) * count_places)]
                    client = ors.Client('5b3ce3597851110001cf6248ce6c95ac96814219a4c3a7741f323b73') # Phikho-caz's api key 2500
                    print('Quota Exceeded daily limit or (greater than 3500 branch) timeout')

    csv_copy = property_place_csv.copy(deep=True)

    csv_copy['dist_to_place_M'] = to_place_distances
    csv_copy['dist_to_place_KM'] = csv_copy['dist_to_place_M'] / 1000
    csv_copy['time_to_place_S'] = to_place_times
    csv_copy['time_to_place_MIN'] = csv_copy['time_to_place_S'] / 60
    
    csv_copy['dist_to_cbd_M'] = to_cbd_distances
    csv_copy['dist_to_cbd_KM'] = csv_copy['dist_to_cbd_M'] / 1000
    csv_copy['time_to_cbd_S'] = to_cbd_times
    csv_copy['time_to_cbd_MIN'] = csv_copy['time_to_cbd_S'] / 60
    
    if (mode == 'saving'):
        csv_copy.to_csv(f'../../data/featured/{year}_distance_rental_place.csv', index=False)
    return csv_copy








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