import pandas as pd
import json
from flatdict import FlatDict
from pandas.io.json import json_normalize
from datetime import datetime, timedelta, date
import numpy as np

# standard columns
## add additional as needed for specific transform requirements + end table
standard_columns = ['event_date',
                 'event_timestamp',
                 'event_name',
                 'event_previous_timestamp',
                 'event_bundle_sequence_id',
                 'event_server_timestamp_offset',
                 'user_id',
                 'user_pseudo_id',
                 'user_first_touch_timestamp',
                 'stream_id',
                 'platform',
                 'item_id',
                 'content_type',
                 'firebase_screen',
                 'engaged_session_event',
                 'firebase_event_origin',
                 'firebase_screen_id',
                 'ga_session_number',
                 'firebase_screen_class',
                 'firebase_previous_class',
                 'firebase_previous_screen',
                 'engagement_time_msec',
                 'ga_session_id',
                 'user_ltv_revenue',
                 'user_ltv_currency',
                 'event_value_in_usd',
                 'ecommerce_total_item_quantity',
                 'ecommerce_unique_items',
                 'device_category',
                 'device_mobile_brand_name',
                 'device_mobile_model_name',
                 'device_mobile_os_hardware_model',
                 'device_operating_system',
                 'device_operating_system_version',
                 'device_advertising_id',
                 'device_language',
                 'device_is_limited_ad_tracking',
                 'device_time_zone_offset_seconds',
                 'geo_continent',
                 'geo_country',
                 'geo_region',
                 'geo_city',
                 'geo_sub_continent',
                 'geo_metro',
                 'app_info_id',
                 'app_info_version',
                 'app_info_firebase_app_id',
                 'app_info_install_source',
                 'traffic_source_medium',
                 'traffic_source_source',
                 'added_on']


# general functions
def json_to_df(file):
    '''transforms nested json file into dataframe'''
    event_list = []

    with open(file) as f:
        for j in f:
            event = json.loads(j)
            event_list.append(event)

    for i in range(len(event_list)):
        event = event_list[i]

        if 'event_params' in event.keys():
            params = event['event_params']
            params_unwrap = {}
            for p in params:
                params_unwrap.update({p['key']: list(p['value'].values())[0]})
            # del event['event_params']
            event.update(params_unwrap)

        if 'user_properties' in event.keys():
            # properties = event['user_properties']
            # properties_unwrap = {}
            # for p in properties:
            #     properties_unwrap.update({p['key']: list(p['value'].values())[0]})
            #     properties_unwrap.update({f"{p['key']}_timestamp": list(p['value'].values())[1]})
            del event['user_properties']
            # event.update(properties_unwrap)

        if 'items' in event.keys():
            # items = event['items']
            del event['items']
            # if not items:
            #     pass
            # else:
            #     event.update(items[0])

        event = FlatDict(event)
        rename_keys = [key.replace(':', '_') for key in event.keys()]
        event = dict(zip(rename_keys, list(event.values())))
        event_list[i] = event
        print(f'{i + 1}/{len(event_list)} rows complete.', end='\r')

    df = json_normalize(event_list)

    return df

def transform_initial(df):
    df1 = df[df['platform'] != 'WEB'].copy()

    columns = df1.columns
    renamedColumns = ['final_' + each for each in columns]
    renamedColumnMapping = dict(zip(columns, renamedColumns))

    df1 = df1.rename(columns=renamedColumnMapping)
    df1.dropna(how='all', inplace=True)
    df1['added_on'] = datetime.now().strftime('%Y-%m-%d')

    return df1

def transform_prefinal(df):
    df.drop(columns=['final_event_params','final_user_properties','final_items','index'], errors='ignore', inplace=True)
    df.replace(to_replace='[]', value='', inplace=True)
    df.replace(to_replace=':', value='-', inplace=True)
    df.columns = df.columns.str.replace('final_','')

    return df

def drop_irrelevant_columns(df, final_columns):
    irrelevant_columns = [each for each in df.columns if each not in final_columns]
    if irrelevant_columns:
        df = df.drop(columns=irrelevant_columns)
        return df
    else:
        print('no columns to drop')

# funnel-specific functions
def transform_ecomm(df):
    df_ecomms = df[df['final_event_name'] == 'ecommerce_purchase'].copy()
    # try:
    #     df_ecomms.drop(columns='engagement_time_msec', inplace=True)
    # except:
    #     pass
    df_ecomms = df_ecomms.reset_index()

    return df_ecomms

