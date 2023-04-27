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
app.secret_key = config.FLASK_SECRET_KEY


def get_user_info(access_token: str):

    url = "https://api.amazon.com/user/profile"
    headers = {
        # 'x-amz-access-token': access_token,
        'Authorization': f"Bearer {access_token}",
        'Accept': 'application/json',
        'Accept-Language': 'en-US'
    }

    res = requests.get(url, headers=headers)
    # print(res.status_code)
    if res.status_code != 200:
        logger.error("error for Obtain Customer Profile Information")
        return None

    return res.json()


@app.route('/authorize')
def authorize():

    client_id = request.args.get('client_id')
    # flask.session['client_id'] = client_id

    auth_url = amzn.create_auth_grant_url(permission_scope=amzn.scope_4+'%20profile', state=client_id)

    return flask.redirect(auth_url)


@app.route('/oauth2callback')
def oauth2callback():

    try:

        # url = str(request.url)
        # pattern = r'code=(.*?)&'
        # code = re.findall(pattern, url)[0]
        code = request.args.get('code', None)
        # client_id = flask.session['client_id']
        client_id = request.args.get('state', None)

        if request.args.get('error') is not None:
            error = {'client_id': client_id, 'error': request.args.get('error')}
            logger.error(f"oauth2callback error: {error}")

            # return flask.redirect("https://lk.ecomru.ru")
            return jsonify(error)

        res = amzn.get_tokens(code=code)

        if res.status_code == 200:
            credentials = res.json()
            logger.info(f"credentials successfully")

            profiles = {}
            regions = ['NA', 'EU', 'FE']

            for region in regions:
                amzn_reg = AmznAdsEcomru(
                    client_id=config.CLIENT_ID,
                    client_secret=config.CLIENT_SECRET,
                    region=region
                )
                # tokens = amzn_reg.get_tokens(refresh_token=credentials["refresh_token"])
                # amzn_reg.access_token = tokens.json()['access_token']
                amzn_reg.access_token = credentials["access_token"]
                profiles[region] = amzn_reg.get_profiles()

            # print(profiles)
            # print(request.headers)

            user_info = get_user_info(access_token=credentials["access_token"])
            # print(user_info)

            result = {
                'client_id': client_id,
                'credentials': credentials,
                'profiles': profiles,
                'user_info': user_info
            }

            # код для вставки в базу

            # return flask.redirect("https://lk.ecomru.ru")
            return jsonify(result)

        else:
            logger.error(f"get tokens error: {res.status_code}, {res.json()}")
            # return flask.redirect("https://lk.ecomru.ru")
            return jsonify({'error': "auth error"})

    except BaseException as ex:
        logger.error(f"oauth2callback error: {ex}")
        # return flask.redirect("https://lk.ecomru.ru")
        return jsonify({'error': "auth error"})

