import requests
import calendar
import time
import secret_vars
import json
import pandas as pd


# Define the base API
# base = 'https://tools.brightlocal.com/seo-tools/api'
# version = 'v4'
max_expiry = 1800

expiry = calendar.timegm(time.gmtime()) + max_expiry
key = secret_vars.key
secret = secret_vars.secret


def get_locations():
    # Hits the location API and returns it as a pandas dataframe
    locations = 'https://tools.brightlocal.com/seo-tools/api/v1/clients-and-locations/locations/search'
    r = requests.get(locations, params={'api-key': key, "expires": expiry})
    response = json.loads(r.text)

    df = pd.DataFrame(response['locations'])
    df['location'] = df['location-reference'].str.split('-', expand=True)[0]

    return df


def get_report_ids():
    # get report ids for all things done (
    r = requests.get('https://tools.brightlocal.com/seo-tools/api/v4/rf', params={'api-key': key, "expires":expiry})
    response = json.loads(r.text)

    report_ids = []

    for report in response['reports']:
        if report['complete'] == True:
            report_ids.append(report['report_id'])

    return report_ids


def get_review_counts(report_ids):
    # Get the total number of reviews. This will feed the pagnation in the review extract. Returns dict of counts.
    counts = {}

    for id in report_ids:
        url = f'https://tools.brightlocal.com/seo-tools/api/v4/rf/{id}/reviews/count'
        r = requests.get(url, params={'api-key': key, "expires": expiry})
        response = json.loads(r.text)
        counts[id] = int(response['count'])

    return counts


def get_reviews(report_ids):
    # gets all the reviews and puts them in a pandas dataframe.
    df = pd.DataFrame()

    for id in report_ids:
        url = f'https://tools.brightlocal.com/seo-tools/api/v4/rf/{id}/reviews'
        r = requests.get(url, params={'api-key': key, "expires": expiry, 'limit': 100})
        response = json.loads(r.text)
        df_id = pd.DataFrame(response['reviews'])
        df_id['loc_id'] = id
        df = df.append(df_id)

    return df


def testing():
    result = get_reviews(get_report_ids())
    return result