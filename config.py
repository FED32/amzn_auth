import os


# настройка flask
class Configuration(object):
    DEBUG = False


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# базы данных
PG_HOST = os.environ.get('ECOMRU_PG_HOST', None)
PG_PORT = os.environ.get('ECOMRU_PG_PORT', None)
PG_SSL_MODE = os.environ.get('ECOMRU_PG_SSL_MODE', None)
PG_DB_NAME = os.environ.get('ECOMRU_PG_DB_NAME', None)
PG_USER = os.environ.get('ECOMRU_PG_USER', None)
PG_PASSWORD = os.environ.get('ECOMRU_PG_PASSWORD', None)
PG_target_session_attrs = 'read-write'

CH_HOST = os.environ.get('ECOMRU_CH_HOST', None)
CH_DB_NAME = os.environ.get('ECOMRU_CH_DB_NAME', None)
CH_USER = os.environ.get('ECOMRU_CH_USER', None)
CH_PASSWORD = os.environ.get('ECOMRU_CH_PASSWORD', None)
CH_PORT = os.environ.get('ECOMRU_CH_PORT', None)

PG_DB_PARAMS = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

# приложение LwA
CLIENT_ID = os.environ.get('AMZN_LWA_CLIENT_ID', None)
CLIENT_SECRET = os.environ.get('AMZN_LWA_CLIENT_SECRET', None)

# REDIRECT_URI = 'https://amazon.com'
# REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'
REDIRECT_URI = 'https://apps0.ecomru.ru:4433/oauth2callback'
REGION = 'NA'
# PERMISSION_SCOPE =
