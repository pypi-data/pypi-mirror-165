import datetime
import time
import uuid
import hmac
import hashlib



class Journera:
    """
    A class to create authentication and payloads for Journera API.

    Based on https://api.docs.journera.com/overview.html
    """
    def __init__(self, ClientSecretKey, ClientAccessKey):
        self.clientsecret = ClientSecretKey
        self.clientkey = ClientAccessKey
        self.action = 'POST'

    def create_StringToSign(self, method='POST', requestpath='/publish/v1/events', timestamp=None, nonce=None):
        """
        Create signing string.

        Parameters:
            method: will only be POST for Journera.
            requestpath: varies for stage or prod, default is prod
            timestamp (int): UNIX timestamp
            nonce: 1-time generated unique HEX value
        """
        if timestamp is None:
            timestamp = str(int(time.time()))  # unix timestamp rounded to closest int
        if nonce is None:
            nonce = str(uuid.uuid4())  # generate nonce

        StringToSign = f'{method}\n{requestpath}\n{timestamp}\n{nonce}\n'

        return StringToSign

    def create_auth(self, method='POST', requestpath='/publish/v1/events', timestamp=None, nonce=None):

        if timestamp is None:
            timestamp = str(int(time.time()))  # unix timestamp rounded to closest int
        if nonce is None:
            nonce = str(uuid.uuid4())  # generate nonce

        # create UTF-8 encoded keys & signing string
        encodedSigningString = self.create_StringToSign(method=method,
                                                              requestpath=requestpath,
                                                              timestamp=timestamp,
                                                              nonce=nonce)

        signature = hmac.new(bytes(self.clientsecret, 'UTF-8'),
                             bytes(encodedSigningString, 'UTF-8'),
                             hashlib.sha256).hexdigest()

        auth = f'hmac ck={self.clientkey},ts={timestamp},n={nonce},sig={signature}'
        # auth = 'hmac ck=%s,ts=%s,n=%s,sig=%s' % (args.key, timestamp, nonce, signature)

        return auth

    @staticmethod
    def generate_eventpackage(customerid,
                              action,
                              firstname=None,
                              lastname=None,
                              address1=None,
                              address2=None,
                              city=None,
                              state=None,
                              zip=None,
                              addressLabel=None,
                              email=None,
                              emailLabel=None,
                              phone=None,
                              phoneLabel=None,
                              ):
        # create list of dicts

        customerid = str(customerid)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')+'Z' # ISO  format
        if action == 'delete':
            event_package = [
                {
                 "Type": "CustomerName",
                 "Action": action,
                 "Timestamp": timestamp,
                 "CustomerId": customerid,
                 "EventData": {
                    "First": firstname,
                    "Last": lastname
                    }
                },
                {
                    "Type": "CustomerAddress",
                    "Action": action,
                    "Timestamp": timestamp,
                    "CustomerId": customerid,
                    "EventData": {
                        "Line1": address1,
                        "Line2": address2,
                        "City": city,
                        "State": state,
                        "PostalCode": zip,
                        "Label": addressLabel
                    }
                },
                {
                 "Type": "CustomerEmail",
                 "Action": action,
                 "Timestamp": timestamp,
                 "CustomerId": customerid,
                 "EventData": {
                    "Email": email,
                    "Label": emailLabel
                    }
                },
                {
                 "Type": "CustomerPhone",
                 "Action": action,
                 "Timestamp": timestamp,
                 "CustomerId": customerid,
                 "EventData": {
                    "Number": phone,
                    "Label": phoneLabel
                    }
                }
            ]
        elif action == 'add':
            event_package = [
                {
                 "Type": "CustomerName",
                 "Timestamp": timestamp,
                 "CustomerId": customerid,
                 "EventData": {
                    "First": firstname,
                    "Last": lastname
                    }
                },
                {
                    "Type": "CustomerAddress",
                    "Timestamp": timestamp,
                    "CustomerId": customerid,
                    "EventData": {
                        "Line1": address1,
                        "Line2": address2,
                        "City": city,
                        "State": state,
                        "PostalCode": zip,
                        "Label": addressLabel
                    }
                },
                {
                 "Type": "CustomerEmail",
                 "Timestamp": timestamp,
                 "CustomerId": customerid,
                 "EventData": {
                    "Email": email,
                    "Label": emailLabel
                    }
                },
                {
                 "Type": "CustomerPhone",
                 "Timestamp": timestamp,
                 "CustomerId": customerid,
                 "EventData": {
                    "Number": phone,
                    "Label": phoneLabel
                    }
                }
            ]
        return event_package

    @staticmethod
    def generate_eventpackage_deletion(customerid,
                                          action,
                                          firstname=None,
                                          lastname=None
                                          ):
        # create list of dicts

        customerid = str(customerid)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')+'Z' # ISO  format
        if action == 'delete':
            event_package = [
                {
                 "Type": "CustomerName",
                 "Action": action,
                 "Timestamp": timestamp,
                 "CustomerId": customerid,
                 "EventData": {
                    "First": firstname,
                    "Last": lastname
                    }
                }
            ]
        # elif action == 'delete' and firstname is None and lastname is None:
        #     event_package = [
        #         {
        #             "Type": "CustomerName",
        #             "Action": action,
        #             "Timestamp": timestamp,
        #             "CustomerId": customerid,
        #         }
        #     ]
        return event_package