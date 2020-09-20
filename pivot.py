import utilities as utils
from datetime import datetime
import pandas as pd

start_time = datetime.now()
print("*"*10, "Process started @", start_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*50)


save_dir = "../../Output/"
no_records = 15
test_movie_ids = ["tt1630029", "tt0499549"]
# test_movie_ids = ["tt12011004", "tt11547218", "tt7247382", "tt6231500"]
# test_movie_ids = ["tt12011004", "tt11547218", "tt7247382", "tt6231500"]

# data_df, cols = read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title", level_2="akas",
#                                   show=True, no_records_to_show=no_records)
# print()

title_basics_data_df, title_basics_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                            level_2="basics",
                                                            show=False, no_records_to_show=no_records)
# print("title_basics_data_df.dtypes :")
# print(title_basics_data_df.dtypes)

title_types_count = title_basics_data_df[title_basics_data_df["titleType"] == "movie"]["titleType"].value_counts()
# print("title_types_count :")
# print(title_types_count)

temp_df = pd.read_csv("../../Data/tmdb/results.csv")
imdb_ids = temp_df["imdb_id"].values
imdb_ids = imdb_ids # [0:6]
print("imdb_ids :", imdb_ids)

# movie_ids = list(title_basics_data_df["tconst"].head(10000).values)
# test_movie_ids.extend(movie_ids)

test_movie_ids = imdb_ids[0:10000]

print("test_movie_ids :", test_movie_ids)

# filter = (title_basics_data_df["titleType"] == "movie") & \
#          (title_basics_data_df["primaryTitle"].str.contains("Avatar", na=False, case=False)) & \
#          (title_basics_data_df["tconst"].isin(test_movie_ids))
filter = (title_basics_data_df["titleType"] == "movie") & (title_basics_data_df["tconst"].isin(test_movie_ids))
# filter = (title_basics_data_df["tconst"].isin(test_movie_ids))

# print("title_basics_data_df :", title_basics_data_df.head(no_records))
# print()

title_basics_data_df = title_basics_data_df[title_basics_data_df["tconst"].isin(test_movie_ids)]
print("title_basics_data_df.shape :", title_basics_data_df.shape)

title_basics_data_pivoted_df = utils.pivot_movie_data(input_df=title_basics_data_df,
                                                keep_cols=["tconst", "primaryTitle", "startYear"],
                                                index_col="tconst",
                                                pivot_cols="genres",
                                                prefix="genres__")
print("title_basics_data_pivoted_df.shape :", title_basics_data_pivoted_df.shape)

title_crew_data_df, title_crew_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                        level_2="crew",
                                                        show=False, no_records_to_show=no_records)
title_crew_data_df = title_crew_data_df[title_crew_data_df["tconst"].isin(test_movie_ids)]
# title_crew_data_df = title_crew_data_df[title_crew_data_df["directors"].str.contains(",")]

name_basics_data_df, name_basics_data_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/", level_1="name",
                                                               level_2="basics",
                                                               show=False, no_records_to_show=no_records)

# title_crew_data_df["writers"] = title_crew_data_df.assign(var1=title_crew_data_df["writers"].str.split(",")).explode("writers")
title_crew_data_writers_df = title_crew_data_df[["tconst", "writers"]].copy().drop_duplicates()
title_crew_data_writers_df = utils.split_cols_into_rows(source_df=title_crew_data_writers_df, split_col_name="writers")

joined_writers_df = pd.merge(title_crew_data_writers_df, name_basics_data_df,
                             left_on="writers", right_on="nconst", how="left")
title_crew_writers_pivot_df = utils.pivot_movie_data(input_df=joined_writers_df,
                                               keep_cols=["tconst"],
                                               index_col="tconst",
                                               pivot_cols="primaryName",
                                               prefix="writer__")
# print("title_crew_writers_pivot_df :")
# print(title_crew_writers_pivot_df.head(no_records))
print("title_crew_writers_pivot_df.shape :", title_crew_writers_pivot_df.shape)

title_crew_data_directors_df = title_crew_data_df[["tconst", "directors"]].copy().drop_duplicates()
title_crew_data_directors_df = utils.split_cols_into_rows(source_df=title_crew_data_directors_df, split_col_name="directors")


joined_directors_df = pd.merge(title_crew_data_directors_df, name_basics_data_df,
                               left_on="directors", right_on="nconst", how="left")
title_crew_directors_pivot_df = utils.pivot_movie_data(input_df=joined_directors_df,
                                                 keep_cols=["tconst"],
                                                 index_col="tconst",
                                                 pivot_cols="primaryName",
                                                 prefix="director__")
# print("title_crew_directors_pivot_df :")
# print(title_crew_directors_pivot_df.head(no_records))

title_principals_data_df, title_principals_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                                    level_2="principals",
                                                                    show=False, no_records_to_show=no_records)
