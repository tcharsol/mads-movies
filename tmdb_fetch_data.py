#Move all functions to this file
import pandas as pd 
import numpy as np 
from urllib import request
import json
import csv
import re
import time
import random


global api_key
api_key = '35ee0168b67995d0c4266c806c126954'

def clean_movie_name(movie_name):
    value = movie_name.strip().replace(' ','+')
    return value

def get_tmdb_movie_id(movie_name,release_year):
    query_url = 'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}'.format(api_key=api_key,movie_name=movie_name)
    resp = request.urlopen(query_url)
    data = json.load(resp)

    for movie in data['results']:
        if release_year == movie['release_date'][:4]:
            return movie['id']
        else: 
            continue

def get_movie_details(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'.format(api_key=api_key,movie_id = movie_id)
    resp = request.urlopen(url)
    data_dict = json.load(resp)
    df = convert_resp_dict_series(data_dict)
    #data_string = json.dumps(data)
    #print(type(data_string),data_string)
    return df

def convert_resp_dict_series(resp_dict):
    df = pd.DataFrame.from_dict(resp_dict, orient='index')
    return df.transpose()

def get_movielens_details(movie_string):
    for item in re.finditer("(?P<name>[a-zA-Z\s:,#&-'0-9!?]*)(?:\()(?P<year>[0-9\s]*)(?:\))",movie_string):
        m = item.groupdict()
    return m




movielens = pd.read_csv("C:/Users/tam74426/MADS/SIADS 591/Project/data/ml-25m/movies.csv")
movie_names_list = movielens['title'].tolist()
total_count = len(movie_names_list)

batch_size = 100
total_batches = int(total_count/batch_size)
sleep_times = [batch_size*i for i in range(1,total_batches)]

count = 0
movies_not_found = list()

for item in movie_names_list:
    print(count,item)
    try:
        movielens_dict = get_movielens_details(item)
    except:
        with open("movies_not_found.csv","a",newline = '\n',encoding="utf-8") as f:
            f.write(item+ "\n")
        continue
    movie_name = movielens_dict['name']
    print(count,item,movie_name)
    release_year = movielens_dict['year']
    movie_name = clean_movie_name(movie_name)
    try:
        movie_id = get_tmdb_movie_id(movie_name=movie_name,
                                release_year=release_year)
        results = get_movie_details(movie_id=movie_id)
    except:
        movies_not_found.append(item)
        with open("movies_not_found.csv","a",newline = '\n',encoding="utf-8") as f:
            f.write(item+ "\n")
        continue

    with open("results.csv","a",newline = '\n',encoding="utf-8") as f:
        if count == 0:
            header = True
        else:
            header = False
        results.to_csv(f,header=header)
        count = count + 1
        if count in sleep_times:
            sleep_time = random.randint(100,200)
            print('going to sleep for {} seconds----------------------------------------------------------------------------------------------------------------'.format(sleep_time))
            time.sleep(sleep_time)
            



""" for movie_id in range(5000,6000):
    try:
        results = get_movie_details(movie_id=movie_id)
        print(results)
        count = count + 1
    except:
        print("Not found:",movie_id)
        movies_not_found.append(movie_id)
        continue

    with open("results.csv","a",newline = '\n',encoding="utf-8") as f:
        if count == 0:
            header = True
        else:
            header = False
        results.to_csv(f,header=header)

    if count >= 50:
        break 
         """







