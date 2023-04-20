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
CLIENT_ID = 'amzn1.application-oa2-client.9fd2f3d1c6934f0292ed191c929b1fba'
CLIENT_SECRET = '1f17d8d087e59d5ff8a3ef6985903d065181a94d3c775c65069ee5c335f92cd3'
# REDIRECT_URI = 'https://amazon.com'
REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'
# REDIRECT_URI = ''
REGION = 'NA'
# PERMISSION_SCOPE =
