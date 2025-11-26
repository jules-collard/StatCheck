import os
from dotenv import load_dotenv

import logfire

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT')
BACKEND_URL = os.getenv('BACKEND_URL')
LOGFIRE_TOKEN = os.getenv('LOGFIRE_TOKEN')

logfire.configure(environment=ENVIRONMENT)

def get_log_level(status_code: int):
    if status_code >= 400 and status_code < 500:
        return 'notice'
    elif status_code >= 500:
        return 'warn'
    else:
        return 'info'

if __name__ == '__main__':
    logfire.info('Successfully launched db-updates')