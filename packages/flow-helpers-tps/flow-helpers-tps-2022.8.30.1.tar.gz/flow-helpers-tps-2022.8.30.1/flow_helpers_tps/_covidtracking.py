from datetime import datetime
import requests
import json
import pandas as pd

class covidtracking:
    def __init__(self):
        pass

    # Make a get request to get the latest data from covid tracking website api
    # Get the response data as a python object
    def get_covid(self):
        url=f'https://covidtracking.com/api/v1/states/daily.json'
        r=requests.get(url)
        data=r.json()

        # Convert COVID-19 .json into pandas dataframe
        with open('covid_daily.json','w') as file:
            json.dump(data, file, sort_keys=True, indent=4)
        df = pd.read_json('covid_daily.json')

        # print(df)
        return df