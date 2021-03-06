import pandas as pd 
import numpy as np 
import re

tmdb_raw = pd.read_csv('results.csv')


def get_all_genres_from_data(s):

    """
    The results.csv file has a series of strings which contains the genre information in the following format: 
    "[{'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]"
    This function parses through this string to get the genre names

    Parameters:
    -----------

    s = pd.Series
        pd.Series object containing all the genre information
    
    Returns:
    --------

    all_genres : set
        set object with a list of the genres

    """

    all_genres = set()

    for index,value in s.items():
        genre_list = parse_genres_from_string(value)
        for item in genre_list:
            all_genres.add(item)

    all_genres = list(all_genres)
    all_genres  = sorted(all_genres, key=str.lower)
    return all_genres

def parse_genres_from_string(genre_string):

    """
    This function matches a pattern to return the genres in the following format: "[{'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]"

    Parameters:
    ----------

    genre_string : str
        string object that needs to be parsed

    Returns:
    --------

    genres : list
        list object containing all the genres that a movie belongs to

    """

    x = re.finditer("(?P<whatever>name[\':\s]*)(?P<genre>[a-zA-Z\s]*)",genre_string)
    genres = [item.group(2) for item in x]

    return genres

def get_genre_matrix(all_genres,movie_genres):

    """
    Converts the movie genres (i.e Titanic belongs to genres 'Romance', 'Drama') to a matrix of 1,0 
    ['Mystery', 'Animation', 'Romance', 'History', 'Thriller', 'Fantasy', 'TV Movie', 'Horror', 'Documentary', 'Drama', 'Science Fiction', 'Western', 'Crime', 'War', 'Action', 'Family', 'Adventure', 'Music', 'Comedy']
    The Titanic genre matrix for this becomes:
    [0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0] with 1 marking the presence of Romance and Drama.

    Parameters:
    -----------
    all_genres : list
        list of possible genres
    
    movie_genres : list
        genres pertaining to particular movie

    Returns:
    --------

    genre_matrix : list or np.ndarray

    """
    genre_matrix = list()
    for item in all_genres:
        if item in movie_genres:
            genre_matrix.append(1)
        else:
            genre_matrix.append(0)
    
    return genre_matrix

def convert_list_to_series(genre_list):

    s = pd.Series(genre_list)

    return s

def append_genre_data(df):
    """
    Appends the genre data to the results dataframe:

    Parameters:
    -----------

    df : pd.Dataframe
        the dataframe to which the genre dataframe should be appended to

    s : pd.Series
        the genre matrix converted to series

    Returns:
    ---------

    df : pd.Dataframe
        the dataframe with the genre matrix data appended

    """

    old_df = df
    all_genres = get_all_genres_from_data(df['genres'])

    #Define new Dataframe
    #new_columns = list(df.columns) + all_genres
    #np_new = np.array(np.empty([len(df),len(new_columns)]))
    #new_df = pd.DataFrame(np_new, columns = new_columns)
    matrix_list = list()

    for index,row in old_df.iterrows():
        print('Parsing row - {}'.format(index))
        genre_string = row['genres']
        movie_genres = parse_genres_from_string(genre_string)
        genre_matrix = get_genre_matrix(all_genres=all_genres,movie_genres=movie_genres)
        matrix_list.append(genre_matrix)
        #matrix_series = pd.Series(genre_matrix)
        #new_df.loc[index] = row.append(matrix_series, ignore_index=False, verify_integrity=False)
    
    full_genre_matrix = np.array(matrix_list)
    df_genre = pd.DataFrame(np.array(full_genre_matrix),columns = all_genres)
    new_df = pd.concat([old_df, df_genre],axis=1)
    #print(full_genre_matrix)
    return new_df
    
y = parse_genres_from_string("[{'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]")
all_genres = get_all_genres_from_data(tmdb_raw['genres'])
genre_matrix = get_genre_matrix(all_genres=all_genres,movie_genres=['War','Western'])
new_df = append_genre_data(tmdb_raw)

new_df.to_csv('results_processed_withGenre.csv')
