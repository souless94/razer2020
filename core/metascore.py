import requests
import time
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# don't forget to refresh lol key
lol_key = 'RGAPI-d3798be0-998a-4f86-8f9c-ac86e8f89698'
dota_key = '76b62706-1c6f-4e06-b7a6-bcc5523073cf'
fortnite_key = '8954ce57-a687c6b7-93e484e5-e0fd7193'
pubg_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzMTY4MmVhMC03OTE0LTAxMzgtYWYyNi0wMDNiMDE4NjQ5MzkiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTg5NTcyNjMzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImphY2tpZS11cGxldmVsIn0.6LixccqXITLvrQFT6S-Np7ofo82ZUbSaqul8f8UkERk'

# get PUBGMatchTimings to construct playing pattern
def getPUBGMatchTiming(username):
    match_dates = []
    headers = {"Accept": "application/vnd.api+json",
               "Authorization": "Bearer "+ pubg_key}
    res = requests.get("https://api.pubg.com/shards/steam/players?filter[playerNames]=" + username, headers = headers)
    match_list = res.json()['data'][0]['relationships']['matches']['data']
    for match in match_list:
        id_ = match['id']
        match_details = requests.get("https://api.pubg.com/shards/steam/matches/" + str(id_), headers=headers).json()
        match_dates.append(match_details['data']['attributes']['createdAt'])
    return match_dates

# get LOLMatchTimings
def getLOLMatchTiming(username):
    match_dates = []
    res = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + str(username) + "?api_key=" + lol_key)
    match_list = res.json()['matches']
    for match in match_list:
        match_dates.append(datetime.fromtimestamp(match['timestamp']/1000))
    return match_dates

# get Fortnite match timings
def getFortniteMatchTiming(username):
    match_dates = []
    headers = {"Authorization": fortnite_key}
    res = requests.get("https://fortniteapi.io/matches?account=" + str(username), headers=headers)
    for match in res.json()['matches']:
        match_dates.append(match['date'])
    return match_dates

# get Dota2 match timings
def getDota2MatchTiming(username):
    match_dates = []
    matches = requests.get('https://api.opendota.com/api/players/' + str(username) + '/recentmatches')
    
    for date in matches.json():
        match_dates.append(datetime.fromtimestamp(date['start_time']))
    return match_dates    

# get dota wordcloud to see what the user is saying during games
def getDota2WordCloud(username):
    user_wordcloud = requests.get('https://api.opendota.com/api/players/' + str(username) + '/wordcloud')
    return user_wordcloud.json()['my_word_counts']

# lag is a function of internet access, both himself and his peers
# constant lagging will be detrimental to his score
def getLagScore(user_wordcloud):
    # get total wordcount
    wordcountSum = sum(user_wordcloud.values())
    
    # initialize NLP wordstemmer
    
    lag_sum = 0
    for word in user_wordcloud:
        if word == "lagg" or word == "lag":
            lag_sum += user_wordcloud[word]
            
    lag_proportion = lag_sum / wordcountSum

    if lag_proportion > 0.1:
        return 0
    else:
        return 1

# ascertain whether the user is playing during workdays and working hours
def generateMatchPatternScore(match_dates):
    match_df = pd.DataFrame({"date": match_dates})
    match_df['real_date'] = pd.to_datetime(match_df['date'])
    hourly_df = match_df.resample('H', on = 'real_date').count()
    
    isPlayingDuringWorkingHours = []

    for i in hourly_df.index:
        if i.dayofweek in range(5):
            if not ((i.hour > 12 and i.hour < 14) or i.hour > 18):
                isPlayingDuringWorkingHours.append(1)
            else:
                isPlayingDuringWorkingHours.append(0)
        else:
            isPlayingDuringWorkingHours.append(0)

    hourly_df['isPlayingDuringWorkHours'] = isPlayingDuringWorkingHours
    return (1 - hourly_df['isPlayingDuringWorkHours'].sum()/len(hourly_df))    
    
# combines all of the scores into one metascore
def score_generator(dictionary_of_games):
    metascore = {"metascore": 0}
    game_number = 0
    for game, username in dictionary_of_games.items():
        if game.lower() == 'pubg':
            pubg_score = generateMatchPatternScore(getPUBGMatchTiming(username))
            metascore['metascore'] += pubg_score
            game_number += 1
        elif game.lower() == 'dota2':
            dota_lag_score = getLagScore(getDota2WordCloud(username))
            metascore['metascore'] += dota_lag_score
            dota_score = generateMatchPatternScore(getDota2MatchTiming(username))
            metascore['metascore'] += dota_score
            game_number += 2
        elif game.lower() == 'lol':
            lol_score = generateMatchPatternScore(getLOLMatchTiming(username))
            metascore['metascore'] += lol_score
            game_number += 1
        elif game.lower() == 'fortnite':
            fortnite_score = generateMatchPatternScore(getFortniteMatchTiming(username))
            metascore['metascore'] += fortnite_score
            game_number += 1
    if game_number == 0:
        pass
    else:
        metascore['metascore'] = metascore['metascore'] / game_number
        
    return metascore