def transform_rf_selectcontent(df):
    df_selectcontents = df[df['final_event_name'] == 'select_content'].copy()
    df_selectcontents = df_selectcontents.reset_index()
    df_selectcontents['funnel_phase'] = df['final_content_type']
    df_final = df_selectcontents[df_selectcontents['funnel_phase'].str.startswith('rf_') == True]

    return df_final

def transform_rf_viewsearch(df):
    df_viewsearch = df[df['final_event_name'] == 'view_search_results'].copy()
    df_viewsearch = df_viewsearch.reset_index()
    df_viewsearch['start_date'] = df_viewsearch['final_start']
    df_viewsearch['end_date'] = df_viewsearch['final_end']
    df_viewsearch['funnel_phase'] = 'rf_viewsearchresults'

    return df_viewsearch

def transform_rf_addtocart(df):
    df_a2c = df[(df['final_event_name'] == 'add_to_cart') | (df['final_event_name'] == 'remove_from_cart')].copy()
    df_a2c = df_a2c.reset_index()
    df_a2c['final_prepay'] = df_a2c['final_prepaid']
    df_a2c['funnel_phase'] = 'rf_' + df_a2c['final_event_name']

    return df_a2c

def transform_checkout_progress(df):
    df_cp = df[df['final_event_name'] == 'checkout_progress'].copy()
    df_cp = df_cp.reset_index()
    df_cp['final_item_category'] = df['final_checkout_option']

    return df_cp

def transform_funnel_finalclean(df):
    df = transform_prefinal(df)
    final_columns = standard_columns.copy()
    final_columns.extend(['selected_item', 'funnel_phase', 'transaction_id'])
    df = drop_irrelevant_columns(df=df, final_columns=final_columns)

    return df

# other events
def transform_coupons(df):
    df1 = df[df['final_event_name'].isin(['enable_or_disable_coupons','delete_coupons']) == True].copy()
    df1.dropna(axis=1, how='all', inplace=True)
    df1 = transform_prefinal(df1)
    final_columns = standard_columns.copy().extend(['coupon_name', 'did_enable'])
    df1 = drop_irrelevant_columns(df=df1, final_columns=final_columns)

    return df1

def transform_cancellations(df):
    df1 = df[df['final_event_name'] == 'reservation_cancel'].copy()
    df1.dropna(axis=1, how='all', inplace=True)
    df1 = transform_prefinal(df1)
    final_columns = standard_columns.copy()
    final_columns.extend(['location', 'transaction_id'])
    df1 = drop_irrelevant_columns(df=df1, final_columns=final_columns)

    return df1

def transform_corporateaccount(df):
    df1 = df[df['final_event_name'] == 'add_corporate_account'].copy()
    df1.dropna(axis=1, how='all', inplace=True)
    df1 = transform_prefinal(df1)
    final_columns = standard_columns.copy()
    final_columns.extend(['account_code'])
    df1 = drop_irrelevant_columns(df=df1, final_columns=final_columns)

    return df1

def transform_login(df):
    df1 = df[df['final_event_name'] == 'login'].copy()
    df1.dropna(axis=1, how='all', inplace=True)
    df1 = transform_prefinal(df1)
    final_columns = standard_columns.copy()
    final_columns.extend(['method'])
    df1 = drop_irrelevant_columns(df=df1, final_columns=final_columns)

    return df1

def transform_tutorial(df):
    df1 = df[df['final_event_name'].isin(['tutorial_complete','tutorial_begin']) == True].copy()
    df1.dropna(axis=1, how='all', inplace=True)
    df1 = transform_prefinal(df1)
    final_columns = standard_columns.copy()
    final_columns.extend(['completed'])
    df1 = drop_irrelevant_columns(df=df1, final_columns=final_columns)

    return df1

def transform_signup(df):
    df1 = df[df['final_event_name'] == 'sign_up'].copy()
    df1.dropna(axis=1, how='all', inplace=True)
    df1 = transform_prefinal(df1)
    final_columns = standard_columns.copy()
    final_columns.extend(['preferred_facility'])
    df1 = drop_irrelevant_columns(df=df1, final_columns=final_columns)
    if 'event_previous_timestamp' not in df1.columns:
        df1['event_previous_timestamp'] = np.NaN

    return df1

def transform_screens(df):
    df1 = df[df['final_event_name'].isin(['screen_view','session_start','app_open']) == True].copy()
    df1.dropna(axis=1, how='all', inplace=True)
    df1 = transform_prefinal(df1)
    final_columns = standard_columns.copy()
    final_columns.extend(['entrances'])
    df1 = drop_irrelevant_columns(df=df1, final_columns=final_columns)

    return df1
