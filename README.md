# mads-movies
Explore the primary factors impacting a movie's profitability
------------------------------------------------------------------------------------------------------------------------

## Data Processing Steps


### MovieLens
First Download the Movielens datase. The file called "movies.csv" is used from this dataset. The remaining data is not utiltized.

### TMDB
1. Once you have the movies.csv from Movielens, go to script -> tmdb_fetch_data.py
2. Enter the api_key if you have one or use the key in the script
3. Enter the folder location of movies.csv in the script OR you find see a FILE NOT FOUND ERROR!
4. Run the script tmdb_fetch_data.py. The script will start populating the results.csv file with the required data from TMDB.
5. Once the results.csv has been fully populated, go to script -> tmdb_data_features.py
6. Enter the folder location of results.csv in the script OR you find see a FILE NOT FOUND ERROR!
7. Run the script. You will the processed TMDB dataset with the genre data


### IMDd
The following files should be executed / accessed in the following sequence:
1. process_imdb_data.py - this step creates an intermediate data set (the location should be set because the steps that follow use this file)
2. machine-learning-data-exploration.ipynb
3. machine-learning-regression-ipynb
4. machine-learning-classification.ipynb


Key Resources:

Let us try and use this workflow as much as possible - https://jakevdp.github.io/blog/2017/03/03/reproducible-data-analysis-in-jupyter/

Atlassian work flow - https://www.atlassian.com/git/tutorials/comparing-workflows

Consider adding ethics checklist like this one - https://deon.drivendata.org/

------------------------------------------------------------------------------------------------------------------------


Explore the primary factors impacting a movie's profitability

Use this repository to explore the relationship between several key factors (director, writer, cast, crew etc.) and a movie's profitability.

This analysis uses the following datasets. 

MovieLens - https://grouplens.org/datasets/movielens/25m/

IMDB - https://www.imdb.com/interfaces/

Boxofficemojo - No dataset yet. A scraper might be required. Here is a starting point - https://medium.com/@kunsitu/analysing-weekend-box-office-data-from-box-office-mojo-by-using-python-part-1-86dcabac9164

This paper can be cited as inpsiration for this analysis - https://arxiv.org/pdf/1506.05382v2.pdf