title_principals_data_df = title_principals_data_df[title_principals_data_df["tconst"].isin(test_movie_ids)]
# print("title_principals_data_df :")
# print(title_principals_data_df.head(no_records))
title_principals_data_df = title_principals_data_df[["tconst", "nconst"]].copy().drop_duplicates()
joined_principals_df = pd.merge(title_principals_data_df, name_basics_data_df, on="nconst", how="left")
title_crew_principals_pivot_df = utils.pivot_movie_data(input_df=joined_principals_df,
                                                  keep_cols=["tconst"],
                                                  index_col="tconst",
                                                  pivot_cols="primaryName",
                                                  prefix="principal__")
# print("title_crew_principals_pivot_df :")
# print(title_crew_principals_pivot_df.head(no_records))

pivoted_df = pd.merge(title_basics_data_pivoted_df, title_crew_writers_pivot_df,
                      left_index=True, right_index=True, how="left")
pivoted_df = pd.merge(pivoted_df, title_crew_directors_pivot_df,
                      left_index=True, right_index=True, how="left")
pivoted_df = pd.merge(pivoted_df, title_crew_principals_pivot_df,
                     left_index=True, right_index=True, how="left")
# print("pivoted_df :")
# print(pivoted_df.head(no_records))

# #
# # # Title Episode ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# # print("Title Episode ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
# # data_df, cols = read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title", level_2="episode",
# #                                   show=True, no_records_to_show=no_records)
# # print()
# #

#
#
# # Title Ratings ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# print("Title Ratings ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
# title_ratings_data_df, title_ratings_cols = read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
#                                                               level_2="ratings",
#                                                               show=False, no_records_to_show=no_records)
# print("title_ratings_data_df :")
# print(title_ratings_data_df.head(no_records))
# print()
#
#
# # Name Basics ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#
#
# # Join ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# print("Join ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#

#

# print("joined_directors_df :")
# print(joined_directors_df.head(no_records))
# title_crew_directors_pivot_df = pivot_movie_data(input_df=joined_directors_df,
#                                                  keep_cols=["tconst"],
#                                                  index_col="tconst",
#                                                  pivot_cols="primaryName",
#                                                  prefix="director__")
# print("title_crew_directors_pivot_df :")
# print(title_crew_directors_pivot_df.head(no_records))
#
#

#

#
#
# # keep_cols = ["tconst", "originalTitle", "startYear", "runtimeMinutes", "genres",
# #              "averageRating", "numVotes",
# #              "directors", "writers",
# #              "category", "job", "characters",
# #              "primaryName", "birthYear", # "deathYear", "primaryProfession"
# #              ]
# #
# # keep_cols = list(joined_df.columns)
# # drop_cols = ["titleType", "originalTitle", "isAdult", "endYear", "ordering",
# #              "knownForTitles_principal", "knownForTitles_director", "knownForTitles_directors", "knownForTitles_writer", "knownForTitles",
# #              "nconst_principal", "nconst_director", "nconst_directors", "nconst_writer", "nconst",
# #              "deathYear_principal", "deathYear_director", "deathYear_directors", "deathYear_writer", "deathYear",
# #              "primaryProfession_principal", "primaryProfession_director", "primaryProfession_directors", "primaryProfession_writer", "primaryProfession",
# #              "job",
# #              "writers",
# #              "directors"] #,
#              # "nconst_writer", "deathYear_writer", "primaryProfession_writer", "knownForTitles_writer",
#              # "nconst", "deathYear", "primaryProfession", "knownForTitles", "primaryName"]
# # drop_cols = ["titleType", "originalTitle", "isAdult", "endYear",
# #              "deathYear_writers", "primaryProfession_writers", "knownForTitles_writers",
# #              "deathYear_name", "primaryProfession_name", "knownForTitles_name",
# #              "deathYear_writer", "primaryProfession_writer", "knownForTitles_writer",
# #              "deathYear", "primaryProfession", "knownForTitles",
# #              "writers", "directors", "ordering", "nconst_writers", "nconst_writers", "deathYear_names",
# #              "nconst_name", "nconst"]
# # keep_cols = [x for x in keep_cols if x not in drop_cols]
# # joined_df = joined_df[keep_cols]
# #
# # renamed_cols = {"primaryName": "primaryName_director",
# #                 "birthYear": "birthYear_director"}
# # joined_df = joined_df.rename(columns=renamed_cols)
# #
# # print("joined_df :")
# # print(joined_df.head(no_records))
# # joined_df.to_csv(save_dir + "joined_df.csv", sep="\t")
# #
# # pivoted_df = joined_df.pivot_table(index=["tconst", "primaryTitle", "startYear", "runtimeMinutes", "primaryName_writer", "primaryName_director"],
# #                                    columns="primaryName_principal",
# #                                    # values="primaryName_principal",
# #                                    aggfunc=len)
# # pivoted_df.reset_index(drop=False, inplace=True)
# #
# #
# # print("pivoted_df :")
# print(pivoted_df.head(no_records))
pivoted_df.to_csv(save_dir + "pivoted_df.csv", sep="\t")

end_time = datetime.now()
print("*"*10, "Process ended @", end_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*50)
duration = end_time - start_time
print("*"*10, "Duration -", duration, "*"*50)

