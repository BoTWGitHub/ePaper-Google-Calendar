import os
import requests
import json

def get_data():
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"

    authorization = ""
    location = ""

    cfgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weatherConfig.json')
    if os.path.exists(cfgdir):
        with open(cfgdir, 'r') as configData:
            data = json.loads(configData.read())
            authorization = data["Authorization"]
            location = data["Location"]

    params = {
        "Authorization": authorization,
        "locationName": location,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)

        location = data["records"]["location"][0]["locationName"]

        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        print(location)
        print(start_time)
        print(end_time)
        print(weather_state)
        print(rain_prob)
        print(min_tem)
        print(comfort)
        print(max_tem)

    else:
        print(response.status_code, " : Can't get data!")


def main():
    get_data()

if __name__=='__main__':
    main()
