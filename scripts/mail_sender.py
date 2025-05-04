import ssl
import smtplib 
import logging
from configparser import ConfigParser
from datetime import date, timedelta

# чтение конфигурационного файла
config = ConfigParser()
config.read('config.ini.i')

smtp_login = config['Email']['smtp_login']
smtp_password = config['Email']['smtp_password']
smtp_server = config['Email']['smtp_server']
smtp_port = int(config['Email']['smtp_port'])
recipients = [r.strip() for r in config['Email']['recipients'].split(',')]

def send_email():
    """ 
    Отправляет email-уведомления указанным получателям через SMTP сервер mail.ru.
    Текст письма фиксированный, уведомляет об успешной обработке данных. 
    """
    
    try:
        context = ssl.create_default_context()
        smtpObj = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtpObj.login(
            smtp_login,
            smtp_password
        )
        from_email = smtp_login

        subject = f"Уведомление об обработке данных за {date.today() - timedelta(days=1)}"
        body = f"""
        Уважаемые коллеги,
        
        Информируем вас, что обработка данных за {date.today() - timedelta(days=1)} успешно завершена. Данные загружены в БД, а сводный отчет - в Google Таблицы.
        
        Это автоматическое уведомление, пожалуйста, не отвечайте на это письмо.
        """
        
        message = f"Subject: {subject}\n\n{body}".encode('utf-8')

        for recipient in recipients:
            smtpObj.sendmail(from_email, recipient, message)
        smtpObj.quit()

    except Exception as e:
        logging.error(f'Ошибка при отправке email: {e}')
