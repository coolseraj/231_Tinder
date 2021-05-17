# coding=utf-8
import json
import time

import tinder_config_ex as config
import requests
import numpy as np
import urllib.request
import os
from os import listdir
from os.path import isfile, join
import xlsxwriter



get_headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
    "Accept": "application/json"
}
headers = get_headers.copy()
headers['content-type'] = "application/json"



"""def get_auth_token(fb_auth_token, fb_user_id):
    if "error" in fb_auth_token:
        return {"error": "could not retrieve fb_auth_token"}
    if "error" in fb_user_id:
        return {"error": "could not retrieve fb_user_id"}
    url = config.host + '/v2/auth/login/facebook'
    req = requests.post(url,
                        headers=headers,
                        data=json.dumps(
                            {'token': fb_auth_token, 'facebook_id': fb_user_id})
                        )
    try:
        tinder_auth_token = req.json()["data"]["api_token"]
        headers.update({"X-Auth-Token": tinder_auth_token})
        get_headers.update({"X-Auth-Token": tinder_auth_token})
        print("You have been successfully authorized!")
        return tinder_auth_token
    except Exception as e:
        print(e)
        return {"error": "Something went wrong. Sorry, but we could not authorize you."}
"""

def authverif():
    #res = get_auth_token(tinder_config_ex.fb_access_token, tinder_config_ex.fb_user_id)
    headers.update({"X-Auth-Token": config.tinder_token})
    get_headers.update({"X-Auth-Token": config.tinder_token})
    res = config.tinder_token
    if "error" in res:
        return False
    return True


