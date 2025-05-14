import requests
# import csv
import json

location_url = "http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code}&appid={open_weather_api_key}"
station_url = "https://api.weather.gov/points/{lat},{lon}"
forecast_url = "https://api.weather.gov/gridpoints/{station}/{lat},{lon}/forecast/hourly"
open_weather_url = "https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={open_weather_api_key}"
uv_url = "https://api.openuv.io/api/v1/forecast?lat={lat}&lng={lon}"


with open('config.json', 'r') as config_file:
    config = json.load(config_file)

open_weather_api_key = config['open_weather_api_key']
uv_headers = {
    "x-access-token": config['uv_api_key']
}


def check_season(time):
    month = time[5:7]
    if(month == '09' or month == '10' or month == '11'):
        return "autumn"
    if(month == '12' or month == '01' or month == '02'):
        return "winter"
    if(month == '03' or month == '04' or month == '05'):
        return "spring"
    if(month == '06' or month == '07' or month == '08'):
        return "summer"
    else:
        raise Exception("Invalid Season")


def check_clouds(value):
    if 0 <= value <= 20:
        return "clear"
    if 20 < value <= 70:
        return "partly cloudy"
    if 70 < value <= 90:
        return "cloudy"
    if 90 < value <= 100:
        return "overcast"
    else:
        raise Exception("Invalid Cloud Value")


def check_location(index):
    if index == 0:
        return "coastal"
    if index == 1:
        return "inland"
    if index == 2:
        return "mountain"
    else:
        raise Exception("Invalid Location Index")


def get_data(station, lat, lon, index, gridX, gridY):
    print(station)
    print(lat)
    print(lon)
    print(index)

    url = forecast_url.format(station=station, lat=gridX, lon=gridY)
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    values = data['properties']['periods']
    print(len(values))

    temperature = ['Temperature']
    humidity = ['Humidity']
    wind_speed = ['Wind Speed']
    precipitation = ['Precipitation (%)']
    location = ['Location']
    season = ['Season']
    atmosphere = ['Atmospheric Pressure']
    visibility = ['Visibility(km)']
    cloudiness = ['Cloud Cover']
    uv = ['UV Index']
    weather_type = ['Weather Type']

    for i in range(len(values)):
        temp_f = values[i]['temperature']
        temperature.append((temp_f-32)*5/9)
        humidity.append(values[i]['relativeHumidity']['value'])
        wind_speed.append(values[i]['windSpeed'])
        precipitation.append(values[i]['probabilityOfPrecipitation']['value'])
        location.append(check_location(index))
        time = values[i]['startTime']
        season.append(check_season(time))
        weather_type.append(values[i]['shortForecast'])

    url = open_weather_url.format(open_weather_api_key=open_weather_api_key, lat=lat, lon=lon)
    print(url)
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    values = data['list']

    for i in range(len(values)):
        atmosphere.append(values[i]['main']['pressure'])
        visibility.append(values[i]['visibility'] / 1000)
        cloudiness.append(check_clouds(values[i]['clouds']['all']))

    url = uv_url.format(lat=lat, lon=lon)
    response = requests.get(url,headers=uv_headers)
    response.raise_for_status()

    data = response.json()
    values = data['result']

    for i in range(len(values)):
        uv.append(values[i]['uv'])

    rows = zip(temperature, humidity, wind_speed, precipitation, cloudiness, atmosphere, uv, season, visibility, location, weather_type)
    return rows

def make_csv(csv_data):
    with open('live_weather_classification_data.csv', mode='w', newline='', encoding='utf-8') as f:
        import csv
        writer = csv.writer(f)
        writer.writerows(csv_data)

def main():
    inland_town_name = input("Enter the city name on an inland town: ")
    inland_state_name = input("Enter the state of the inland town: ")

    mountain_town_name = input("Enter the city name on a mountain town: ")
    mountain_state_name = input("Enter the state of the mountain town: ")

    coastal_town_name = input("Enter the city name on an coastal town: ")
    coastal_state_name = input("Enter the state of the coastal town: ")

    town_name = [coastal_town_name, inland_town_name, mountain_town_name]
    town_state = [coastal_state_name, inland_state_name, mountain_state_name]

    csv_data = []

    for i in range(3):
        url = location_url.format(city_name=town_name[i], state_code=town_state[i],
                                  open_weather_api_key=open_weather_api_key)
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        lat = data[0].get('lat')
        lon = data[0].get('lon')

        url = station_url.format(lat=lat, lon=lon)

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        station = data['properties']['gridId']
        gridX = data['properties']['gridX']
        gridY = data['properties']['gridY']

        csv_insert = get_data(station, lat, lon, i, gridX, gridY)
        csv_data.append(csv_insert)


    make_csv(csv_data)

if __name__ == '__main__':
    main()

