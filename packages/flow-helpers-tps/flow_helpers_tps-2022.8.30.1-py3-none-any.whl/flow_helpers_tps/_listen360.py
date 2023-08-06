from datetime import date, timedelta, datetime
import requests
import pandas as pd
import xml.etree.ElementTree as ET


class Listen360:
    def __init__(self, org, user, pw):
        self.org=org
        self.user = user
        self.pw=pw

    def get_reviews(self, start_date, end_date):
        start_date=start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        url=f'https://app.listen360.com/organizations/{self.org}/reviews.csv?per_page=50000&start_date={start_date}T00:00:00&end_date={end_date}T23:59:59'
        r=requests.get(url,auth=(self.user,self.pw))
        t=r.text
        t=t.encode('ascii','ignore').decode('utf-8')
        return t

    def get_customers(self, page_start, page_end):
        url=f'https://app.listen360.com/organizations/{self.org}/customers.xml?'

        df_cols = ['company-name'
            , 'created-at'
            , 'first-name'
            , 'full-name'
            , 'id'
            , 'last-name'
            , 'last-survey-bounced'
            , 'mobile-phone-number'
            , 'name'
            , 'net-promoter-label'
            , 'organization-id'
            , 'permits-contact'
            , 'reference'
            , 'status'
            , 'title'
            , 'updated-at'
            , 'work-city'
            , 'work-country'
            , 'work-email'
            , 'work-phone-number'
            , 'work-postal-code'
            , 'work-region'
            , 'work-street'
            , 'custom-choice-1-label'
            , 'custom-choice-2-label'
            , 'custom-choice-3-label'
            , 'custom-choice-4-label'
            , 'custom-choice-5-label'
            , 'custom-choice-6-label'
            , 'custom-choice-7-label'
            , 'custom-choice-8-label'
            , 'custom-choice-9-label'
            , 'custom-choice-10-label'
            , 'permits-email-contact'
            , 'permits-sms-contact', ]

        rows = []

        for page in reversed(range(page_start, page_end)):

            if page < page_end + 1:
                response = requests.get(url + f"&page={page}", auth=(self.user, self.pw))
                print(url + f"page=" + str(page))

                if response.status_code == 200:
                    root = ET.fromstring(response.content)

                    for node in root:
                        res = []
                        res.append(node.attrib.get(df_cols[0]))
                        for el in df_cols[1:]:
                            if node is not None and node.find(el) is not None:
                                res.append(node.find(el).text)
                            else:
                                res.append(None)
                        rows.append({df_cols[i]: res[i]
                                     for i, dummy in enumerate(df_cols)})

                else:
                    pass
            else:
                pass

        t = pd.DataFrame(rows, columns=df_cols)
        return t