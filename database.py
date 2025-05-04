import psycopg2
import logging

class DBConnector:
    def __init__(self, host, database, user, password):
        self.db_config = {
            'host': host,
            'database': database,
            'user': user,
            'password': password
        }

    def load_to_database(self, processed_data):
        """
        Загружает обработанные данные в PostgreSQL базу данных MyGrader в таблицу 'skillfactory_grader'
        """
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()

            for action in processed_data:
                cur.execute("INSERT INTO skillfactory_grader (user_id, client_token, result_source, outcome_service, is_correct, attempt_type, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                            (action['user_id'], action['client_token'], action['result_source'], action['outcome_service'], action['is_correct'], action['attempt_type'], action['created_at']))
            conn.commit()
            cur.close()
        
        except Exception as e:
            logging.error(f'Ошибка загрузки данных в БД: {e}')
            raise
        finally:
            if conn:
                cur.close()
                conn.close()

