import pandas as pd


def entrypoint_label (row):
    # Homepage, Market, Airport, Facility, Reserve, Coupon, Account, All others
    if pd.isna(row['prev page']) is True:
        return 'reservation page'
    elif row['pagepath level 1'] == 'reserve':
        return 'reservation page'
    elif row['prev page'] == '/' and row['pagepath level 1'] == '':
        return 'homepage'
    elif row['pagepath level 1'] == 'account':
        return 'account pages'
    elif row['pagepath level 1'] == 'coupons':
        return 'coupons'
    elif row['pagepath level 1'] == 'locations' and pd.isna(row['pagepath level 2']) is True:
        return 'locations page'
    elif row['pagepath level 1'] == 'locations' and pd.isna(row['pagepath level 4']) is False:
        return 'facility pages'
    elif row['pagepath level 1'] == 'locations' and pd.isna(row['pagepath level 2']) is False and pd.isna(row['pagepath level 3']) is True:
        return 'market pages'
    elif row['pagepath level 1'] == 'locations' and pd.isna(row['pagepath level 3']) is False and pd.isna(row['pagepath level 4']) is True:
        return 'airport pages'
    elif row['pagepath level 1'] == 'promotions' and row['pagepath level 2'] == 'corporatehome':
        return 'corporate pages'
    elif row['pagepath level 1'] == 'promotions' and pd.isna(row['pagepath level 2']) is True:
        return 'promotions promocode page'
    # elif row['pagepath level 1'] == 'business':
    #     return 'business page'
#    elif row['pagepath level 1'] == 'promotions' and row['pagepath level 2']) == 'travelcoupon':
#        return 'promotions - travelcoupon'
    else:
        return 'Other'


def promopage_label(row):
    # pre
    if row['dt'] < pd.to_datetime('2021-3-16') and pd.isna(row['promo_promocode']) is False:
        return 'promotions page'

    # post
    elif row['promo pagepath level 1'] == 'reserve':
        return 'reservation page'
    elif row['promo_pg'] == '/' and row['promo pagepath level 1'] == '':
        return 'homepage'
    elif row['promo pagepath level 1'] == 'account':
        return 'account pages'
    elif row['promo pagepath level 1'] == 'coupons':
        return 'coupons'
    elif row['promo pagepath level 1'] == 'locations' and pd.isna(row['promo pagepath level 2']) is True:
        return 'locations page'
    elif row['promo pagepath level 1'] == 'locations' and pd.isna(row['promo pagepath level 4']) is False:
        return 'facility pages'
    elif row['promo pagepath level 1'] == 'locations' and pd.isna(row['promo pagepath level 2']) is False and pd.isna(
            row['promo pagepath level 3']) is True:
        return 'market pages'
    elif row['promo pagepath level 1'] == 'locations' and pd.isna(row['promo pagepath level 3']) is False and pd.isna(
            row['promo pagepath level 4']) is True:
        return 'airport pages'
    elif row['promo pagepath level 1'] == 'promotions' and row['promo pagepath level 2'] == 'corporatehome':
        return 'corporate pages'
    elif row['promo pagepath level 1'] == 'promotions' and pd.isna(row['promo pagepath level 2']) == True:
        return 'promotions page'

    # post and none
    elif row['dt'] < pd.to_datetime('2021-3-16') and pd.isna(row['promo_promocode']) is False:
        return 'promotions page - no code entered'

    elif pd.isna(row['promo_promocode']) == True:
        return 'no code entered'

    else:
        return 'Other'

def reservation_completed(row):
    if pd.isna(row['RC_ct']) == True:
        return 'no'

    elif row['RC_ct'] == 0:
        return 'no'

    elif pd.isna(row['rc_discounttype']) == True:
        return 'no'

    else:
        return 'yes'


def promocode_entered(row):
    if pd.isna(row['promo_promocode']) == True:
        return 'no promocode entered'

    elif row['promo_promocode'] == '':
        return 'no promocode entered'

    else:
        return row['promo_promocode']


def promocode_applied(row):
    # pre
    if row['promocode entered'] == 'no promocode entered':
        return 'no promocode entered'

    elif pd.isna(row['promocode entered']) == True:
        return 'no promocode entered'

    elif row['dt'] <= pd.to_datetime('2021-3-16') and pd.isna(row['rc_promocode']) == True and row[
        'rc_discounttype'] == 'PromoCampaign':
        return row['promo_promocode']

    elif row['sp_promocode'] == 'DOES NOT APPLY':
        return 'code entered does not apply'

    elif row['rs_promocode'] == 'DOES NOT APPLY':
        return 'code entered does not apply'

    elif row['rc_promocode'] == 'DOES NOT APPLY':
        return 'code entered does not apply'

    elif pd.isna(row['rc_promocode']) == True and pd.isna(row['rs_promocode']) == False:
        return row['rs_promocode']

    elif pd.isna(row['rc_promocode']) == True and pd.isna(row['rs_promocode']) == True and pd.isna(row['sp_promocode']) == False:
        return row['sp_promocode']

    else:
        return row['rc_promocode']


