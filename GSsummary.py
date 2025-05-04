from collections import defaultdict
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from configparser import ConfigParser
import logging

# чтение конфигурационного файла
config = ConfigParser()
config.read('config.ini.i')

credentials_file = config['Google']['credentials_file']
table_url = config['Google']['table_url']


def summary_by_day(processed_data):
    """ 
    Генерирует ежедневную сводку по действиям пользователей
    """
    grouped_by_day = defaultdict(list)
    for action in processed_data:
        date = datetime.strptime(action['created_at'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
        grouped_by_day[date].append(action)

    day_summary = []
    for day, actions in grouped_by_day.items():
        # Общее количество попыток
        total_attempts = len(actions)

        # Run и submit 
        run_attempts = sum(1 for action in actions if action.get('attempt_type') == 'run')
        submit_attempts = sum(1 for action in actions if action.get('attempt_type') == 'submit')

        # Количество уникальных пользователей
        unique_users = len({action['user_id'] for action in actions})

        day_entry = {
            'date': day,
            'total_attempts': total_attempts,
            'run_attempts': run_attempts,
            'submit_attempts': submit_attempts,
            'unique_users': unique_users
            }
        day_summary.append(day_entry)
    logging.info(f'Сгенерировано саммари за {day_summary[0]["date"]}')
    return day_summary

def authorize_google_sheets():
    """Авторизация в Google Sheets API"""
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(credentials_file, scopes=scope)
        logging.info('Авторизация с API Google Sheets прошла успешно')
        return gspread.authorize(creds)
        
    except Exception as e:
        logging.error(f'Ошибка авторизации с API Google Sheets: {e}')
        raise

def add_summary_to_googlesheets(day_summary):
        """ 
        Загружает сводную статистику по дням в Google Таблицу.
        """
        try: 
            client = authorize_google_sheets()
            sheet = client.open_by_url(table_url).sheet1

            rows_to_add = [
                [day['date'], day['total_attempts'], day['run_attempts'], day['submit_attempts'], day['unique_users']] for day in day_summary
        ]

            sheet.append_rows(rows_to_add)
        
        except gspread.exceptions.APIError as e:
            logging.error(f'Ошибка Google API: {e.response.text}')
            raise
        except Exception as e:
            logging.error(f'Ошибка загрузки данных в Google Sheets: {str(e)}')
            raise
