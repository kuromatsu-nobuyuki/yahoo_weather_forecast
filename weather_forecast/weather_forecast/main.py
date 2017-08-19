#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from client.YahooWeatherAPIClient import WeatherClient, Location

app_id = os.getenv('APP_ID', None)

if app_id is None:
    raise AttributeError('APP_ID environment is not set.')

if __name__ == '__main__':
    client = WeatherClient(token=app_id)

    location = Location(35.581442, 139.640531, '武蔵中原駅')
    rain_forecast = client.get_weather_forecast(location)

    if rain_forecast is not None:
        for forecast in rain_forecast:
            print '%d:%d %d mm/h' % (forecast['hour'], forecast['minute'], forecast['rainfall'])
    else:
        print 'It will not rain for a while.'
