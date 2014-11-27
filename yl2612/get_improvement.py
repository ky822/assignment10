import pandas as pd
import numpy as np


def test_grades(grade_list):
    '''
    Take a list of grades sorted in date order,
    returns 1 if the median grade after the first graded date, i.e., median grade excepting the first grade, is bigger than the first grade,
    returns -1 if it is smaller than the first grade,
    and returns 0 if they are the same.
    '''
    grade_num = {'A':3, 'B':2, 'C':1} # create a dictionary that map A,B,C to 3,2,1, respectively
    grade_list_num = [grade_num[grade] for grade in grade_list] #create a new list using 1,2,3 to represent A,B,C.
    
    if len(grade_list)==1: #returns 0 if there is only one grade in the list
        return 0
    if grade_list_num[0] > np.median(grade_list_num[1:]):
        return -1
    elif grade_list_num[0] < np.median(grade_list_num[1:]):
        return 1
    else:
        return 0


def test_restaurant_grades(df,camis_id):
    '''
    Examine if the grade for a restaurant is improving.
    Return 1 if it is improving, -1 if it is declining, 0 if it stays the same.
    '''  
    collect_grades = df.GRADE[df.index==camis_id] #select grades having the same camis_id
    assess_quality = test_grades(collect_grades)
    return assess_quality


def get_sum(df):
    '''
    This function calculates the sum of improvement.
    '''
    collect_unique_ids = df.index.unique() #collect the ids
    compute_sum = 0
    for unique_id in collect_unique_ids:
        compute_sum += test_restaurant_grades(df, unique_id)
    return compute_sum