def entrypoint_transform(df):
    # basic funnel v1.0 w/ entrypoints
    # general funnel transform for v1.0

    # setup
    df['prev page'] = df['instantiate_previouspage']
    df.drop(columns=['instantiate_previouspage'], inplace=True)

    # select relevant records
    df1 = df.loc[df['prev page'].str.match('https://theparkingspot\.com|https://www.theparkingspot\.com') == True].copy()
    df2 = df.loc[df['prev page'].isna() == True].copy()
    df1 = pd.concat([df1, df2])

    # clean
    df1['prev page'] = df1['prev page'].str.lower()
    df1['prev page'] = df1['prev page'].str.replace('\?.*', '')
    df1['prev page'] = df1['prev page'].str.replace('www\.', '')
    df1['prev page'] = df1['prev page'].str.replace('https://', '')
    df1['prev page'] = df1['prev page'].str.replace('//', '/')
    df1['prev page'] = df1['prev page'].str.replace('theparkingspot.com', '')
    df1['prev page'] = df1['prev page'].str.replace('.aspx', '')
    df1['prev page'] = df1['prev page'].str.replace('#', '')
    values = {'rc_prepay': 'null', 'rc_discounttype': 'null'}
    df1 = df1.fillna(value=values)     # replace na with explicit 'null' string

    # create new columns for each level in the URL
    df1['pagepath level 1'] = df1['prev page'].str.split('/').str[1]
    df1['pagepath level 2'] = df1['prev page'].str.split('/').str[2]
    df1['pagepath level 3'] = df1['prev page'].str.split('/').str[3]
    df1['pagepath level 4'] = df1['prev page'].str.split('/').str[4]

    # apply categorization
    df1['entrypoint'] = df1.apply(lambda row: entrypoint_label(row), axis=1)
    df1['reservation completed'] = df1.apply(lambda row: reservation_completed(row), axis=1)
    df1.reset_index(inplace=True, drop=True)

    df1['dt'] = pd.to_datetime(df1['dt'])

    df_final = df1[['dt',
                   'entrypoint',
                   'pagepath level 1',
                   'pagepath level 2',
                   'pagepath level 3',
                   'pagepath level 4',
                   'rc_prepay',
                   'rc_discounttype',
                   'reservation completed',
                   'instantiate_ct',
                   'POD_ct',
                   'SP_ct',
                   'CCO_ct',
                   'SCC_ct',
                   'CID_ct',
                   'RS_ct',
                   'RC_ct']]

    return df_final


def promo_transform(df):

    # specify data
    df['prev page'] = df['instantiate_previouspage']
    df.drop(columns=['instantiate_previouspage'], inplace=True)
    df_w = df.loc[
        df['prev page'].str.match('https://theparkingspot\.com|https://www.theparkingspot\.com') == True].copy()
    df_w1 = df.loc[df['prev page'].isna() == True].copy()
    df1 = pd.concat([df_w, df_w1])

    # clean data
    df1['prev page'] = df1['prev page'].str.lower()
    df1['prev page'] = df1['prev page'].str.replace('\?.*', '')
    df1['prev page'] = df1['prev page'].str.replace('www\.', '')
    df1['prev page'] = df1['prev page'].str.replace('https://', '')
    df1['prev page'] = df1['prev page'].str.replace('//', '/')
    df1['prev page'] = df1['prev page'].str.replace('theparkingspot.com', '')
    df1['prev page'] = df1['prev page'].str.replace('.aspx', '')
    df1['prev page'] = df1['prev page'].str.replace('#', '')

    values = {'rc_prepay': 'null', 'rc_discounttype': 'null'}
    df1 = df1.fillna(value=values) # replace na with explicit 'null' string

    # create new columns
    df1['pagepath level 1'] = df1['prev page'].str.split('/').str[1]
    df1['pagepath level 2'] = df1['prev page'].str.split('/').str[2]
    df1['pagepath level 3'] = df1['prev page'].str.split('/').str[3]
    df1['pagepath level 4'] = df1['prev page'].str.split('/').str[4]

    df1['promo pagepath level 1'] = df1['promo_pg'].str.split('/').str[1]
    df1['promo pagepath level 2'] = df1['promo_pg'].str.split('/').str[2]
    df1['promo pagepath level 3'] = df1['promo_pg'].str.split('/').str[3]
    df1['promo pagepath level 4'] = df1['promo_pg'].str.split('/').str[4]

    df1['entrypoint'] = df1.apply(lambda row: entrypoint_label(row), axis=1)
    df1['reservation completed'] = df1.apply(lambda row: reservation_completed(row), axis=1)
    df1['promocode entrypoint'] = df1.apply(lambda row: promopage_label(row), axis=1)
    df1['promocode entered'] = df1.apply(lambda row: promocode_entered(row), axis=1)
    df1['promocode applied'] = df1.apply(lambda row: promocode_applied(row), axis=1)

    df1.reset_index(inplace=True, drop=True)
    df1['dt'] = pd.to_datetime(df1['dt'])

    df_final = df1[['dt',
                    'entrypoint',
                    'promocode entrypoint',
                    'promocode entered',
                    'promocode applied',
                    'promo_promocode',
                    'sp_promocode',
                    'rs_promocode',
                    'rc_promocode',
                    'rc_prepay',
                    'rc_discounttype',
                    'reservation completed',
                    'pagepath level 1',
                    'pagepath level 2',
                    'pagepath level 3',
                    'pagepath level 4',
                    'promo pagepath level 1',
                    'promo pagepath level 2',
                    'promo pagepath level 3',
                    'promo pagepath level 4',
                    'instantiate_ct',
                    'promo_ct',
                    'POD_ct',
                    'SP_ct',
                    'CCO_ct',
                    'SCC_ct',
                    'CID_ct',
                    'RS_ct',
                    'RC_ct']]

    return df_final

