from datetime import datetime
import pandas as pd
import os
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


start_time = datetime.now()
print("*"*10, "Process started @", start_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*25)

i_am_here = os.getcwd()
print("i_am_here :", i_am_here)
temp_df = pd.read_csv("../../Data/tmdb/results.csv")
# print("temp_df :")
# print(temp_df.head())
# col_names = list(temp_df.columns)
# print("col_names :", col_names)

imdb_ids = temp_df["imdb_id"].values
print("imdb_ids :", imdb_ids[0:6])
print("len(imdb_ids) :", len(imdb_ids))
end_time = datetime.now()
print("*"*10, "Process ended @", end_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*25)
duration = end_time - start_time
print("*"*10, "Duration -", duration, "*"*25)