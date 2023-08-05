from googleapiclient import discovery
from googleapiclient import http
from google.oauth2 import service_account
import pandas as pd

class GSC:
    # instance attributes
    def __init__(self, key):
        self.key = key
        credentials = service_account.Credentials.from_service_account_info(self.key)
        self.service = discovery.build('searchconsole', 'v1', credentials=credentials)


    def list_sites(self):
        sitelist = self.service.sites().list().execute()
        return sitelist


    def ConstructQueryRequestBody(self, sdate, edate, dims, dimfilters):
        # https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics/query
        dimfilterclause = []

        for each in dimfilters:
            dict = {'dimension': each[0],
                    'operator': each[1],
                    'expression': each[2]}
            dimfilterclause.append(dict)

        if dimfilters != '':
            request = {
                'startDate': sdate,
                'endDate': edate,
                'dimensions': dims,  # feed in a list of dimensions
                'searchType': 'web',  # web, image, video
                'dimensionFilterGroups': [
                    {
                        'groupType': 'and',
                        'filters': dimfilterclause
                    }
                ],
                'aggregationType': 'byProperty',  # other option is byPage or byProperty
                'rowLimit': 20000,  # range 1-25000, default 1000
                'startRow': 0  # default 0, is zero-based index
            }

        elif dimfilters == '':
            request = {
                'startDate': sdate,
                'endDate': edate,
                'dimensions': dims,  # feed in a list of dimensions
                'searchType': 'web',  # web, image, video
                'aggregationType': 'byProperty',  # other option is byPage or byProperty
                'rowLimit': 20000,  # range 1-25000, default 1000
                'startRow': 0  # default 0, is zero-based index
            }

        return request


    def ConstructInspectRequestBody(self, url, site='https://www.theparkingspot.com/'):
        # https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect
        request = {
                "inspectionUrl": url,
                "siteUrl": site,
                "languageCode": "en-US"
        }
        return request


    def execute_request(self, type, service,request, property_uri=None):
        """Executes a searchAnalytics.query request.
        Args:
          service: The webmasters service to use when executing the query.
          property_uri: The site or app URI to request data for.
          request: The request to be executed.
        Returns:
          An array of response rows.
        """
        if type == 'query':
            return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()

        elif type == 'inspect':
            return service.urlInspection().index().inspect(body=request).execute()


    def run_request(self, type, site, request):
        response = self.execute_request(type=type, service=self.service, property_uri=site, request=request)
        return response


    def results_todf(self, type, response, dims=None):
        # if len(response) == 1:
        #     return 'no data returned'

        if type == 'query':
            df = pd.DataFrame(response['rows'])
            df[dims] = pd.DataFrame(df['keys'].values.tolist(), index=df.index)

            return df

        elif type == 'inspect':
            indexStatusResult = response['inspectionResult']['indexStatusResult']
            try:
                mobileStatusResult = response['inspectionResult']['mobileUsabilityResult']
            except:
                mobileStatusResult = 'na'
            if 'issues' not in mobileStatusResult.keys():
                mobileStatusResult['issues'] = None
            if 'referringUrls' in indexStatusResult.keys():
                del indexStatusResult['referringUrls']
            mobileStatusResult2 = {'msr_' + k: v for (k, v) in mobileStatusResult.items()}
            indexStatusResult2 = {'isr_' + k: v for (k, v) in indexStatusResult.items()}
            concatDict = {**indexStatusResult2, **mobileStatusResult2}
            df = pd.DataFrame(concatDict)

            return df

