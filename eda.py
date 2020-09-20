import pandas as pd
import numpy as np 
import altair as alt
import matplotlib.pyplot as plt


def get_first_row(s):
    return s.iloc[0]

#Reads the first line of line of data and determines if data is categorical, quantitative or nominal
def auto_get_data_type(df):
    type_dict = dict()
    columns = list(df.columns)
    for column in columns:
        value = get_first_row(df[column])
        if isinstance(value, str):
            if value.isnumeric():
                type_dict[column] = 'Q'
            else:
                type_dict[column] = 'C'   
        else:
            type_dict[column] = 'Q'
    return type_dict

#Manually enter if data is categorical, quantitative, nominal or id
def manual_entry_data_type(df):
    type_dict = dict()
    for column in list(df.columns):
        type_dict[column] = input('Enter the variable type for {} (Quantitative/Categorical/Index/Time) Q/C/I/T:'.format(column))
    return type_dict

def get_df_column_list(df):
    return list(df.columns)

def manual_data_type_entry(df):
    value = input('First time data entry (F), Correction (C), Skip this (S):')
    if value == 'F':     
        type_dict = manual_enter_data_type(df)
    elif value == 'C':
        correction = 'y'
        while correction == 'y':
            variable = input('Enter variable name:')
            value = input('Enter variable type:')
            type_dict[variable] = value
            correction = input('Update more variables(y/n):')
    elif value == 'S':
        print('Cool! here is dict:',type_dict)
    return type_dict


def get_column_names_for_variable_type(columns,type_dict,variable_type):
    cat_columns = [key for key,value in type_dict.items() if value is variable_type]
    return cat_columns

def get_data_for_variables(df,data_type_dict,variable_type):
    #print('get_data_for_variables--------------->',df)
    columns = get_df_column_list(df)
    var_columns = get_column_names_for_variable_type(columns,data_type_dict,variable_type)
    index_column = get_index_column(columns,data_type_dict)
    data_dict = dict()
    
    if variable_type == 'C':
        for column in var_columns:
            summary = df.groupby(column).agg({index_column: 'count'}).reset_index()
            data_dict[column] = summary
        return data_dict,var_columns
      
    elif variable_type == 'Q':
        for column in var_columns:
            quantitative_data = clean_quantitative_data(df[column])
            data_dict[column] = quantitative_data
        return data_dict,var_columns


def get_index_column(columns,type_dict):
    index_column = [key for key,value in type_dict.items() if value is 'I']
    return index_column[0]

def get_time_column(columns,type_dict):
    time_column = [key for key,value in type_dict.items() if value is 'T']
    return time_column[0]

def create_sorted_bar_chart(df,x_name,y_name,color='orange'):
    chart = alt.Chart(df).mark_bar(color=color).encode(
            x = x_name,
            y = alt.Y(y_name, sort='-x'))
    return chart

def get_x_y_column_names(df):
    columns = get_df_column_list(df)
    x_name = columns[1]
    y_name = columns[0]
    return x_name,y_name
    
def show_sorted_bar_chart(df):
    x_name,y_name = get_x_y_column_names(df)
    chart = create_sorted_bar_chart(df,x_name,y_name,color='orange')
    return chart


def clean_quantitative_data(s):
    s = pd.to_numeric(s, errors='coerce', downcast='float').dropna()
    return s

def clean_dataframe_for_timeseries(df,data_type_dict):
    columns = list(df.columns)
    for column in columns:
        value = data_type_dict[column]
        if value == 'T':
            df[column] = pd.to_datetime(df[column])
        elif value == 'Q':
            df[column] = pd.to_numeric(df[column], errors='coerce', downcast='float')
        else:
            continue

def get_central_tendency_for_variable(s):
    return s.mean(),s.median(),s.mode()

def get_spread_for_variable(s):
    return s.std(),s.var()

def get_skew_kurt_for_variable(s):
    return s.kurtosis(),s.skew()

def get_summary_statistics(s):
    mean, median, mode = get_central_tendency_for_variable(s)
    std, var = get_spread_for_variable(s)
    kurtosis, skewness = get_skew_kurt_for_variable(s)
    
    summary_dict = {'mean':mean, 'median':median, 'mode':mode,'std':std,
                    'var':var,'kurtosis':kurtosis,'skewness':skewness}
    
    return pd.DataFrame(summary_dict)

def run_non_graphical_EDA_categorical(df,data_type_dict):
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('                              Univariate Non-Graphical EDA                                   ')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    
    print('-------------------------------CATEGORICAL-------------------------------------------------\n')
    columns = get_df_column_list(df)
    index_column = get_index_column(columns,data_type_dict)
    cat_data_dict,cat_data_columns = get_data_for_variables(df=df,data_type_dict=data_type_dict,variable_type='C')
    for column in cat_data_columns:
        cata_data_summary = df.groupby(column).agg(
                                Frequency=pd.NamedAgg(column=index_column, aggfunc='count')).reset_index()
        cat_data_dict[column] = cata_data_summary
        print('---------------------------------------------------------------------------------------\n')
        print(cata_data_summary)
    
