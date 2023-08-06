import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import pandas as pd
import xml.etree.ElementTree as ET
import pandas as pd


class SalesforceSOAP:
    # NOTE: salesforce APIs are CASE SENSITIVE! stupid.

    def __init__(self, clientId, clientSecret, auth_url, service_url):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.auth_url = auth_url
        self.service_url = service_url
        self.auth_token = ''

    def get_auth_token(self):
        '''if auth token is blank, then gets initial access token
        if auth token is not blank, then gets a refresh access token using current auth token'''
        auth_token_url = self.auth_url + '/v2/token'

        if self.auth_token == '':
            payload = {
                "client_id": self.clientId,
                "client_secret": self.clientSecret,
                "grant_type": "client_credentials",
            }
        elif self.auth_token != '':
            payload = {
                "client_id": self.clientId,
                "client_secret": self.clientSecret,
                "grant_type": "client_credentials",
                "access_token": self.auth_token
            }

        payload = json.dumps(payload)  # turn into string

        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", auth_token_url, headers=headers, data=payload)

        response_dict = response.json()

        # write value of token
        self.auth_token = response_dict['access_token']

        return self.auth_token

    def get_list(self, listId=None):
        '''retrieve specified list. if none specified, retrieves all lists'''
        service_url = self.service_url

        if self.auth_token is None:
            self.get_auth_token()

        if listId != None:
            payload = '''<?xml version="1.0" encoding="UTF-8"?>
                <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                   <s:Header>
                      <a:Action s:mustUnderstand="1">Retrieve</a:Action>
                      <a:MessageID>urn:uuid:7e0cca04-57bd-4481-864c-6ea8039d2ea0</a:MessageID>
                      <a:ReplyTo>
                         <a:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
                      </a:ReplyTo>
                      <a:To s:mustUnderstand="1">{service_url}</a:To>
                      <a:fueloauth>{auth_token}</a:fueloauth>
                   </s:Header>
                    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
                         <RetrieveRequest>
                            <ObjectType>List</ObjectType>
                            <Properties>ListName</Properties>
                            <Properties>ID</Properties>
                            <Filter xsi:type="SimpleFilterPart">
                            <Property>ID</Property>
                            <SimpleOperator>equals</SimpleOperator>
                            <Value>{listId}</Value>
                            </Filter>
                         </RetrieveRequest>
                      </RetrieveRequestMsg>
                    </s:Body>
                </s:Envelope>'''

        elif listId is None:
            payload = '''<?xml version="1.0" encoding="UTF-8"?>
                <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                   <s:Header>
                      <a:Action s:mustUnderstand="1">Retrieve</a:Action>
                      <a:MessageID>urn:uuid:7e0cca04-57bd-4481-864c-6ea8039d2ea0</a:MessageID>
                      <a:ReplyTo>
                         <a:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
                      </a:ReplyTo>
                      <a:To s:mustUnderstand="1">{service_url}</a:To>
                      <a:fueloauth>{auth_token}</a:fueloauth>
                   </s:Header>
                    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
                         <RetrieveRequest>
                            <ObjectType>List</ObjectType>
                            <Properties>ListName</Properties>
                            <Properties>ID</Properties>
                         </RetrieveRequest>
                      </RetrieveRequestMsg>
                    </s:Body>
                </s:Envelope>'''

        headers = {'Content-Type': 'application/soap+xml'}
        data = payload.format(auth_token=self.auth_token, listId=listId, service_url=service_url)

        response = requests.request("POST", url=service_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.text

        elif response.status_code >= 500: #TODO: less hacked-together reauth
            self.get_auth_token()
            data = payload.format(auth_token=self.auth_token, listId=listId, service_url=service_url)
            response = requests.request("POST", url=service_url, headers=headers, data=data)
            return response.text

    def get_list_subscribers(self, listId):
        '''retrieve subscribers from list'''
        service_url = self.service_url

        if self.auth_token == '':
            self.get_auth_token()

        payload = '''<?xml version="1.0" encoding="UTF-8"?>
            <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
               <s:Header>
                  <a:Action s:mustUnderstand="1">Retrieve</a:Action>
                  <a:MessageID>urn:uuid:7e0cca04-57bd-4481-864c-6ea8039d2ea0</a:MessageID>
                  <a:ReplyTo>
                     <a:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
                  </a:ReplyTo>
                  <a:To s:mustUnderstand="1">{service_url}</a:To>
                  <a:fueloauth>{auth_token}</a:fueloauth>
               </s:Header>
                <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
                     <RetrieveRequest>
                        <ObjectType>ListSubscriber</ObjectType>
                        <Properties>ObjectID</Properties>
                        <Properties>SubscriberKey</Properties>
                        <Properties>CreatedDate</Properties>
                        <Properties>ModifiedDate</Properties>
                        <Properties>Client.ID</Properties>
                        <Properties>Client.PartnerClientKey</Properties>
                        <Properties>ListID</Properties>
                        <Properties>Status</Properties>
                         <Filter xsi:type="SimpleFilterPart">
                           <Property>ListID</Property>
                           <SimpleOperator>equals</SimpleOperator>
                           <Value>{listId}</Value>
                        </Filter>
                     </RetrieveRequest>
                  </RetrieveRequestMsg>
                </s:Body>
            </s:Envelope>'''

        headers = {'Content-Type': 'application/soap+xml'}

        data = payload.format(auth_token=self.auth_token, listId=listId, service_url=service_url)

        response = requests.request("POST", url=service_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.text

        elif response.status_code >= 500: #TODO: less hacked-together reauth
            self.get_auth_token()
            data = payload.format(auth_token=self.auth_token, listId=listId, service_url=service_url)
            response = requests.request("POST", url=service_url, headers=headers, data=data)
            return response.text

    def update_list_subscribers(self, listId, subscriberData, attribute):
        """
        listId -- points to where to put the subscribers
        subscriberData -- df or dictionary of emailaddress + attribute(s) values.
        attribute -- just 1 attribute right now.
        """

        service_url = self.service_url

        # batch the data - create a list of lists of dictionaries in 200 chunks
        subscriberData_batchlists = self.create_batch(list=subscriberData, chunksize=200) # list of lists of dicts

        response_list=[]

        for batchlist in subscriberData_batchlists: # for each list of dicts
            batch_payload_list = []
            for each in batchlist: # for each dict in list
                subscriber_email = list(each.keys())[0]
                attribute_value = list(each.values())[0]

                # batch_payload = '''<EmailAddress>{subscriber_email}</EmailAddress>
                #     <SubscriberKey>{subscriber_email}</SubscriberKey>
                #     <Status>Active</Status>
                #     <Attributes>
                #         <Name>{attribute}</Name>
                #         <Value>{attribute_value}</Value>
                #     </Attributes>'''

                batch_payload = '''<Objects xsi:type="Subscriber">
                <partnerkey xsi:nil="true"></partnerkey>
                <objectid xsi:nil="true"></objectid>
                <EmailAddress>{subscriber_email}</EmailAddress>
                    <SubscriberKey>{subscriber_email}</SubscriberKey>
                    <Status>Active</Status>
                    <Attributes>
                        <Name>{attribute}</Name>
                        <Value>{attribute_value}</Value>
                    </Attributes>
                    <Lists>
                        <partnerkey xsi:nil="true"></partnerkey>
                        <ID>{listId}</ID>
                        <Action>Upsert</Action>
                        <Status>Active</Status>
                        </Lists>
                    </Objects>'''

                batch_payload = batch_payload.format(subscriber_email=subscriber_email,
                                                     attribute=attribute,
                                                     attribute_value=attribute_value,
                                                     listId=listId)
                batch_payload_list.append(batch_payload) #append payload to list
            batched_payload = '\n'.join(batch_payload_list) #flatten


            truncated_payload = '''<?xml version="1.0" encoding="UTF-8"?>
                <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                   <s:Header>
                      <a:Action s:mustUnderstand="1">Create</a:Action>
                      <a:MessageID>urn:uuid:7e0cca04-57bd-4481-864c-6ea8039d2ea0</a:MessageID>
                      <a:ReplyTo>
                         <a:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
                      </a:ReplyTo>
                      <a:To s:mustUnderstand="1">{service_url}</a:To>
                      <a:fueloauth>{auth_token}</a:fueloauth>
                   </s:Header>
                    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    <UpdateRequest xmlns="http://exacttarget.com/wsdl/partnerAPI">
                       {batched_payload}
                    </UpdateRequest>
                    </s:Body>
                </s:Envelope>'''

            if self.auth_token == '':
                self.get_auth_token()

            data = truncated_payload.format(auth_token=self.auth_token,
                                            batched_payload=batched_payload,
                                            service_url=service_url)


            headers = {'soapAction': 'Update', 'Content-Type': 'application/soap+xml'}
            response = requests.request("POST", url=service_url, headers=headers, data=data)

            # TODO: CANNOT rely only on 200 response, will actually need to parse the output to make sure user was added.
            if response.status_code == 200:
                response_list.append(response.text)

            elif response.status_code >= 500: #TODO: less hacked-together reauth
                self.get_auth_token()
                response = requests.request("POST", url=service_url, headers=headers, data=data)
                response_list.append(response.text)

        return response_list

    # def continueRequest(self):
        
    def get_unsubscribers(self):
        '''retrieve subscribers from list'''
        service_url = self.service_url

        if self.auth_token == '':
            self.get_auth_token()

        payload = '''<?xml version="1.0" encoding="UTF-8"?>
            <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
               <s:Header>
                  <a:Action s:mustUnderstand="1">Retrieve</a:Action>
                  <a:MessageID>urn:uuid:7e0cca04-57bd-4481-864c-6ea8039d2ea0</a:MessageID>
                  <a:ReplyTo>
                     <a:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
                  </a:ReplyTo>
                  <a:To s:mustUnderstand="1">{service_url}</a:To>
                  <a:fueloauth>{auth_token}</a:fueloauth>
               </s:Header>
                <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
                     <RetrieveRequest>
                        <ObjectType>Subscriber</ObjectType>
                        <Properties>SubscriberKey</Properties>
                        <Properties>UnsubscribedDate</Properties>
                         <Filter xsi:type="SimpleFilterPart">
                           <Property>Status</Property>
                           <SimpleOperator>equals</SimpleOperator>
                           <Value>Unsubscribed</Value>
                        </Filter>
                     </RetrieveRequest>
                  </RetrieveRequestMsg>
                </s:Body>
            </s:Envelope>'''

        headers = {'Content-Type': 'application/soap+xml'}

        data = payload.format(auth_token=self.auth_token, service_url=service_url)

        response = requests.request("POST", url=service_url, headers=headers, data=data)

        response_xml = ET.ElementTree(ET.fromstring(response.content))

        if response.status_code == 200:
            # parse results function
            # continue request
            if self.parse_xml_tag(response=response, tag='OverallStatus') == 'MoreDataAvailable':
                # do a continue request with requestID
                RequestID = self.parse_xml_tag(response=response, tag='RequestID')
                # submit continue request



            return response.text

        # https://salesforce.stackexchange.com/questions/88128/continuerequest-within-the-soap-envelope
        # TODO: store response
        # TODO: parse response to see if there is OverallStatus == 'MoreDataAvailable', if so get request ID
        # TODO: submit a 'continuerequest' using request ID

        elif response.status_code >= 500: #TODO: less hacked-together reauth
            self.get_auth_token()
            data = payload.format(auth_token=self.auth_token, service_url=service_url)
            response = requests.request("POST", url=service_url, headers=headers, data=data)


            return response.text

    def create_batch(self, list, chunksize):
        """splits list into list of chunksized lists"""
        for i in range(0, len(list), chunksize):
            yield list[i:i + chunksize]

    def parse_xml_tag(self, response, tag):
        response_xml = ET.ElementTree(ET.fromstring(response.content))

        tag_text = [child.text for child in response_xml.iter('*') if tag in child.tag]

        return tag_text

    def parse_todf(self, response, tag1, tag2, tag_gap):
        '''
        interim parsing to extract 2 desired, linked tags or attributes in xml response
        tag 1: first tag/attribute
        tag 2: second tag/attribute
        tag_gap: rough way of doing this but number of fields/other tags in between each tag.
        '''
        response_xml = ET.ElementTree(ET.fromstring(response.content))

        list1 = [(i,child.text) for i,child in enumerate(response_xml.iter('*')) if tag1 in child.tag]
        indexlist = [each[0] for each in list]
        list2 = [(i - tag_gap, child.text) for i, child in enumerate(response_xml.iter('*')) if
                 tag2 in child.tag and i - tag_gap in indexlist]

        df1 = pd.DataFrame(list1,columns=['key',{tag1}])
        df2 = pd.DataFrame(list2, columns=['key',{tag2}])
        df3 = df1.merg(df2, how='inner', on='key')

        return df3

service_url = "https://mc4yt73g8c8xzx6wnl5r43v67dwq.soap.marketingcloudapis.com/Service.asmx"
auth_url = "https://mc4yt73g8c8xzx6wnl5r43v67dwq.auth.marketingcloudapis.com"
clientId = "b8xymdu28fzxfdsd5veb7zew"
clientSecret = "rxcy0Qza80R4LdSxFUBeT3Tw"
test_listId = '56587'

obj=SalesforceSOAP(clientId=clientId,clientSecret=clientSecret,auth_url=auth_url,service_url=service_url)
unsub_response = obj.get_unsubscribers()
print(unsub_response)