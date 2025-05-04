import os
import glob
import re
import logging
from datetime import datetime, timedelta
from configparser import ConfigParser

# чтение конфигурационного файла
config = ConfigParser()
config.read('config.ini.i')

logs_dir = config['Logging']['logs_dir']
days_to_keep = config['Logging']['days_to_keep']

def create_logger():
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    log_filename = os.path.join(logs_dir, f"{datetime.now().strftime('%Y-%m-%d')}.txt")
    print(f'Лог пишется в файл: {log_filename}')

    logging.basicConfig(
        filename=log_filename,
        filemode='a',
        format='%(asctime)s - %(name)s %(levelname)s: %(message)s',
        level=logging.INFO,
        force=True
        )

def clean_old_logs(logs_dir="logs", days_to_keep=3):
    edge_date = (datetime.now() - timedelta(days=3)).date()

    for file in glob.glob(os.path.join(logs_dir, '*.txt')):
        pattern = r'\d{4}-\d{2}-\d{2}'
        match = re.search(pattern, file)
        if match:
            file_date = datetime.strptime(match.group(), '%Y-%m-%d').date() 
            if file_date < edge_date:
                os.remove(file)
