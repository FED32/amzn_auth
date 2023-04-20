import flask
from flask import jsonify, request
import requests
import re
import json
from werkzeug.exceptions import BadRequestKeyError
from ecom_amzn_ads import AmznAdsEcomru
import config
from config import Configuration
import logger

logger = logger.init_logger()

amzn = AmznAdsEcomru(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    redirect_uri=config.REDIRECT_URI,
    region=config.REGION
)


app = flask.Flask(__name__)
app.config.from_object(Configuration)


@app.route('/authorize')
def authorize():

    auth_url = amzn.create_auth_grant_url(permission_scope=amzn.scope_4)

    return flask.redirect(auth_url)


@app.route('/oauth2callback')
def oauth2callback():

    try:
        url = str(request.url)

        # pattern = r'code=(.*?)&'
        # code = re.findall(pattern, url)[0]
        code = request.args.get('code', None)

        res = amzn.get_tokens(code=code)

        if res.status_code == 200:
            credentials = res.json()
            logger.info(f"credentials successfully")

            # код для вставки в базу

            # return flask.redirect("https://lk.ecomru.ru")
            return jsonify(credentials)

        else:
            logger.error(f"get tokens error: {res.status_code}, {res.json()}")
            return jsonify({'error': "auth error"})

    except BaseException as ex:
        logger.error(f"oauth2callback error: {ex}")
        return jsonify({'error': "auth error"})

