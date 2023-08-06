import pandas as pd
import requests
from requests.exceptions import HTTPError


class ScrapingHub:
    

    # initialized / instance attributes
    def __init__(self, key):
        self.key = key
        self.storage_url = 'https://storage.scrapinghub.com/'
        self.param_apikey = ('apikey', key)
        self.param_format_json = ('format','json')

    def get_joblist(self, project_id, spider=None):
        list_jobs_url = self.storage_url + f'jobq/{project_id}/list'
        joblist=[]

        if spider:
            param_spider = ('spider', spider)
        else:
            param_spider = None

        try:
            response = requests.get(url=list_jobs_url,
                                    params=[self.param_apikey,
                                            self.param_format_json,
                                            param_spider])
            response.raise_for_status()
        except HTTPError as http_err:
            (f'HTTP error occurred during joblist retrieval: {http_err}')
        else:
            jobs_summary = response.json()

        master = pd.DataFrame.from_records(jobs_summary)
        master.reset_index(inplace=True, drop=True)
        for each in master['key']:
            joblist.append(each)

        return joblist


    def get_jobdata(self, job_id, spider=None):
        """get job data for specified run"""
        job_item_url = self.storage_url + f'items/{job_id}/'

        if spider:
            param_spider = ('spider', spider)
        else:
            param_spider = None

        try:
            response = requests.get(url=job_item_url,
                                        params=[self.param_apikey,
                                                self.param_format_json,
                                                param_spider])
            response.raise_for_status()
        except HTTPError as http_err:
            (f'HTTP error occurred during item retrieval: {http_err}')
        else:
            specificItem = response.json()

        itemdf = pd.DataFrame.from_records(specificItem)
        itemdf['job'] = job_id

        return itemdf


    def get_spider_alljobs(self, project_id, spider):
        """pull all jobs and data for a specified spider"""
        itemdf = pd.DataFrame()

        keylist = self.get_joblist(project_id=project_id, spider=spider)

        for each in keylist:
            tempdf = self.get_jobdata(job_id=each, spider=spider)
            itemdf = pd.concat([itemdf, tempdf])

        itemdf.sort_values(by=['job'], inplace=True)
        itemdf.reset_index(drop=True, inplace=True)

        return itemdf