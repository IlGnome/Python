#python 3
import requests
import sys
import time

'''

		REMOVE THE FUCKING API KEY BEFORE RELEASING.
		LIKE JESUS FUCK REMOVE IT

'''
try:
	WeatherInfo = requests.get("API KEY AND LOCATION GOES HERE") 

	CurrentConditions = WeatherInfo.json()

	DegreesF = CurrentConditions["current_observation"]["temp_f"]
	DegreesC = CurrentConditions["current_observation"]["temp_c"]
	HeatIndex = CurrentConditions["current_observation"]["heat_index_string"]
	Wind_MPH = CurrentConditions["current_observation"]["wind_string"]
	WeatherStatus = CurrentConditions["current_observation"]["weather"]
	WindChill = CurrentConditions["current_observation"]["windchill_string"]
	Humidity = CurrentConditions["current_observation"]["relative_humidity"]
	pass
except:
	print("Unable to show weather information at this time")
	sys.exit(1)
if HeatIndex == "NA":
	HeatIndex = ""

if WindChill == "NA":
	WindChill = ""



FeelsLike =" and feels like\x02 " + HeatIndex + WindChill + "\x02"	

if WindChill == "" and HeatIndex == "":
	FeelsLike = ""
# \x02 will bold the item in IRSSI


print( "At \x02%s\x02 the temprature is \x02%sF\x02 (\x02%sC\x02)%s, with a humidity of \x02%s\x02. The Wind is \x02%s\x02 and the weather is \x02%s\x02." % (time.strftime('%a %H:%M:%S'), DegreesF, DegreesC, FeelsLike, Humidity,  Wind_MPH, WeatherStatus))
