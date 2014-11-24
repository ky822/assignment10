
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#This function is to load data
def load_data(fpath, features):
    """
    fpath: The data file path to be loaded
    features: The features name (columns name) in the data file to be loaded
    """
    df = pd.read_csv(fpath)
    df = df[features]
    return df

#This function is to clean data
def clean_data(df):
    """
    df: dataframe to be cleaned
    """
    df = df[df['GRADE'].isin(['A','B','C'])] #to check if grade is in A,B or C, removing invalid data
    df = df.drop_duplicates() #drop duplicates
    df['GRADE DATE'] = pd.to_datetime(df['GRADE DATE'])#transfer to datetime type
    df = df.set_index('CAMIS')#set id as index
    return df

#This function is to test if grade in a grade list is improving or declining
def test_grades(grade_list):
    """
    grade_list: a grade list to be tested
    
    Return:
    increase: 1 if increasing, 0 if not changing, -1 if declining
    
    Note:
    The grade list is sorted in date order, the first element is the day nearest to current date
    """
    grade_dict = {'A': 1, 'B': 0, 'C': -1} #assign 1 for A, 0 for B, -1 for C
    
    result = grade_dict[grade_list[0]]-grade_dict[grade_list[-1]]#calculate the difference between the first grade and the last grade
    
    if result == 0:
        increase = 0 #if there is no different between the first and last grade, return 0 for not changing
    elif result > 0:
        increase = 1 #if there is a increase between the first and last grade, return 1 for improving
    elif result < 0:
        increase = -1 #if there is a decrease between the first and last grade, return -1 for declining
        
    """
    Please note: 
    The reasons I choose to just simply calculate the difference between the first and last grade are:
    1)The maximum amount of grade records is only 8 for all restaurants in this dataset.
      That is, it is hard to distinguish outliers and capture the trend in grade records for a restaurant.
    2)The grade records are categorical, the distance between any two categories is hard to say.
      It's reasonable to just simply say that A is greater than B and B is greater than C.
    3)According to this specific situation in our restaurant dataset, 
      simply check the different in today's grade and the first grade is practical and efficient.
    """
    return increase

#This function is to get grade list for each restaurant
def test_restaurant_grades(df, camis_id):
    """
    camis_id: restaurant ID
    """
    grade_list = list(df['GRADE'][camis_id]) #get grade list for each restaurant
    return test_grades(grade_list)

#This function is to create a reference for an existing dataframe
def df_reference(df):
    """
    Return:
    df_refer: A dataframe only contains information about ID and borough without duplicates.
    """
    df_refer = df.drop(['GRADE','GRADE DATE'], axis=1)
    df_refer['CAMIS'] = df_refer.index
    df_refer = df_refer.drop_duplicates()
    return df_refer


