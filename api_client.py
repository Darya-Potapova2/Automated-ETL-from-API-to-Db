from configparser import ConfigParser
from datetime import datetime, timedelta
import requests
import logging

# чтение конфигурационного файла
config = ConfigParser()
config.read('config.ini.i')

URL = config['API']['url']
CLIENT = config['API']['client']
CLIENT_KEY = config['API']['client_key']


def request_data(start_date, end_date):
    """
    Запрашивает данные с API itresume 
    """
    params = {
        'client': CLIENT,
        'client_key': CLIENT_KEY,
        'start': start_date,
        'end': end_date
    }
    try:
        response = requests.get(URL, params=params)
        data = response.json()
        return data
    except Exception as e:
        logging.error(f'Ошибка запроса данных: {e}')
        raise
