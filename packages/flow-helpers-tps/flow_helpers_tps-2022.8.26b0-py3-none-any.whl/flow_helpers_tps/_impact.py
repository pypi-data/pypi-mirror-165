import requests
import json
import pandas as pd

class Impact:

    def __init__(self, account, key):
        self.account=account
        self.key=key

    def pull(self,url):
        response = json.loads(requests.get(url).text)
        df = pd.DataFrame(response['Records'])
        return df

    def construct_url(self,api,resource,id,addl_params):
        params = []
        for k, v in addl_params.items():
            if isinstance(v, list):
                for i in v:
                    params.append(f'{k}={i}')
            else:
                params.append(f'{k}={v}')
        params = '&'.join(params)
        url = f'https://{self.account}:{self.key}@api.impact.com/{api}/{self.account}/{resource}/{id}.json?{params}'
        return url


if __name__ == '__main__':
    account = ''
    key = ''
    api=''
    resource=''
    id=''
    addl_params = {
    }

    i=Impact(account, key)
    df=i.pull(i.construct_url(api,resource,id,addl_params))

    print(df)