def get_recommendations():
    '''
    Returns a list of users that you can swipe on
    '''
    try:
        r = requests.get('https://api.gotinder.com/user/recs', headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting recomendations:", e)

def likes_sent():
    try:
        r = requests.get('https://api.gotinder.com/v2/my-likes?locale=en', headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting recomendations:", e)


def get_updates(last_activity_date=""):
    '''
    Returns all updates since the given activity date.
    The last activity date is defaulted at the beginning of time.
    Format for last_activity_date: "2017-07-09T10:28:13.392Z"
    '''
    try:
        url = config.host + '/updates'
        r = requests.post(url,
                          headers=headers,
                          data=json.dumps({"last_activity_date": last_activity_date}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting updates:", e)


def get_self():
    '''
    Returns your own profile data
    '''
    try:
        url = config.host + '/profile'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your data:", e)


def change_preferences(**kwargs):
    '''
    ex: change_preferences(age_filter_min=30, gender=0)
    kwargs: a dictionary - whose keys become separate keyword arguments and the values become values of these arguments
    age_filter_min: 18..46
    age_filter_max: 22..55
    age_filter_min <= age_filter_max - 4
    gender: 0 == seeking males, 1 == seeking females
    distance_filter: 1..100
    discoverable: true | false
    {"photo_optimizer_enabled":false}
    '''
    try:
        url = config.host + '/profile'
        r = requests.post(url, headers=headers, data=json.dumps(kwargs))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not change your preferences:", e)


def get_meta():
    '''
    Returns meta data on yourself. Including the following keys:
    ['globals', 'client_resources', 'versions', 'purchases',
    'status', 'groups', 'products', 'rating', 'tutorials',
    'travel', 'notifications', 'user']
    '''
    try:
        url = config.host + '/meta'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your metadata:", e)

def get_meta_v2():
    '''
    Returns meta data on yourself from V2 API. Including the following keys:
    ['account', 'client_resources', 'plus_screen', 'boost',
    'fast_match', 'top_picks', 'paywall', 'merchandising', 'places',
    'typing_indicator', 'profile', 'recs']
    '''
    try:
        url = config.host + '/v2/meta'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your metadata:", e)

def update_location(lat, lon):
    '''
    Updates your location to the given float inputs
    Note: Requires a passport / Tinder Plus
    '''
    try:
        url = config.host + '/passport/user/travel'
        r = requests.post(url, headers=headers, data=json.dumps({"lat": lat, "lon": lon}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)

def reset_real_location():
    try:
        url = config.host + '/passport/user/reset'
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)


def get_recs_v2():
    '''
    This works more consistently then the normal get_recommendations becuase it seeems to check new location
    '''
    try:
        url = config.host + '/v2/recs/core?locale=en-US'
        r = requests.get(url, headers=headers)
        return r.json()
    except Exception as e:
        print('excepted')

def set_webprofileusername(username):
    '''
    Sets the username for the webprofile: https://www.gotinder.com/@YOURUSERNAME
    '''
    try:
        url = config.host + '/profile/username'
        r = requests.put(url, headers=headers,
                         data=json.dumps({"username": username}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not set webprofile username:", e)

def reset_webprofileusername(username):
    '''
    Resets the username for the webprofile
    '''
    try:
        url = config.host + '/profile/username'
        r = requests.delete(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not delete webprofile username:", e)

def get_person(id):
    '''
    Gets a user's profile via their id
    '''
    try:
        url = config.host + '/user/%s' % id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get that person:", e)


def send_msg(match_id, msg):
    try:
        url = config.host + '/user/matches/%s' % match_id
        r = requests.post(url, headers=headers,
                          data=json.dumps({"message": msg}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not send your message:", e)

def unmatch(match_id):
    try:
        url = config.host + '/user/matches/%s' % match_id
        r = requests.delete(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not unmatch person:", e)

def superlike(person_id):
    try:
        url = config.host + '/like/%s/super' % person_id
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not superlike:", e)


def like(person_id):
    try:
        url = config.host + '/like/%s' % person_id
        r = requests.get(url, headers=get_headers)
        print('Liked')
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not like:", e)


def dislike(person_id):
    try:
        url = config.host + '/pass/%s' % person_id
        r = requests.get(url, headers=get_headers)
        print("Pass")
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not dislike:", e)


def report(person_id, cause, explanation=''):
    '''
    There are three options for cause:
        0 : Other and requires an explanation
        1 : Feels like spam and no explanation
        4 : Inappropriate Photos and no explanation
    '''
    try:
        url = config.host + '/report/%s' % person_id
        r = requests.post(url, headers=headers, data={
                          "cause": cause, "text": explanation})
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not report:", e)


def match_info(match_id):
    try:
        url = config.host + '/matches/%s' % match_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)

def all_matches(count=60, message=0, page_token=None):
    try:
        url = config.host + '/v2/matches?locale=en&count=' + str(count) + '&message=' + str(message) + '&is_tinder_u=false'
        if page_token:
            url = url + '&page_token=' + page_token
        r = requests.get(url, headers=headers)
        json = r.json()
        if 'data' in json.keys() and 'next_page_token' in json['data'].keys():
                next_page_data = all_matches(count, message, json['data']['next_page_token'])
                json['data']['matches'] = json['data']['matches'] + next_page_data['data']['matches']
        return json
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)

def fast_match_info():
  try:
      url = config.host + '/v2/fast-match/preview'
      r = requests.get(url, headers=headers)
      count = r.headers['fast-match-count']
      # image is in the response but its in hex..
      return count
  except requests.exceptions.RequestException as e:
      print("Something went wrong. Could not get your fast-match count:", e)

def trending_gifs(limit=3):
  try:
      url = config.host + '/giphy/trending?limit=%s' % limit
      r = requests.get(url, headers=headers)
      return r.json()
  except requests.exceptions.RequestException as e:
      print("Something went wrong. Could not get the trending gifs:", e)

def gif_query(query, limit=3):
  try:
      url = config.host + '/giphy/search?limit=%s&query=%s' % (limit, query)
      r = requests.get(url, headers=headers)
      return r.json()
  except requests.exceptions.RequestException as e:
      print("Something went wrong. Could not get your gifs:", e)


def process_recs(recs):
    """Gets data from the recs. Only collects if swiped"""
    recs = recs['results']
    ids = []
    bios = []
    xsmall_photos = []
    small_photos = []
    med_photos = []
    large_photos = []
    variance = 4
    mean = 3
    delays = np.random.randn(len(recs)) * variance + mean
    delays[delays < 0] = 1
    print(delays)
    for i in range(len(recs)):
        person = recs[i]
        person_xsmall_photos = []
        person_small_photos = []
        person_med_photos = []
        person_large_photos = []
        if np.random.rand() < like_prob:
            ids.append(person['_id'])
            bios.append(person['bio'])

            for j in range(len(person['photos'])):
                person_xsmall_photos.append(person['photos'][j]['processedFiles'][3]['url'])
                person_small_photos.append(person['photos'][j]['processedFiles'][2]['url'])
                person_med_photos.append(person['photos'][j]['processedFiles'][1]['url'])
                person_large_photos.append(person['photos'][j]['processedFiles'][0]['url'])

            xsmall_photos.append(person_xsmall_photos)
            small_photos.append(person_small_photos)
            med_photos.append(person_med_photos)
            large_photos.append(person_large_photos)
            like(person['_id'])
        else:
            dislike(person['_id'])
        time.sleep(delays[i])
    return ids, bios, xsmall_photos, small_photos, med_photos, large_photos


def process_matches(matches):
    """Processes match data. Return matcher id and their images"""
    matches = matches['data']
    matches = matches['matches']
    ids = []
    xsmall_photos = [] #Nested array
    small_photos = []
    med_photos = []
    large_photos = []

    for i in range(len(matches)):
        person = matches[i]['person']
        ids.append(person['_id'])

        person_xsmall_photos = []
        person_small_photos = []
        person_med_photos = []
        person_large_photos = []
        for j in range(len(person['photos'])):
            if len(person['photos'][j]['processedFiles']) != 4:
                continue
            person_xsmall_photos.append(person['photos'][j]['processedFiles'][3]['url'])
            person_small_photos.append(person['photos'][j]['processedFiles'][2]['url'])
            person_med_photos.append(person['photos'][j]['processedFiles'][1]['url'])
            person_large_photos.append(person['photos'][j]['processedFiles'][0]['url'])
        xsmall_photos.append(person_xsmall_photos)
        small_photos.append(person_small_photos)
        med_photos.append(person_med_photos)
        large_photos.append(person_large_photos)
    return (ids, xsmall_photos, small_photos, med_photos, large_photos)

def write_rec_data(ids, bios, xs, s, m, l):
    """Saves the info"""
    foldername = "RawData/"
    for i in range(len(ids)):
        id = ids[i]
        img_urls = s[i]
        for j in range(len(img_urls)):
            img_url = img_urls[j]
            img_name = id + '_' + str(j) + '.jpg'
            fullfilename = os.path.join(foldername, img_name)
            urllib.request.urlretrieve(img_url, fullfilename)

def write_match_data(match_ids, match_imgs):
    """Writes the matches to an excel file.
    Will also pics to training data that haven't been swiped on."""
    mypath = 'RawData'
    foldername = "RawData/"
    filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    # Instantiate excel sheet
    workbook = xlsxwriter.Workbook('labels.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Img_names')

    count = 2
    for i in range(len(match_ids)):
        match_id = match_ids[i]
        for j in range(len(match_imgs[i])):
            match_img_name = match_id + '_' + str(j) + '.jpg'
            match_img_url = match_imgs[i][j]
            # Check to see if the file does not exist in filenames. if not, add them (manually matched)
            if not match_img_name in filenames:
                fullfilename = os.path.join(foldername, match_img_name)
                urllib.request.urlretrieve(match_img_url, fullfilename)
            # Write to the excel sheet
            worksheet.write('A' + str(count), match_img_name)
            count += 1
    workbook.close()









like_prob = 0.3 #Probability of swiping right
swipe = False
authverif()



if swipe:
    for i in range(200):
        r = get_recommendations()
        rec_ids, rec_bios, rec_xsmall, rec_small, rec_med, rec_large = process_recs(r)
        write_rec_data(rec_ids, rec_bios, rec_xsmall, rec_small, rec_med, rec_large)

m = all_matches(count=5)
ids, xsmall, small, med, large = process_matches(m)
write_match_data(ids, small)

