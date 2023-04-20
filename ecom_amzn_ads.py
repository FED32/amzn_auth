import requests
import json
import os
import gzip
import time
import pandas as pd
import numpy as np


class AmznAdsEcomru:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 redirect_uri: str,
                 region: str = 'NA'
                 ):

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        url_prefix_na = 'https://www.amazon.com/ap/oa'
        url_prefix_eu = 'https://eu.account.amazon.com/ap/oa'
        url_prefix_fe = 'https://apac.account.amazon.com/ap/oa'

        self.scope_1 = 'advertising::campaign_management'
        self.scope_2 = 'advertising::test:create_account'
        self.scope_3 = 'advertising::audiences'
        self.scope_4 = 'advertising::test:create_account%20advertising::campaign_management'

        authorization_url_na = 'https://api.amazon.com/auth/o2/token'
        authorization_url_eu = 'https://api.amazon.co.uk/auth/o2/token'
        authorization_url_fe = 'https://api.amazon.co.jp/auth/o2/token'

        api_url_na = 'https://advertising-api.amazon.com'
        api_url_eu = 'https://advertising-api-eu.amazon.com'
        api_url_fe = 'https://advertising-api-fe.amazon.com'

        self.access_token = None
        self.refresh_token = None

        if region == 'NA':
            self.url_prefix = url_prefix_na
            self.authorization_url = authorization_url_na
            self.api_url = api_url_na
        elif region == 'EU':
            self.url_prefix = url_prefix_eu
            self.authorization_url = authorization_url_eu
            self.api_url = api_url_eu
        elif region == 'FE':
            self.url_prefix = url_prefix_fe
            self.authorization_url = authorization_url_fe
            self.api_url = api_url_fe

    def create_auth_grant_url(self, permission_scope: str):
        """
        :return: authorization URL
        """
        auth_grant_url = self.url_prefix
        return f'{auth_grant_url}?scope={permission_scope}&response_type=code&client_id={self.client_id}&state=State&redirect_uri={self.redirect_uri}'

    def get_tokens(self, code=None, refresh_token=None):
        """
        :return: code 200 - JSON object with access_token, refresh_token, token_type, expires_in
        """
        url = self.authorization_url

        if code is not None and refresh_token is None:
            body = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': self.redirect_uri,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                    }
        elif code is None and refresh_token is not None:
            body = {'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                    }
        else:
            print('Incorrect data')
            return None

        response = requests.post(url, data=json.dumps(body))
        print(response.status_code)
        return response

    def test_acc_response(self, country='US', type_='VENDOR'):
        """
        Creating a test account
        """

        url = self.api_url + '/testAccounts'

        head = {'Amazon-Advertising-API-ClientId': self.client_id,
                'Authorization': 'Bearer ' + self.access_token,
                'content-type': 'application/json',
                'cache-control': 'no-cache'
                }

        body = {"countryCode": country,
                #         "accountMetaData": {"vendorCode": "ABCDE"},
                "accountMetaData": {},
                "accountType": type_
                }

        response = requests.post(url, headers=head, data=json.dumps(body))
        print(response.status_code)
        return response

    def test_acc_status(self, request_id):
        """
        Checking the status of an account creation request
        """
        url = f'{self.api_url}/testAccounts?requestId={request_id}'

        head = {'Amazon-Advertising-API-ClientId': self.client_id,
                'Authorization': 'Bearer ' + self.access_token
                }

        response = requests.get(url, headers=head)
        print(response.status_code)
        return response

    def get_profiles(self,
                     # api_program='campaign',
                     # access_level='view',
                     # profile_type_filter='vendor',
                     # valid_payment_method_filter='false'
                     ):
        """
        returns the profiles available for the authorized user account
        """
        url = self.api_url + '/v2/profiles'
        head = {'Amazon-Advertising-API-ClientId': self.client_id,
                'Authorization': 'Bearer ' + self.access_token}
        # params = {'apiProgram': api_program,
        #           'accessLevel': access_level,
        #           'profileTypeFilter': profile_type_filter,
        #           'validPaymentMethodFilter': valid_payment_method_filter
        #           }
        response = requests.get(url, headers=head
                                # params=params
                                )
        # print(response.status_code)
        return response

    def get_campaigns(self, profile_id):
        """Get campaigns"""

        # url = 'https://advertising-api.amazon.com/sp/campaign/list'
        url = f"{self.api_url}/sp/campaigns/list"

        head = {
            'Amazon-Advertising-API-ClientId': self.client_id,
            'Amazon-Advertising-API-Scope': str(profile_id),
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/vnd.spCampaign.v3+json',
            'Content-Type': 'application/vnd.spCampaign.v3+json'
        }

        return requests.post(url, headers=head)

    def campaign_report(self, profile_id, name, date_from, date_to):
        """Campaign report"""

        # url = 'https://advertising-api.amazon.com/reporting/reports'

        url = f'{self.api_url}/reporting/reports'

        head = {
            'Content-Type': 'application/vnd.createasyncreportrequest.v3+json',
            'Amazon-Advertising-API-ClientId': self.client_id,
            'Amazon-Advertising-API-Scope': str(profile_id),
            # 'Amazon-Advertising-API-Scope': self.scope_1,
            'Authorization': 'Bearer ' + self.access_token
        }

        body = {
            "name": name,
            "startDate": date_from,
            "endDate": date_to,
            "configuration": {
                "adProduct": "SPONSORED_PRODUCTS",
                "groupBy": ["campaign", "adGroup"],
                "columns": ["impressions", "clicks", "cost", "campaignId", "adGroupId", "date"],
                "reportTypeId": "spCampaigns",
                "timeUnit": "DAILY",
                "format": "GZIP_JSON"
            }
        }

        return requests.post(url, headers=head, data=json.dumps(body))

    def report_status(self, profile_id, report_id):
        """Checking report status"""

        url = f"{self.api_url}/reporting/reports/{report_id}"

        head = {
            'Content-Type': 'application/vnd.createasyncreportrequest.v3+json',
            'Amazon-Advertising-API-ClientId': self.client_id,
            'Amazon-Advertising-API-Scope': str(profile_id),
            'Authorization': 'Bearer ' + self.access_token
        }

        return requests.get(url, headers=head)

    @staticmethod
    def save_report(report_url, json_path=None):
        """Downloading reports"""

        req = requests.get(report_url)
        data = json.loads(gzip.decompress(req.content))

        if json_path is not None:
            with open(json_path, 'w') as f:
                json.dump(data, f)
                print(f'Saved: {json_path}')
            return 'OK'
        else:
            return data

        # with open(gzip_path, 'wb') as file:
        #     file.write(req.content)
        # #
        # if extract is True:
        #     with gzip.open(gzip_path, "rb") as f:
        #         data = json.loads(f.read())
        #     with open(json_path, 'w') as f:
        #         json.dump(data)
        #         print(data)
        #         # f.extractall(path)
        #     # with zipfile.ZipFile(path) as zf:
        #     #     zf.extractall(path)
        #     if rem_gzip is True:
        #         os.remove(path)
        #         print(f'Удаление {path}')

    def get_report(self, profile_id, report_id, json_path=None):

        url = f"{self.api_url}/reporting/reports/{report_id}"

        head = {
            'Content-Type': 'application/vnd.createasyncreportrequest.v3+json',
            'Amazon-Advertising-API-ClientId': self.client_id,
            'Amazon-Advertising-API-Scope': str(profile_id),
            'Authorization': 'Bearer ' + self.access_token
        }

        try:
            status = None
            while status != 'COMPLETED':
                req = requests.get(url, headers=head)
                status = req.json()['status']
                print(f"{report_id}: {status}")
                time.sleep(5)

            req = requests.get(url, headers=head)
            report_url = req.json()['url']

            return self.save_report(report_url, json_path)

        except:
            return None


