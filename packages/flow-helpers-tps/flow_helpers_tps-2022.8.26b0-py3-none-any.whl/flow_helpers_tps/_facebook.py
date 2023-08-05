import pandas as pd
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi
import hmac
import hashlib
import requests
import json

class Facebook:
    def __init__(self, app_id, app_secret, access_token):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.appsecret_proof = hmac.new(
            self.app_secret.encode('utf-8'),
            msg=self.access_token.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

    def pull_insights_sdk(self, adaccount_id, since, until, fieldlist, time_increment=1, level='ad'):
        FacebookAdsApi.init(app_id=self.app_id, app_secret=self.app_secret, access_token=self.access_token)
        # since / until is end date inclusive
        # time_increment = 1 to break into individual days

        params = {
            'time_increment':time_increment,
            'time_range': {
                'since': f'{since}',
                'until': f'{until}'
            },
            'fields': fieldlist,
            'breakdowns': [],
            'level': level,
            'action_report_time': 'conversion',
            'use_unified_attribution_setting': True
        }

        results = AdAccount(adaccount_id).get_insights(params=params)
        results = str(results)
        results = results.replace('<AdsInsights>','')
        results = json.loads(results)
        return results

    def pull_insights_requests(self, adaccount_id, since, until, fieldlist, time_increment=1):
        # since / until is end date inclusive
        # time_increment = 1 to break into individual days

        url = f'https://graph.facebook.com/v11.0/{adaccount_id}/insights'

        params = {
            'access_token': self.access_token,
            'appsecret_proof': self.appsecret_proof,
            'time_range': str({'since': f'{since}', 'until': f'{until}'}),
            'time_increment': time_increment,
            'fields': fieldlist,
            'breakdowns': [],
            'level': 'ad',
            'action_report_time': 'conversion',
            'use_unified_attribution_setting': True
        }

        results = requests.get(url=url, params=params)

        return results

    def transform(self, results):
        df = pd.DataFrame()
        for i in range(len(results)):
            r = results[i] ##._json
            if 'actions' in r:
                actions = r['actions']
                actions_unwrap = {}
                for a in actions:
                    actions_unwrap.update({a['action_type'] + '_actioncount': a['value']})
                del r['actions']
                r.update(actions_unwrap)
            if 'action_values' in r:
                action_values = r['action_values']
                action_values_unwrap = {}
                for av in action_values:
                    action_values_unwrap.update({av['action_type'] + '_actionvalue': av['value']})
                del r['action_values']
                r.update(action_values_unwrap)
            r = pd.DataFrame(r, index=[i, ])
            df = df.append(r)

        return df
