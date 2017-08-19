FROM python:2.7

RUN apt-get update -y
RUN pip install requests

COPY weather_forecast /root/weather_forecast

CMD python /root/weather_forecast/main.py