def run_non_graphical_EDA_quantitative(df,data_type_dict):
        
    print('-------------------------------QUANTITATIVE-------------------------------------------------\n')
    columns = get_df_column_list(df)
    index_column = get_index_column(columns,data_type_dict)
    quant_data_dict,quant_data_columns = get_data_for_variables(df=df,data_type_dict=data_type_dict,variable_type='Q')
    for column in quant_data_columns:
        print('---------------------------Summary Statistics for {}-----------------------------------\n'.format(column))
        quantitative_data = clean_quantitative_data(df[column])
        print(get_summary_statistics(quantitative_data))

        
def run_graphical_EDA_categorical(df,data_type_dict):
    all_columns = get_df_column_list(df)
    index_column = get_index_column(all_columns,data_type_dict)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('                              Univariate Graphical EDA                                   ')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    print('-------------------------------CATEGORICAL-------------------------------------------------\n')
    
    #input_string = input('Enter the column names of the categorical data separated by comma (,) for visual exploration:')
    
    cat_data_dict,cat_data_columns = get_data_for_variables(df=df,data_type_dict=data_type_dict,variable_type='C')
    #cat_variables_for_graph = [item.strip() for item in input_string.split(',')]
    for cat_variable in cat_data_columns: 
        cat_df = cat_data_dict[cat_variable]
        cat_df = cat_df.sort_values(by=list(cat_df.columns)[1],ascending=False)
        if len(cat_df) > 20:
            value = input('The summary data for {} has many rows. Would you like see top 20 only?(y/n)'.format(cat_variable))
            if value == 'y':
                cat_df = cat_df.iloc[:20]
        print('-------------------------------------------------------------------------------------\n')
        show_sorted_bar_chart(cat_df).display()
        
def run_graphical_EDA_quantitative(df,data_type_dict):
    print('-------------------------------QUANTITATIVE-------------------------------------------------\n')
    all_columns = get_df_column_list(df)
    index_column = get_index_column(all_columns,data_type_dict)
    quant_data_dict,quant_data_columns = get_data_for_variables(df=df,data_type_dict=data_type_dict,variable_type='Q')
    for column in quant_data_columns:
        print('---------------------------Histogram for {}-----------------------------------\n'.format(column))
        quantitative_data = clean_quantitative_data(df[column])
        plt.hist(np.array(quantitative_data))
        plt.show()
    
    outlier_val = input('Would you like to see the distribution without outliers? (y/n):')
    if outlier_val == 'y':
        for column in quant_data_columns:
            print('---------------------------Histogram for {} without outliers-----------------------------------\n'.format(column))
            quantitative_data = clean_quantitative_data(df[column])
            quantitative_data_no_outliers = quantitative_data[(np.abs(stats.zscore(quantitative_data)) < 3)]
            plt.hist(np.array(quantitative_data_no_outliers))
            plt.show()
            outlier_val = input('remove more outliers for {}?(y/n):'.format(column))
            while outlier_val == 'y':
                quantitative_data_no_outliers = quantitative_data_no_outliers[(np.abs(stats.zscore(quantitative_data_no_outliers)) < 3)]
                plt.hist(np.array(quantitative_data_no_outliers))
                plt.show()
                outlier_val = input('remove more outliers for {}?(y/n):'.format(column))
                
def truncate_data(df):
    if len(df) > 5000:
        df = df[:5000]
    return df
                               
def run_time_series_EDA(df,data_type_dict):
    all_columns = get_df_column_list(df)
    time_column = get_time_column(all_columns,data_type_dict)
    quant_data_dict,quant_data_columns = get_data_for_variables(df=df,data_type_dict=data_type_dict,variable_type='Q')
    
    
    for column in quant_data_columns:
        print('---------------------------Time Series for {}-----------------------------------\n'.format(column))
        
        df_chart = df[[time_column,column]]
        #quantitative_data = clean_dataframe_for_timeseries(df_chart,data_type_dict)
        quantitative_data = df_chart
        chart = alt.Chart(truncate_data(quantitative_data)).mark_line().encode(
                x=time_column+':T',
                y=column+':Q'
                )
        chart.display()
        
def run_non_graphical_EDA_info(df,data_type_dict):
    run_non_graphical_EDA_categorical(df,data_type_dict)
    run_non_graphical_EDA_quantitative(df,data_type_dict)   
    return None

def run_graphical_EDA_info(df,data_type_dict):
    run_graphical_EDA_categorical(df,data_type_dict)
    run_graphical_EDA_quantitative(df,data_type_dict)
    run_time_series_EDA(df,data_type_dict)
    return None
      
def run_preliminary_EDA(df):
    print(df.head())
    data_type_dict = manual_entry_data_type(df)
    run_non_graphical_EDA_info(df,data_type_dict)
    run_graphical_EDA_info(df,data_type_dict)
    return None