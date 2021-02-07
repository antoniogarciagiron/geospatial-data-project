import requests
import json
import os
import pandas as pd
from functools import reduce
import operator
import geopandas as gpd
from cartoframes.viz import Map, Layer, popup_element
import geopy.distance
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster


def geocode(where, geocode_token):
    '''Takes the name of a place to fint the coordinates and a token from GeoCode, and returns a dictionary item with the Name of the city and the longitude and latitude
    Takes: city and API token
    Returns: the dictionary with the place coordinates
    '''
    data = requests.get(f"https://geocode.xyz/{where}?json=1&auth={geocode_token}")
    city = data.json()
    city_data={}
    city_data["city"] = where
    city_data["longitude"] = city.get('longt')
    city_data["latitude"] = city.get('latt')
    return city_data


def find_list_foursquare(city, looking_for, tok1, tok2, limit):
    '''Takes the coordinates of a city, previously obtained from Geocode, if possible and a key with the kind of place you are looking for, for example, "Restaurant", "Coffee"...
    and looks into Foursquare API to get the list of places in the selected location
    Takes: city coordinates, key with the place you want
    Returns: a json file containing information of places in a selected location
    '''
    url_query = 'https://api.foursquare.com/v2/venues/explore'

    parameters = {"client_id" : tok1,
                  "client_secret" : tok2,
                  "v": "20180323",
                  "ll": f"{city.get('coordinates')[0]},{city.get('coordinates')[1]}",
                  "query":f"{looking_for}",
                  "limit": limit  
                 }
    resp = requests.get(url= url_query, params=parameters)
    data = json.loads(resp.text)
    return data


def getFromDict(dictio,maps):
    '''Obtains information from a json 
    Takes: the json and the path to reach the information you are looking for
    Returns: the value from the json/path
    '''
    return reduce (operator.getitem,maps,dictio)


def get_coordinates_from_list(data):    
    '''From the json downloaded with the Foursquare API, it takes a list with dictionaries containing the name of the place and the coordinates
    Takes: a json from Foursquare
    Returns: a list with dictionaries containing the name and coordinates of the places
    '''
    level_1 = data.get("response")
    level_2 = level_1.get("groups")[0]
    level_3 = level_2.get("items")
    m_name = ["venue","name"]
    m_latitude = ["venue","location","lat"]
    m_longitude = ["venue","location","lng"]
    final_list = []
    for dic in level_3:
        element = {}
        element["name"] = getFromDict(dic,m_name)
        element["latitude"] = getFromDict(dic,m_latitude)
        element["longitude"] = getFromDict(dic,m_longitude)
        final_list.append(element)
    return final_list


def create_table(final_list):
    '''Transforms the list with names and coordinates into a dataframe with a column containing GeoDataframe values, in order to plot the places in CartoFrames
    Takes: a list of places and their coordinates
    Returns: a dataframe
    '''
    table = pd.DataFrame(final_list)
    gdf = gpd.GeoDataFrame(table, geometry = gpd.points_from_xy(table.longitude,table.latitude))
    return gdf


def only_cords(place):
    '''Gets the coordinates from a list with place, latitude and longitude
    Takes: a dictionary containing latitude and longitude
    Returns: a list with latitude and longitude
    '''
    lat = place.get('latitude')
    long = place.get('longitude')
    return [lat, long]


def all_combinations(final_list_1, final_list_2, final_list_3, final_list_4):
    '''Takes 4 sets with places and their coordinates, extracts the coordinates and creates a list of lists with the coordinates 
    for all the possible combinations containing one place from each original set
    Takes: 4 sets of places and their coordinates
    Returns: a list with all the possible combinations
    '''
    polygon = []
    for place_1 in final_list_1:
        c_1 = only_cords(place_1)
        for place_2 in final_list_2:
            c_2 = only_cords(place_2)
            for place_3 in final_list_3:
                c_3 = only_cords(place_3)
                for place_4 in final_list_4:
                    c_4 = only_cords(place_4)
                    set_distances = [c_1, c_2, c_3, c_4]
                    polygon.append(set_distances)
    return polygon


def get_optimal_combination(polygon):
    '''It takes a list with combinations of the coordinates of 4 places, calculates the 6 distances separating the 4 places (i.e, the perimeter and 2 diagonals) and sums them
    If the sum is smaller than the counter it saves the value and the coordinates of the 4 places
    When it finishes it returns the optimal combination of places withing smaller distance
    Takes: 4 sets of places and their coordinates
    Returns: a list with all the possible combinations
    '''
    min_distance = 40075000
    for group in polygon:
        dist1 = geopy.distance.geodesic(group[0],group[1]).meters
        dist2 = geopy.distance.geodesic(group[0],group[2]).meters
        dist3 = geopy.distance.geodesic(group[0],group[3]).meters
        dist4 = geopy.distance.geodesic(group[1],group[2]).meters
        dist5 = geopy.distance.geodesic(group[1],group[3]).meters
        dist6 = geopy.distance.geodesic(group[3],group[2]).meters

        dist = dist1 + dist2 + dist3 + dist4 + dist5 + dist6 
        separation = dist
        if separation < min_distance:
            min_distance = separation
            closer_places = group
    return closer_places

def get_centroid_place(closer_places):
    lat=0
    long=0
    for place in closer_places:
        lat += place[0]
        long += place[1]
    lat = lat/len(closer_places)
    long = long/len(closer_places)
    return [lat, long]