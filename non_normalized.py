import utilities as utils
from datetime import datetime
import pandas as pd


start_time = datetime.now()
print("*"*10, "Process started @", start_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*50)


def get_non_normalized_movie_data_df(imdb_ids_list=["tt1630029", "tt0499549"], no_records_to_display=0):

    title_basics_data_df, title_basics_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                                level_2="basics",
                                                                show=False, no_records_to_show=no_records)

    title_basics_data_df = title_basics_data_df[title_basics_data_df["tconst"].isin(test_movie_ids)]
    title_basics_data_df = utils.split_cols_into_rows(source_df=title_basics_data_df, split_col_name="genres")
    title_basics_data_df = title_basics_data_df[["tconst", "genres"]]
    title_basics_data_df["type"] = "genre"
    title_basics_data_df.columns = ["tconst", "value", "type"]


    title_crew_data_df, title_crew_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                            level_2="crew",
                                                            show=False, no_records_to_show=no_records)
    title_crew_data_df = title_crew_data_df[title_crew_data_df["tconst"].isin(imdb_ids_list)]
    # title_crew_data_df = title_crew_data_df[title_crew_data_df["directors"].str.contains(",")]

    name_basics_data_df, name_basics_data_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/", level_1="name",
                                                                   level_2="basics",
                                                                   show=False, no_records_to_show=no_records)

    title_crew_data_writers_df = title_crew_data_df[["tconst", "writers"]].copy().drop_duplicates()
    title_crew_data_writers_df = utils.split_cols_into_rows(source_df=title_crew_data_writers_df, split_col_name="writers")

    joined_writers_df = pd.merge(title_crew_data_writers_df, name_basics_data_df,
                                 left_on="writers", right_on="nconst", how="left")
    joined_writers_df = joined_writers_df[["tconst", "primaryName"]]
    joined_writers_df["type"] = "writer"
    joined_writers_df.columns = ["tconst", "value", "type"]


    title_crew_data_directors_df = title_crew_data_df[["tconst", "directors"]].copy().drop_duplicates()
    title_crew_data_directors_df = utils.split_cols_into_rows(source_df=title_crew_data_directors_df, split_col_name="directors")
    joined_directors_df = pd.merge(title_crew_data_directors_df, name_basics_data_df,
                                   left_on="directors", right_on="nconst", how="left")
    joined_directors_df = joined_directors_df[["tconst", "primaryName"]]
    joined_directors_df["type"] = "director"
    joined_directors_df.columns = ["tconst", "value", "type"]


    title_principals_data_df, title_principals_cols = utils.read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                                        level_2="principals",
                                                                        show=False, no_records_to_show=no_records)
    title_principals_data_df = title_principals_data_df[title_principals_data_df["tconst"].isin(test_movie_ids)]
    title_principals_data_df = title_principals_data_df[["tconst", "nconst"]].copy().drop_duplicates()
    joined_principals_df = pd.merge(title_principals_data_df, name_basics_data_df, on="nconst", how="left")
    joined_principals_df = joined_principals_df[["tconst", "primaryName"]]
    joined_principals_df["type"] = "principal"
    joined_principals_df.columns = ["tconst", "value", "type"]

    non_normalized_df = pd.concat([title_basics_data_df, joined_writers_df, joined_directors_df, joined_principals_df])
    non_normalized_df = non_normalized_df.reset_index()

    if no_records_to_display > 0:
        print("title_basics_data_df :")
        print(title_basics_data_df.head(no_records_to_display))
        print()

        print("joined_writers_df :")
        print(joined_writers_df.head(no_records_to_display))
        print()

        print("joined_directors_df :")
        print(joined_directors_df.head(no_records_to_display))
        print()

        print("joined_principals_df :")
        print(joined_principals_df.head(no_records_to_display))
        print()

        print("non_normalized_df :")
        print(non_normalized_df)
        print()

    return non_normalized_df


save_dir = "../../Output/"
no_records = 15

temp_df = pd.read_csv("../../Data/tmdb/results.csv")
imdb_ids = temp_df["imdb_id"].values
imdb_ids = imdb_ids # [0:6]
test_movie_ids = imdb_ids[0:100]

non_normalized_df = get_non_normalized_movie_data_df(imdb_ids_list=test_movie_ids, no_records_to_display=5)

non_normalized_df.to_csv(save_dir + "non_normalized_df.csv", sep="\t")

end_time = datetime.now()
print("*"*10, "Process ended @", end_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*50)
duration = end_time - start_time
print("*"*10, "Duration -", duration, "*"*50)

