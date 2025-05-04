import json
import logging
from datetime import datetime
from collections import defaultdict

def process_data(raw_data):
    """
    Обрабатывает сырые данные из API
    """
    logging.info('Началось преобразование сырых данных')
    processed_data = []

    for action in raw_data:
        if not action.get('passback_params'):
            continue

        try: 
            params_str = action['passback_params'].replace("'", '"')
            params_dict = json.loads(params_str)

            processed_data.append({
                'user_id': action['lti_user_id'],
                'client_token': params_dict.get('oauth_consumer_key', ''),
                'result_source': params_dict.get('lis_result_sourcedid', ''),
                'outcome_service': params_dict.get('lis_outcome_service_url', ''),
                'is_correct': action['is_correct'],
                'attempt_type': action['attempt_type'],
                'created_at': action['created_at']
            })

        except json.JSONDecodeError as e:
            logging.warning(f'Ошибка декодирования JSON: {e} в данных: {action["passback_params"]}')
        
        except Exception as e:
            logging.error(f'Ошибка преобразования сырых данных: {e}')

    return processed_data

