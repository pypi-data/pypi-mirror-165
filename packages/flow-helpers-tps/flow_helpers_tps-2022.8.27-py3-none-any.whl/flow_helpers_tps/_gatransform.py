import pandas as pd
import json
import datetime


def column_rename(df):
    """rename columns"""
    df['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('ga:', '')
    df.replace("''", '(not set)')
    
    # for non-funnel
    df.rename(columns={
        'devicecategory': 'device_category',
        'operatingsystem': 'operating_system',
        'date': 'date_day',
        'users': 'user_count',
        'sessions': 'user_sessions',
        'bouncerate': 'bounce_rate',
        'avgsessionduration': 'avg_session_duration',
        'pageviews': 'page_views',
        'pageviewspersession': 'pages_per_session',
        'pagepath': 'page_path',
        'uniquepageviews': 'unique_page_views',
        'timeonpage': 'time_on_page',
        'datehourminute': 'transaction_ts',
        'productcategory': 'product_category',
        'productname': 'product_name',
        'productsku': 'product_sku',
        'fullreferrer': 'full_referrer',
        'referralpath': 'referral_path',
        'socialnetwork': 'social_network',
        'transactionrevenue': 'transaction_revenue'
    }, inplace=True)

    return df


def column_cast(df):
    cols=[
        'user_count',
        'user_sessions',
        'bounce_rate',
        'avg_session_duration',
        'page_views',
        'pages_per_session',
        'unique_page_views',
        'time_on_page',
        'transaction_revenue',
        'bounces',
        'entrances',
        'exits'
    ]

    for each in cols:
        if each in df.columns:
            df[each] = df[each].astype('float64')

    return df


def regex_campaign(r):
    """transform campaign nomenclature"""

    if r['ga:medium'] != 'cpc':
        return r
    elif isinstance(r['ga:campaign'], str):
        string = r['ga:campaign'].split('_')
    else:
        return r

    if string[0] == 'TPS':
        r['market'] = string[1]
        r['branded'] = string[4]
        r['exact'] = string[5]
    else:
        r['market'] = 'Unable to Parse'
        r['branded'] = string[0][0:8]

        if 'Exact' in r['ga:campaign']:
            r['exact'] = 'Exact'
        elif 'Broad' in r['ga:campaign']:
            r['exact'] = 'Broad'
        else:
            r['exact'] = 'Unable to Parse'

    return r


# reservation funnel transformation functions
def ParkingOptionsDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_dict(r)

        v = p['displayedPrices'].str.split('|', expand=True)
        p.drop('displayedPrices', axis=1, inplace=True)

        pl = pd.concat([p, v], axis=1)

        try:
            pl.drop('sessionID', axis=1, inplace=True)
        except KeyError:
            pass
        except ValueError:
            pass

        details.append(pl)

    prices = pd.concat(details)
    prices.rename(columns = {
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        0:'market',
        1:'facilityParkingID',
        2:'price',
        3:'pricing_frequency',
        4:'discount_amount',
        5:'discount_display_name',
        6:'enabled',
        7:'method',
        8:'reason' #test this
        }, inplace = True)


    prices['market'] = prices['market'].str.strip()
    prices['facilityParkingID'] = prices['facilityParkingID'].astype(int)
    prices['price'] = prices['price'].str.strip()
    prices['price']=prices['price'].str.replace(',','')
    prices['price']=prices['price'].str.replace('NULL','')
    prices['price']=prices['price'].str.replace('$','')
    prices['price']=prices['price'].str.extract('(\d+)').astype(float)
    prices['pricing_frequency'] = prices['pricing_frequency'].str.strip()

    # fixme: Single digit percentage discounts have a strange 'f' string
    prices['discount_amount'] = prices['discount_amount'].str.strip()
    prices['discount_amount'] = prices['discount_amount'].str.replace('f ','') #trying to clean out the 'f' string mentioned earlier.
    prices['discount_amount'].replace('NULL', '', inplace=True)

    prices['discount_display_name'] = prices['discount_display_name'].str.strip()
    prices['discount_display_name'].replace('NULL', '', inplace=True)
    prices['discount_display_name'].replace('disabled', '', inplace=True)

    prices['enabled'] = prices['enabled'].str.strip()
    prices['enabled'].replace('disabled', 0, inplace=True)
    prices.loc[prices['enabled'] != 0, 'enabled'] = True
    prices.loc[prices['enabled'] == 0, 'enabled'] = False

    prices['event_timestamp'] = pd.to_datetime(prices['event_timestamp'])
    prices['customer_id'] = prices['customer_id'].str.replace('NULL', '')
    prices['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return prices


def selectedProduct(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])
        v = p['selectedProduct'].str.split('|', expand=True)
        p.drop('selectedProduct', axis=1, inplace=True)

        pl = pd.concat([p, v], axis=1)

        try:
            pl.drop('sessionID', axis=1, inplace=True)
        except KeyError:
            pass
        except ValueError:
            pass

        details.append(pl)

    choices = pd.concat(details)
    choices.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        0: 'market',
        1: 'facilityParkingID',
        2: 'method',
    }, inplace=True)

    choices['market'] = choices['market'].str.strip()
    choices['facilityParkingID'] = choices['facilityParkingID'].astype(int)
    choices['event_timestamp'] = pd.to_datetime(choices['event_timestamp'])
    choices['customer_id'] = choices['customer_id'].str.replace('NULL', '')
    choices['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    choices_sorted = choices[['browser_id', 'customer_id', 'event_timestamp', 'method', 'market', 'facilityParkingID', 'promoCampaignCode', 'date_added']]

    return choices_sorted


def airportSelected(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    airports = pd.concat(details)
    airports.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        'airportID': 'airport_id',  #
        'airportName': 'airport_code'}, inplace=True)

    # fixme: Sometimes a null airport ID is passed
    airports['airport_id'] = airports['airport_id'].fillna(0).astype(int)
    airports['event_timestamp'] = pd.to_datetime(airports['event_timestamp'])
    airports['customer_id'] = airports['customer_id'].replace('NULL', '')
    airports['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")


    return airports


def carCareOptionsDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_dict(r)

        v = p['displayedPrices'].str.split('|', expand=True)
        p.drop('displayedPrices', axis=1, inplace=True)

        pl = pd.concat([p, v], axis=1)

        try:
            pl.drop('sessionID', axis=1, inplace=True)
        except KeyError:
            pass
        except ValueError:
            pass

        details.append(pl)

    carcare = pd.concat(details)

    carcare.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        0: 'carcare_id',
        1: 'carcare_label',
        2: 'carcare_price'
    }, inplace=True)

    carcare['carcare_id'] = carcare['carcare_id'].astype(int)
    carcare['event_timestamp'] = pd.to_datetime(carcare['event_timestamp'])
    carcare['customer_id'] = carcare['customer_id'].str.replace('NULL', '')
    carcare.loc[carcare['carcare_price'].str.contains('undefined'), 'carcare_price'] = '0'
    carcare['carcare_price'] = carcare['carcare_price'].str.replace('$', '').astype(float)
    carcare['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return carcare


def loginAction(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    login = pd.concat(details)
    login.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)

    login['customer_id'] = login['customer_id'].str.replace('NULL', '')
    login['event_timestamp'] = pd.to_datetime(login['event_timestamp'])
    login['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return login


def reservationConfirmationDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    confirm = pd.concat(details)
    confirm.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        'reservationID': 'reservation_id'}, inplace=True)
    confirm['event_timestamp'] = pd.to_datetime(confirm['event_timestamp'])
    confirm['customer_id'] = confirm['customer_id'].replace('NULL', '')
    confirm['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return confirm


def reservationDetailsDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    resdetail = pd.concat(details)
    resdetail.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        'amountDueAtExit': 'due_at_exit',
        'amountDueNow': 'due_now',
        'carCareName': 'carcare_label',
        'carCarePrice': 'carcare_price',
        'reservationFee': 'reservation_fee',
        'totalDue': 'total_due'}, inplace=True)

    resdetail['event_timestamp'] = pd.to_datetime(resdetail['event_timestamp'])
    resdetail['customer_id'] = resdetail['customer_id'].replace('NULL', '')
    resdetail['carcare_label'] = resdetail['carcare_label'].str.replace('NULL', '')

    currency_columns = [
        'carcare_price',
        'due_at_exit',
        'due_now',
        'reservation_fee',
        'total_due',
    ]

    for col in currency_columns:
        try:
            resdetail[col] = resdetail[col].str.replace('NULL', '0')
            resdetail[col] = resdetail[col].str.replace('$', '').astype(float)
        except:
            resdetail[col] = resdetail[col].astype(float)

    resdetail['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return resdetail


def reservationSummaryDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    summary = pd.concat(details)
    summary.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)

    summary['event_timestamp'] = pd.to_datetime(summary['event_timestamp'])
    summary['customer_id'] = summary['customer_id'].replace('NULL', '')
    summary['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return summary


def selectedCarCare(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])
        v = p['selectedProduct'].str.split('|', expand=True)
        p.drop('selectedProduct', axis=1, inplace=True)

        pl = pd.concat([p, v], axis=1)

        try:
            pl.drop('sessionID', axis=1, inplace=True)
        except KeyError:
            pass
        except ValueError:
            pass

        details.append(pl)

    select = pd.concat(details)
    select.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        0: 'carcare_id',
        1: 'carcare_label'}, inplace=True)

    select['event_timestamp'] = pd.to_datetime(select['event_timestamp'])
    select['customer_id'] = select['customer_id'].str.replace('NULL', '')
    select['carcare_id'] = select['carcare_id'].str.replace('NULL', '')
    select['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return select


def timesSelected(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])
        details.append(p)

    times = pd.concat(details)
    times.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        'checkInDate': 'checkin_date',
        'checkOutDate': 'checkout_date'}, inplace=True)

    times['checkin_date'] = pd.to_datetime(times['checkin_date'])
    times['checkout_date'] = pd.to_datetime(times['checkout_date'])
    times['event_timestamp'] = pd.to_datetime(times['event_timestamp'])
    times['customer_id'] = times['customer_id'].replace('NULL', '')
    times['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return times


def reservePageInstantiated(df):
    details = []

    for ix, row in df.iterrows():
        try:
            r = json.loads(row['ga:eventLabel'])
        except:
            errortoshow = row['ga:eventLabel']
            print({ix}, row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    instantiate = pd.concat(details)
    instantiate.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        0: 'previousPage'}, inplace=True)

    instantiate['event_timestamp'] = pd.to_datetime(instantiate['event_timestamp'])
    instantiate['customer_id'] = instantiate['customer_id'].replace('NULL', '')
    instantiate['previousPage'] = instantiate['previousPage'].replace('^\?.*','') #remove any gclids, etc.
    instantiate['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return instantiate


def loginDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    logindisplay = pd.concat(details)
    logindisplay.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)

    logindisplay['event_timestamp'] = pd.to_datetime(logindisplay['event_timestamp'])
    logindisplay['customer_id'] = logindisplay['customer_id'].replace('NULL', '')
    logindisplay['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return logindisplay


def contactInfoDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    contactInfoDisplay = pd.concat(details)
    contactInfoDisplay.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)

    contactInfoDisplay['event_timestamp'] = pd.to_datetime(contactInfoDisplay['event_timestamp'])
    contactInfoDisplay['customer_id'] = contactInfoDisplay['customer_id'].replace('NULL', '')
    contactInfoDisplay['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return contactInfoDisplay


def compareFacilitiesDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    compareFacilitiesDisplay = pd.concat(details)
    compareFacilitiesDisplay.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        0: 'market'}, inplace=True)
    compareFacilitiesDisplay['event_timestamp'] = pd.to_datetime(compareFacilitiesDisplay['event_timestamp'])
    compareFacilitiesDisplay['customer_id'] = compareFacilitiesDisplay['customer_id'].replace('NULL', '')
    compareFacilitiesDisplay['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return compareFacilitiesDisplay


def payInfoDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    payInfoDisplay = pd.concat(details)
    payInfoDisplay.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)

    payInfoDisplay['event_timestamp'] = pd.to_datetime(payInfoDisplay['event_timestamp'])
    payInfoDisplay['customer_id'] = payInfoDisplay['customer_id'].replace('NULL', '')
    payInfoDisplay['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return payInfoDisplay


def pointsSectionDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    pointsSectionDisplay = pd.concat(details)
    pointsSectionDisplay.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)
    pointsSectionDisplay['event_timestamp'] = pd.to_datetime(pointsSectionDisplay['event_timestamp'])
    pointsSectionDisplay['customer_id'] = pointsSectionDisplay['customer_id'].replace('NULL', '')
    pointsSectionDisplay['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return pointsSectionDisplay


def upsellDisplay(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    upselldisplay = pd.concat(details)
    upselldisplay.rename(columns={  # verify these
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        'isPopup': 'isPopup'}, inplace=True)
    upselldisplay['event_timestamp'] = pd.to_datetime(upselldisplay['event_timestamp'])
    upselldisplay['customer_id'] = upselldisplay['customer_id'].replace('NULL', '')
    upselldisplay['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return upselldisplay


# TODO: BACKFILL
def upsellClicked(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    upsellclicked = pd.concat(details)
    upsellclicked.rename(columns={  # verify these
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id',
        'isPopup': 'isPopup'}, inplace=True)
    upsellclicked['event_timestamp'] = pd.to_datetime(upsellclicked['event_timestamp'])
    upsellclicked['customer_id'] = upsellclicked['customer_id'].replace('NULL', '')
    upsellclicked['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return upsellclicked


# TODO: BACKFILL
def upsellUndoClicked(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    upsellundoclicked = pd.concat(details)
    upsellundoclicked.rename(columns={
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)

    upsellundoclicked['event_timestamp'] = pd.to_datetime(upsellundoclicked['event_timestamp'])
    upsellundoclicked['customer_id'] = upsellundoclicked['customer_id'].replace('NULL', '')
    upsellundoclicked['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return upsellundoclicked


def promoCampaignCodeEntered(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    promo = pd.concat(details)
    promo.rename(columns={
        'promoCampaignCode': 'promoCode',
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)

    promo['event_timestamp'] = pd.to_datetime(promo['event_timestamp'])
    promo['customer_id'] = promo['customer_id'].replace('NULL', '')
    promo['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return promo


def reservationUpsellCampaign(df):
    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['ga:eventLabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        p = pd.DataFrame.from_records(r, index=[0])

        details.append(p)

    upsellcampaign = pd.concat(details)
    upsellcampaign.rename(columns={
        'reservationID': 'reservation_id',
        'upsellCampaignID': 'upsellCampaign_id',
        'browserID': 'browser_id',
        'eventTimestamp': 'event_timestamp',
        'customerID': 'customer_id'}, inplace=True)

    upsellcampaign['event_timestamp'] = pd.to_datetime(upsellcampaign['event_timestamp'])
    upsellcampaign['customer_id'] = upsellcampaign['customer_id'].replace('NULL', '')
    upsellcampaign['date_added'] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")

    return upsellcampaign

def devicebrowsermatch(df):
    df = column_rename(df)

    df = df[df['eventlabel'] != '(other)']

    details = []

    for ix, row in df.iterrows():
        r = json.loads(row['eventlabel'])
        if 'customerID' not in r.keys():
            r['customerID'] = ''

        q = [{'index': ix,
              'browserID': r['browserID'],
              'customerID': r['customerID'],
              'device_category': row['device_category'],
              'date_added': row['date_added']
              }]

        p = pd.DataFrame.from_records(q, index=[0])

        details.append(p)

    final_df = pd.concat(details)
    final_df.rename(columns={
        'browserID': 'browser_id',
        'customerID': 'customer_id'
    }, inplace=True)
    final_df.drop(labels='index', axis=1, inplace=True)
    final_df.drop_duplicates(inplace=True)

    return final_df