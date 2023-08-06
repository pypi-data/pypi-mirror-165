from tasq_cli import settings
from tasq_cli.utils import get_credentials, get_config_file_path

logger = settings.get_logger()

CLIENT_ID = None
BUCKET = None
URL_PREFIX = None
ACCESS_KEY = None
SECRET_KEY = None
TOKEN = None


def load_credentials(config_file_path=None):
    credentials = get_credentials(config_file_path)

    if not credentials.get('client_id') or not credentials.get('access_key') or not credentials.get('secret_key'):
        logger.critical(f'Default credentials not set!, please add valid credentials to {get_config_file_path()}')
        exit(1)

    global CLIENT_ID, BUCKET, URL_PREFIX, ACCESS_KEY, SECRET_KEY, TOKEN
    CLIENT_ID = credentials['client_id']
    BUCKET = credentials['bucket_name']
    URL_PREFIX = credentials['url_prefix']
    ACCESS_KEY = credentials['access_key']
    SECRET_KEY = credentials['secret_key']
    TOKEN = credentials['token']


load_credentials()  # Initial credentials with values from default config file
