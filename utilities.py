import gzip
import os


import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def read_imdb_gz_data(directory, level_1, level_2, show=False, no_records_to_show=5):
    """


    """
    with gzip.open(os.path.join(directory, level_1 + "." + level_2 + ".tsv.gz")) as file:
        data_df = pd.read_csv(file, "\t", encoding="utf-8")
        cols = list(data_df.columns)

    if show:
        print(level_1 + "_" + level_2 + "_data :", data_df.head(no_records_to_show))
        print(level_1 + "_" + level_2 + "_cols :", cols)

    return data_df, cols


def split_cols_into_rows(source_df, split_col_name):
    temp_df = source_df.copy()
    temp = temp_df[split_col_name].str.split(",").apply(pd.Series, 1).stack()

    # if len(temp) > 1:
    temp.index = temp.index.droplevel(-1)
    temp.name = split_col_name
    # print("temp :")
    # print(temp.head())

    del temp_df[split_col_name]
    temp_df = temp_df.join(temp)

    return temp_df


def pivot_movie_data(input_df, keep_cols, index_col, pivot_cols, prefix=None):
    all_cols = list(set(keep_cols + [index_col] + [pivot_cols]))
    # print("all_cols :", all_cols)
    temp_df = input_df[all_cols].copy()
    # print("temp_df :")
    # print(temp_df.head())
    transformed_data = temp_df.pivot_table(index=keep_cols,
                                           columns=pivot_cols,
                                           values=pivot_cols,
                                           aggfunc=len)
    transformed_data.reset_index(drop=False, inplace=True)
    transformed_data.set_index(index_col, inplace=True)
    transformed_data.columns = transformed_data.columns.get_level_values(0)
    if prefix:
        col_names = list(transformed_data.columns)
        if len(prefix) > 0:
            prefixed_col_names = [prefix+str(col) if col not in keep_cols else col for col in col_names]
            transformed_data.columns = prefixed_col_names
    # print("transformed_data.columns.get_level_values(0) :", transformed_data.columns.get_level_values(0))
    # print("transformed_data.index :", transformed_data.index)
    # print("transformed_data.columns :", list(transformed_data.columns))
    return transformed_data


def get_non_normalized_movie_data_df(imdb_ids_list=["tt1630029", "tt0499549"], no_records_to_display=0):

    title_basics_data_df, title_basics_cols = read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                                level_2="basics",
                                                                show=False, no_records_to_show=no_records_to_display)

    title_basics_data_df = title_basics_data_df[title_basics_data_df["tconst"].isin(imdb_ids_list)]
    title_basics_data_df = split_cols_into_rows(source_df=title_basics_data_df, split_col_name="genres")
    title_basics_data_df = title_basics_data_df[["tconst", "genres"]]
    title_basics_data_df["type"] = "genre"
    title_basics_data_df.columns = ["tconst", "value", "type"]


    title_crew_data_df, title_crew_cols = read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                            level_2="crew",
                                                            show=False, no_records_to_show=no_records_to_display)
    title_crew_data_df = title_crew_data_df[title_crew_data_df["tconst"].isin(imdb_ids_list)]
    # title_crew_data_df = title_crew_data_df[title_crew_data_df["directors"].str.contains(",")]

    name_basics_data_df, name_basics_data_cols = read_imdb_gz_data(directory="../../Data/IMDB/", level_1="name",
                                                                   level_2="basics",
                                                                   show=False, no_records_to_show=no_records_to_display)

    title_crew_data_writers_df = title_crew_data_df[["tconst", "writers"]].copy().drop_duplicates()
    title_crew_data_writers_df = split_cols_into_rows(source_df=title_crew_data_writers_df, split_col_name="writers")

    joined_writers_df = pd.merge(title_crew_data_writers_df, name_basics_data_df,
                                 left_on="writers", right_on="nconst", how="left")
    joined_writers_df = joined_writers_df[["tconst", "primaryName"]]
    joined_writers_df["type"] = "writer"
    joined_writers_df.columns = ["tconst", "value", "type"]


    title_crew_data_directors_df = title_crew_data_df[["tconst", "directors"]].copy().drop_duplicates()
    title_crew_data_directors_df = split_cols_into_rows(source_df=title_crew_data_directors_df, split_col_name="directors")
    joined_directors_df = pd.merge(title_crew_data_directors_df, name_basics_data_df,
                                   left_on="directors", right_on="nconst", how="left")
    joined_directors_df = joined_directors_df[["tconst", "primaryName"]]
    joined_directors_df["type"] = "director"
    joined_directors_df.columns = ["tconst", "value", "type"]


    title_principals_data_df, title_principals_cols = read_imdb_gz_data(directory="../../Data/IMDB/", level_1="title",
                                                                        level_2="principals",
                                                                        show=False, no_records_to_show=no_records_to_display)
    title_principals_data_df = title_principals_data_df[title_principals_data_df["tconst"].isin(imdb_ids_list)]
    title_principals_data_df = title_principals_data_df[["tconst", "nconst"]].copy().drop_duplicates()
    joined_principals_df = pd.merge(title_principals_data_df, name_basics_data_df, on="nconst", how="left")
    joined_principals_df = joined_principals_df[["tconst", "primaryName"]]
    joined_principals_df["type"] = "principal"
    joined_principals_df.columns = ["tconst", "value", "type"]

    non_normalized_df = pd.concat([title_basics_data_df, joined_writers_df, joined_directors_df, joined_principals_df])
    non_normalized_df = non_normalized_df.reset_index(drop=True)

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
        print(non_normalized_df.head(no_records_to_display))
        print()

    return non_normalized_df


