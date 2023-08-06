from googleapiclient import discovery
from googleapiclient import http
from google.oauth2 import service_account

import json
import pandas as pd


class GoogleAnalytics:

    # class variables
    SCOPES  = ['https://www.googleapis.com/auth/analytics.readonly']

    # instance variables
    def __init__(self, Key, productionviewId='3410964'):
        self.key=Key
        self.productionviewId = productionviewId
        self.testviewId = '185939573'

        credentials = service_account.Credentials.from_service_account_info(self.key)
        self.reportingobject = discovery.build('analyticsreporting', 'v4', credentials=credentials)

    def ConstructRequestBody(self, sDate, eDate, dims, metrics, metfilters, dimfilters, segmentId):
        """Generic report pull."""

        # error handling if too many inputs
        if len(dims) > 7:
            raise Exception('only up to 7 dimension columns allowed')
        if len(metrics) > 10:
            raise Exception('only up to 10 metric columns allowed')

        # pre-construct buildig blocks for request body
        dimslist = []
        metricslist = []
        metfilterclause = []
        dimfilterclause = []

        for each in metfilters:
                dict = {'metricName': each[0],
                        'operator': each[1],
                        'comparisonValue': each[2]}
                metfilterclause.append(dict)

        for each in dimfilters:
                dict = {'dimensionName': each[0],
                        'operator': each[1],
                        'expressions': each[2]}
                dimfilterclause.append(dict)

        for each in dims:
            dict = {'name': each}
            dimslist.append(dict)

        for each in metrics:
            dict = {'expression': each}
            metricslist.append(dict)

        if segmentId == '':
            if metfilters != '' and dimfilters != '':
                body = {
                    'reportRequests': [
                        {
                            'viewId': self.productionviewId,
                            'dateRanges': [{'startDate': '{}'.format(sDate),  # legacy
                                            'endDate': '{}'.format(eDate)}],  # legacy
                            'metrics': metricslist,
                            'dimensions': dimslist,
                            'metricFilterClauses': [
                                {'operator': 'AND'},
                                {'filters':
                                     metfilterclause
                                 }],
                            'dimensionFilterClauses': [
                                {'operator': 'AND'},
                                {'filters':
                                     dimfilterclause
                                 }],
                            'samplingLevel': 'LARGE',
                            'pageSize': '100000'
                        }
                    ]
                }

            elif metfilters == '' and dimfilters == '':
                body = {
                    'reportRequests': [
                        {
                            'viewId': self.productionviewId,
                            'dateRanges': [{'startDate': '{}'.format(sDate),  # legacy
                                            'endDate': '{}'.format(eDate)}],  # legacy
                            'metrics': metricslist,
                            'dimensions': dimslist,
                            'samplingLevel': 'LARGE',
                            'pageSize': '100000'
                        }
                    ]
                }

            elif metfilters != '' and dimfilters == '':
                body = {
                    'reportRequests': [
                        {
                            'viewId': self.productionviewId,
                            'dateRanges': [{'startDate': '{}'.format(sDate),  # legacy
                                            'endDate': '{}'.format(eDate)}],  # legacy
                            'metrics': metricslist,
                            'dimensions': dimslist,
                            'metricFilterClauses': [
                                {'operator': 'AND'},
                                {'filters':
                                     metfilterclause
                                 }],
                            'samplingLevel': 'LARGE',
                            'pageSize': '100000'
                        }
                    ]
                }

            elif metfilters == '' and dimfilters != '':
                body = {
                    'reportRequests': [
                        {
                            'viewId': self.productionviewId,
                            'dateRanges': [{'startDate': '{}'.format(sDate),  # legacy
                                            'endDate': '{}'.format(eDate)}],  # legacy
                            'metrics': metricslist,
                            'dimensions': dimslist,
                            'dimensionFilterClauses': [
                                {'operator': 'AND'},
                                {'filters':
                                     dimfilterclause
                                 }],
                            'samplingLevel': 'LARGE',
                            'pageSize': '100000'
                        }
                    ]
                }

        # for queries with segmentId, you must include ga:segment as a dimension in the toml file.
        # keep in mind the number of allowed dimensions (7)
        elif segmentId != '':
            if metfilters != '' and dimfilters != '':
                body = {
                    'reportRequests': [
                        {
                            'viewId': self.productionviewId,
                            'dateRanges': [{'startDate': '{}'.format(sDate),  # legacy
                                            'endDate': '{}'.format(eDate)}],  # legacy
                            'metrics': metricslist,
                            'dimensions': dimslist,
                            'metricFilterClauses': [
                                {'operator': 'AND'},
                                {'filters':
                                    metfilterclause
                                 }],
                            'dimensionFilterClauses':[
                                {'operator': 'AND'},
                                {'filters':
                                    dimfilterclause
                                 }],
                            'segments':[
                                {'segmentId': segmentId}
                            ],
                            'samplingLevel': 'LARGE',
                            'pageSize': '100000'
                        }
                    ]
                }

            elif metfilters == '' and dimfilters == '':
                body={
                    'reportRequests': [
                        {
                            'viewId': self.productionviewId,
                            'dateRanges': [{'startDate': '{}'.format(sDate), #legacy
                                            'endDate': '{}'.format(eDate)}], #legacy
                            'metrics': metricslist,
                            'dimensions':dimslist,
                            'segments': [
                                {'segmentId': segmentId}
                            ],
                            'samplingLevel':'LARGE',
                            'pageSize':'100000'
                        }
                    ]
                }

            elif metfilters != '' and dimfilters == '':
                body={
                    'reportRequests': [
                        {
                            'viewId': self.productionviewId,
                            'dateRanges': [{'startDate': '{}'.format(sDate), #legacy
                                            'endDate': '{}'.format(eDate)}], #legacy
                            'metrics': metricslist,
                            'dimensions':dimslist,
                            'metricFilterClauses': [
                                {'operator': 'AND'},
                                {'filters':
                                    metfilterclause
                                 }],
                            'segments': [
                                {'segmentId': segmentId}
                            ],
                            'samplingLevel':'LARGE',
                            'pageSize':'100000'
                        }
                    ]
                }

            elif metfilters== '' and dimfilters != '':
                body={
                    'reportRequests': [
                        {
                            'viewId': self.productionviewId,
                            'dateRanges': [{'startDate': '{}'.format(sDate), #legacy
                                            'endDate': '{}'.format(eDate)}], #legacy
                            'metrics': metricslist,
                            'dimensions':dimslist,
                            'dimensionFilterClauses':[
                                {'operator': 'AND'},
                                {'filters':
                                    dimfilterclause
                                 }],
                            'segments': [
                                {'segmentId': segmentId}
                            ],
                            'samplingLevel':'LARGE',
                            'pageSize':'100000'
                        }
                    ]
                }

        return body


    def ExecuteRequest(self,requestbody):
        """execute GA and return df"""
        # initialize, construct, execute request
        analytics = self.reportingobject

        r = analytics.reports().batchGet(body=requestbody).execute()

        try:
            df = request_to_df(r)
            return df
        except KeyError:
            pass


def request_to_df(r):
    """transform GA response json into df"""

    dim_columns = r['reports'][0]['columnHeader']['dimensions']
    met_columns = []

    for key in r['reports'][0]['columnHeader']['metricHeader']['metricHeaderEntries']:
        met_columns.append(key['name'])

    if len(r['reports'][0]['data']) == 1:
        print("Missing Data from Report")
        return None

    rpt = pd.DataFrame(r['reports'][0]['data']['rows'])

    dim = rpt['dimensions'].apply(pd.Series)
    dim.columns = dim_columns

    met = rpt['metrics'].apply(
        pd.Series)[0].apply(
        pd.Series)['values'].apply(
        pd.Series)
    met.columns = met_columns

    df = pd.concat([dim, met], axis=1)
    if 'ga:date' in df.columns:
        df['ga:date'] = pd.to_datetime(df['ga:date'])
    if 'ga:dateHourMinute' in df.columns:
        df['ga:dateHourMinute'] = pd.to_datetime(df['ga:dateHourMinute'])

    return df