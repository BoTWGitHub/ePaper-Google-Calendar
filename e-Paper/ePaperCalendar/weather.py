import os
import json
import enum
import requests
import logging

WEATHER_URL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"

class WeatherType(enum.Enum):
    Sun = 1
    SunAndCloud = 2
    Cloud = 3
    Wind = 4
    Rain = 5

class Weather:
    def __init__(self) -> None:
        self.weathState = ""
        self.minTemp    = "20"
        self.maxTemp    = "22"
        self.rainProb   = "50"

    def fetchWeather(self) -> None:
        logging.info("fetching weather...")
        authorization = ""
        location = ""

        configFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config\\weatherConfig.json')
        if os.path.exists(configFile):
            with open(configFile, 'r') as configData:
                try:
                    data = json.loads(configData.read())
                    authorization = data["Authorization"]
                    location = data["Location"]
                except:
                    logging.error('weather config file error...')
                    return
        else:
            logging.error(configFile + ' doesn\'t exist')
            return
        
        params = {
            "Authorization": authorization,
            "locationName": location,
        }

        response = requests.get(WEATHER_URL, params=params)
        if response.status_code == 200:
            data = json.loads(response.text)

            weather_elements = data["records"]["location"][0]["weatherElement"]
            self.weathState = weather_elements[0]["time"][0]["parameter"]["parameterName"]
            self.rainProb = weather_elements[1]["time"][0]["parameter"]["parameterName"]
            self.minTemp = weather_elements[2]["time"][0]["parameter"]["parameterName"]
            self.maxTemp = weather_elements[4]["time"][0]["parameter"]["parameterName"]
            logging.info("weather : " + self.weathState)

        else:
            logging.error(response.status_code, " : Can't get data!")

    def getWeather(self) -> list[str]:
        return [self.minTemp, self.maxTemp, self.rainProb]

    def getWeatherType(self):
        type = WeatherType.SunAndCloud

        if self.weathState.find("雨")!=-1:
            type = WeatherType.Rain
        elif self.weathState.find("晴")!=-1 and self.weathState.find("雲")!=-1:
            type = WeatherType.SunAndCloud
        elif self.weathState.find("風")!=-1:
            type = WeatherType.Wind
        elif self.weathState.find("晴")!=-1:
            type = WeatherType.Sun
        elif self.weathState.find("雲")!=-1:
            type = WeatherType.Cloud

        return type
