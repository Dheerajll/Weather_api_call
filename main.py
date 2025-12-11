from requests import get,post
from datetime import datetime
from dotenv import load_dotenv
import os
from pprint import pprint
load_dotenv() # os.getenv("") to get the env variable

def get_utc(iso_time):
    return(datetime.fromisoformat(iso_time).time())
           
def get_lat_lon(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    city_name_unspaced = city_name.replace(" ","")
    params = {
        'name': city_name,
        'count':1
    }
    response = get(url,params=params)
    response_json = response.json()
    results=response_json["results"][0]
    lat = results["latitude"]
    lon = results["longitude"]
    return lat,lon

def get_weather(city_name):
    lat,lon = get_lat_lon(city_name)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude':lat,
        'longitude':lon,
        'daily':["sunrise","sunset","temperature_2m_max","temperature_2m_min","uv_index_max"],
        'hourly':["temperature_2m","relative_humidity_2m"],
        'current':["temperature_2m","relative_humidity_2m","rain"],
        'timezone': "auto"
    }
    response = get(url,params=params)
    response_json = response.json()
    result =response_json
    #pprint(result)
    weather_info = {
        "Temperature":" ".join(map(str,[result["current"]["temperature_2m"],result["current_units"]["temperature_2m"]])),
        "Humidity":" ".join(map(str,[result["current"]["relative_humidity_2m"],result["current_units"]["relative_humidity_2m"]])),
        "Rain":" ".join(map(str,[result["current"]["rain"],result["current_units"]["rain"]])),
        "Sunrise":get_utc(result["daily"]["sunrise"][0]),
        "Sunset":get_utc(result["daily"]["sunset"][0]),
        "Max temperature":" ".join(map(str,[result["daily"]["temperature_2m_max"][0],result["daily_units"]["temperature_2m_max"]])),
        "Min temperature":" ".join(map(str,[result["daily"]["temperature_2m_min"][0],result["daily_units"]["temperature_2m_min"]])),
        "UV index":result["daily"]["uv_index_max"][0]
    }
   
    for key,value in weather_info.items():
        print(f"{key} : {value}") # now the method map(str,value) changes every element in the list value into string

def main():
    city_name = input(("Enter the name of the city you would like to know the weather of: "))
    get_weather(city_name)

if __name__ == "__main__":
    main()


