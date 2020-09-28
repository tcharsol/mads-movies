import utilities as utils
from datetime import datetime
import pandas as pd
import numpy as np

start_time = datetime.now()
print("*"*10, "Process started @", start_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*50)

START_YEAR = 1980
MIN_BUDGET = 1000
MIN_REVENUE = 10
MAX_RECORDS = -1

save_dir = "../../Output/"
no_records = 15

tmdb_df = pd.read_csv("../../Data/tmdb/results.csv")
print("tmdb_df :")
print(tmdb_df[["release_date", "popularity"]].head(1))
print("tmdb_df.columns :", list(tmdb_df.columns))
tmdb_df = tmdb_df[["imdb_id", "revenue", "budget", "runtime", "release_date", "popularity"]]

# print("tmdb_df :")
# print(tmdb_df.head())


imdb_ids = tmdb_df["imdb_id"].values
print("len(imdb_ids) :", len(imdb_ids))
test_movie_ids = imdb_ids#[-5000:]
# test_movie_ids = ["tt0002260"]
print("len(test_movie_ids) :", len(test_movie_ids))

title_basics_data_df, title_basics_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/",
                                                                  level_1="title",
                                                                  level_2="basics",
                                                                  show=False,
                                                                  no_records_to_show=no_records)
print("title_basics_cols :", title_basics_cols)
title_basics_data_df = title_basics_data_df[["tconst", "primaryTitle", "originalTitle", "startYear"]]
title_basics_data_df = pd.merge(title_basics_data_df, tmdb_df, left_on="tconst", right_on="imdb_id", how="inner")

title_basics_data_df["popularity"] = title_basics_data_df["popularity"].astype("Float64")
title_basics_data_df["release_date"] = pd.to_datetime(title_basics_data_df["release_date"])

title_basics_data_df["startYear"] = title_basics_data_df["startYear"].replace("\\N", "0")
title_basics_data_df["startYear"] = title_basics_data_df["startYear"].astype("Float64")

title_basics_data_df["budget"] = title_basics_data_df["budget"].astype("Float64")
title_basics_data_df["runtime"] = title_basics_data_df["runtime"].astype("Float64")
title_basics_data_df["revenue"] = title_basics_data_df["revenue"].astype("Float64")

title_basics_data_df = title_basics_data_df[(title_basics_data_df["startYear"] >= START_YEAR) &
                                            (title_basics_data_df["budget"] >= MIN_BUDGET) &
                                            (title_basics_data_df["revenue"] >= MIN_REVENUE)]
if MAX_RECORDS != -1:
    test_movie_ids = title_basics_data_df["tconst"].values[:MAX_RECORDS]
else:
    test_movie_ids = title_basics_data_df["tconst"].values

print("len(test_movie_ids) :", len(test_movie_ids))
print("test_movie_ids :")
print(test_movie_ids)

title_basics_data_df = title_basics_data_df[title_basics_data_df["tconst"].isin(test_movie_ids)]
title_basics_data_df.to_csv(save_dir + "imdb_title_basics_df.csv", sep="|")
print("title_basics_data_df.shape :", title_basics_data_df.shape)

non_normalized_df = utils.get_non_normalized_movie_data_df(imdb_ids_list=test_movie_ids, no_records_to_display=0)
non_normalized_df = non_normalized_df[non_normalized_df["tconst"].isin(test_movie_ids)]
print("non_normalized_df.shape :", non_normalized_df.shape)

# non_normalized_df = non_normalized_df.head(100)
non_normalized_df.to_csv(save_dir + "imdb_non_normalized_df.csv", sep="|")
print("non_normalized_df :")
print(non_normalized_df.head(15))
print("non_normalized_df['type'].unique() :", non_normalized_df["type"].unique())
print("non_normalized_df.shape :", non_normalized_df.shape)
print("non_normalized_df.shape :", non_normalized_df.shape)

non_normalized_df["type__value"] = non_normalized_df["type"] + "__" + non_normalized_df["value"]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
pivot_df = utils.pivot_movie_data(input_df=non_normalized_df,
                                  keep_cols=["tconst"],
                                  index_col="tconst",
                                  pivot_cols="type__value",
                                  prefix=None)

# print("pivot_df :")
# print(pivot_df.head(1))

# non_normalized_dummies_df.to_csv(save_dir + "imdb_non_normalized_dummies_df.csv", sep="|")
imdb_dummies_df = pd.merge(title_basics_data_df, pivot_df,
                           left_on="tconst", right_index=True, how="left")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# non_normalized_pivot_df = pd.get_dummies(non_normalized_df["type__value"])
# print("non_normalized_pivot_df :")
# print(non_normalized_pivot_df.head(1))
#
# non_normalized_dummies_df = pd.merge(non_normalized_df[["tconst"]], non_normalized_pivot_df,
#                                      left_index=True, right_index=True, how="left")
# # non_normalized_dummies_df = non_normalized_dummies_df.drop_duplicates()
# non_normalized_dummies_df = non_normalized_dummies_df.groupby("tconst").sum()
# print("non_normalized_dummies_df :")
# print(non_normalized_dummies_df.head(1))
#
# # non_normalized_dummies_df.to_csv(save_dir + "imdb_non_normalized_dummies_df.csv", sep="|")
# imdb_dummies_df = pd.merge(title_basics_data_df, non_normalized_dummies_df,
#                            left_on="tconst", right_index=True, how="left")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


imdb_dummies_df.set_index("tconst", inplace=True)
print("imdb_dummies_df.shape :", imdb_dummies_df.shape)#

# imdb_dummies_df = imdb_dummies_df.head(100)
imdb_dummies_df.to_csv(save_dir + "imdb_dummies_df.csv", sep="|", index=True)

end_time = datetime.now()
print("*"*10, "Process ended @", end_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*50)
duration = end_time - start_time
print("*"*10, "Duration -", duration, "*"*50)
