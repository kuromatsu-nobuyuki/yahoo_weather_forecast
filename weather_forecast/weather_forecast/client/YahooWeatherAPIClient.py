# -*- coding: utf-8 -*-
import requests

server_url = 'https://map.yahooapis.jp/weather/V1/place'


class Location:
    def __init__(self, longitude=None, latitude=None, location=None):
        """

        :param longitude: 緯度
        :param latitude: 軽度
        :param location: 地名
        """
        self.longitude = longitude
        self.latitude = latitude
        self.location  = location


class WeatherClient:
    def __init__(self, token):
        self.token = token

    def get_weather_forecast(self, location=None):
        """
        指定された地域の天気の情報を取得する
        :param location:
        :return: 雨の予報がなければNoneを、雨が降りそうであれば、予測した情報を返す。
        返り値は辞書のリスト。フォーマットは以下の通り
        [
        {
            'hour': 時,
            'minute': 分,
            'rainfall': 降雨量
        },
        ...
        ]
        """
        param = self.__create_param(location.longitude, location.latitude)

        try:
            weather_info = requests.get(url=server_url, params=param)
        except Exception as e:
            print e
            return None

        data = weather_info.json()
        weather_forecast_list = data['Feature'][0]['Property']['WeatherList']['Weather']

        # 降雨量が0以上かのフラグ
        is_fall = False

        forecast_list = []
        for forecast in weather_forecast_list:
            date_dict = self.__parse_date(forecast[u'Date'])

            rainfall = 0
            # YahooのAPIは雨が降らない場合、'Rainfall'のキーを返さない仕様らしい
            if 'Rainfall' in forecast:
                rainfall = float(forecast['Rainfall'])
                is_fall = True

            forecast_dict = {
                'hour': date_dict['hour'],
                'minute': date_dict['minute'],
                'rainfall': rainfall
            }

            forecast_list.append(forecast_dict)

        if not is_fall:
            return None

        return forecast_list

    def __create_param(self, longitude=None, latitude=None):
        param = {
            'appid': self.token,
            'coordinates': '%f,%f' % (longitude, latitude),
            'output': 'json',
            'interval': 5
        }
        return param

    def __parse_date(self, date_str=None):
        """
        YahooのAPIが返してくる日時をパースする
        :param date_str: フォーマット：'201708191500'
        :return: year, month, day, hour, minute
        """
        date = {
            'year': int(date_str[0:4]),
            'month': int(date_str[4:6]),
            'day': int(date_str[6:8]),
            'hour': int(date_str[8:10]),
            'minute': int(date_str[10:])
        }
        return date
