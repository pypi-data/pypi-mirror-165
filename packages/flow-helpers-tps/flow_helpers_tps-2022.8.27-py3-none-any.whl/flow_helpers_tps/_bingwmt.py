import requests
import json
import re
from datetime import datetime
import pandas as pd


# based off:
# https://gist.github.com/MartijnSch/4f1696f2c539740222818cb8d5076e24
# https://stackoverflow.com/questions/67160952/bing-webmaster-tools-api-with-python-how-can-i-specify-an-extraction-date-and

class Bing:
    def __init__(self, siteurl, apikey):
        self.key = apikey
        self.siteurl = siteurl

    def datefieldclean(self, datefield):
        t = datetime.fromtimestamp(
            int((re.search("/Date\\((.*)\\)/", datefield).group(1).replace('-0800', '').replace('-0700', ''))) / 1000).strftime('%Y-%m-%d')
        return t

    def get_ranktrafficstats(self):
        url = f'https://ssl.bing.com/webmaster/api.svc/json/GetRankAndTrafficStats?siteUrl={self.siteurl}&apikey={self.key}'
        headers = {'Content-Type': 'application/json'}
        payload = {}  # TODO: investigate if this can be used to pass in date parameter
        response = requests.request("GET", url, headers=headers, data=payload)
        entries = []

        if response.status_code == 200:
            query_data = json.loads(response.text)
        else:
            raise Exception(f'error,\
             response status: {response.status_code},\
             response text: {response.text},\
             response content: {response.content}')

        for each in query_data['d']:
            # TODO: figure out pagination & date if available
            # test case returns 2.7K rows from Jan - Aug 2020 only
            entries.append([
                (re.search("/Date\\((.*)\\)/", each['Date']).group(1)),
                self.datefieldclean(each['Date']),
                each['Impressions'],
                each['Clicks'],
            ])

        df = pd.DataFrame(data=entries, columns=['rawDate', 'Date', 'Impressions', 'Clicks'])
        df.customname = 'ranktrafficstats'
        return df

    def get_querystats(self):
        url = f'https://ssl.bing.com/webmaster/api.svc/json/GetQueryStats?siteUrl={self.siteurl}&apikey={self.key}'
        headers = {'Content-Type': 'application/json'}
        payload = {}  # TODO: investigate if this can be used to pass in date parameter
        response = requests.request("GET", url, headers=headers, data=payload)
        entries = []

        if response.status_code == 200:
            query_data = json.loads(response.text)
        else:
            raise Exception(f'error,\
                     response status: {response.status_code},\
                     response text: {response.text},\
                     response content: {response.content}')

        for each in query_data['d']:
            # TODO: figure out pagination & date if available
            # test case returns 2.7K rows from Jan - Aug 2020 only
            entries.append([
                (re.search("/Date\\((.*)\\)/", each['Date']).group(1)),
                self.datefieldclean(each['Date']),
                each['Query'],
                each['Impressions'],
                each['Clicks'],
                each['AvgClickPosition'] / 10,
                each['AvgImpressionPosition'] / 10
            ])

        df = pd.DataFrame(data=entries,
                          columns=['rawDate', 'Date', 'Query', 'Impressions', 'Clicks', 'AvgClickPosition',
                                   'AvgImpressionPosition'])
        df.customname = 'querystats'
        return df

    def get_json_ranktrafficstats(self):
        url = f'https://ssl.bing.com/webmaster/api.svc/json/GetRankAndTrafficStats?siteUrl={self.siteurl}&apikey={self.key}'
        headers = {'Content-Type': 'application/json'}
        payload = {}  # TODO: investigate if this can be used to pass in date parameter
        response = requests.request("GET", url, headers=headers, data=payload)
        entries = []

        if response.status_code == 200:
            query_data = response.text
        else:
            raise Exception(f'error,\
             response status: {response.status_code},\
             response text: {response.text},\
             response content: {response.content}')


        return query_data

    def get_json_querystats(self):
        url = f'https://ssl.bing.com/webmaster/api.svc/json/GetQueryStats?siteUrl={self.siteurl}&apikey={self.key}'
        headers = {'Content-Type': 'application/json'}
        payload = {}  # TODO: investigate if this can be used to pass in date parameter
        response = requests.request("GET", url, headers=headers, data=payload)
        entries = []

        if response.status_code == 200:
            query_data = response.text
        else:
            raise Exception(f'error,\
                     response status: {response.status_code},\
                     response text: {response.text},\
                     response content: {response.content}')


        return query_data
