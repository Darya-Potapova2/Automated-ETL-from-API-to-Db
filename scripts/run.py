from datetime import datetime, date, timedelta
from configparser import ConfigParser
import logging
from api_client import request_data
from process_data import process_data
from database import DBConnector
from GSsummary import summary_by_day, add_summary_to_googlesheets
from mail_sender import send_email
from logger import create_logger, clean_old_logs

# чтение конфигурационного файла
config = ConfigParser()
config.read('config.ini.i')

HOST = config['Database']['HOST']
DATABASE = config['Database']['DATABASE']
USER = config['Database']['USER']
PASSWORD = config['Database']['PASSWORD']
TABLE = config['Database']['TABLE']

def run():
    # Инициализация логирования
    create_logger()
    clean_old_logs()

    try:
        # Параметры для запроса (последние сутки)
        start_date = datetime.today() - timedelta(days=1)
        end_date = datetime.today()
        
        logging.info(f'Запуск пайплайна обработки данных за {date.today() - timedelta(days=1)}')

        # 1. Получение данных
        logging.info('Этап 1/5: Запрос исходных данных из API')
        raw_data = request_data(start_date, end_date)
        logging.info(f'Успешно получено {len(raw_data)} записей из API')
        
        # 2. Обработка данных
        logging.info('Этап 2/5: Преобразование и валидация данных')
        processed_data = process_data(raw_data)
        logging.info(f'Обработано {len(processed_data)} записей')

        # 3. Сохранение в БД
        logging.info(f'Этап 3/5: Загрузка данных в базу {DATABASE}')
        db_connector = DBConnector(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            table=TABLE
        )
        db_connector.load_to_database(processed_data)
        logging.info('Данные успешно загружены в базу')
        
        # 4. Формирование и загрузка отчета
        logging.info('Этап 4/5: Генерация сводного отчета')
        summary = summary_by_day(processed_data)
        add_summary_to_googlesheets(summary)
        logging.info(f'Отчет успешно добавлен в GoogleSheets')
        
        # 5. Отправка уведомлений
        logging.info('Этап 5/5: Отправка email-уведомлений')
        send_email()
        logging.info('Email-уведомления об обработке данных отправлены сотрудникам')
        
        logging.info(f'Пайплайн обработки данных за {date.today() - timedelta(days=1)} успешно завершен. Обработано {len(processed_data)} записей')
    
    except Exception as e:
        logging.error(f'Ошибка обработки: {str(e)}')
        raise

run()