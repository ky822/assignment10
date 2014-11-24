# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 00:44:10 2014

@author: LaiQX
"""

import pandas as pd
import matplotlib.pyplot as plt


def data_clean(data_frame):
    """
    clean the input data frame. drop some used raw:
    drop all the rows that contains NaN
    drop rows whose GRADE in ['Not Yet Grade','P', 'Z']
    drop rows whose BORO is 'Missing'
    Return the cleaned data frame
    """
    cleaned_df = data_frame.dropna(how='any')
    cleaned_df = cleaned_df.loc[~(cleaned_df.GRADE == 'Not Yet Graded')]
    cleaned_df = cleaned_df.loc[~(cleaned_df.GRADE == 'P')]
    cleaned_df = cleaned_df.loc[~(cleaned_df.GRADE == 'Z')]
    cleaned_df = cleaned_df.loc[~(cleaned_df.BORO == 'Missing')]
    return cleaned_df


def test_grades(grade_list):
    '''
    input a grade list, justify whether it is improving
    if it is improving return 1
    if it stay the same return 0
    if it is declining return -1
    '''
    n = len(grade_list)
    alphabet = dict(zip(['A', 'B', 'C'], [3,  2, 1]))
    count = 0
    for i in range(n-1):
        if alphabet[grade_list[i]] < alphabet[grade_list[i+1]]:
            count -= 1                           
        if alphabet[grade_list[i]] > alphabet[grade_list[i+1]]:
            count += 1
    if count == 0:
        return 0
    else:
        return int(count/abs(count))        # return 1 or -1


def test_restaurant_grades(df, camis_id):
    '''
    input a data frame and a restaurant's camis_is., this function will
    return wheher this restaurant is improving based on the test_grades
    function.
    '''
    data = df[['CAMIS', 'GRADE']]   #we only need CAMIS GRADE in this function
    grade_list = list(data.loc[data.CAMIS == camis_id]['GRADE'])  # the grades are already sorted by date
    grade_is_improved = test_grades(grade_list)
    return grade_is_improved
 

def grade_test_count_all(df):
    '''
    compute the sum of test grade over all restaurant in the dataset
    '''
    data_used = df[['CAMIS','GRADE','BORO']]
    grouped_grade = data_used.groupby('CAMIS')
    improve = 0                # summation of the test_grade
    for name,groups in grouped_grade:
        temp = test_grades(list(groups['GRADE']))
        improve += temp
    f = open('testScore.txt','a+')
    f.write('Over all restaurant in NYC: %s \n \n \n' % (improve))
    f.close


def grade_test_count(df):
    '''
    compute the sum of test grade over all restaurant for each boroughs
    '''
    data_used = df[['CAMIS', 'GRADE', 'BORO']]
    grouped_grade = data_used.groupby('CAMIS')
    improve_test = {}        
    for name, groups in grouped_grade:
        temp = test_grades(list(groups['GRADE']))     #count improve score for each restaurant
        improve_test[name] = (temp, list(groups['BORO'])[0])  # also record which borough the restaurant in
    improve_test = pd.DataFrame(improve_test)        # turn this dict to dataframe
    improve_test = improve_test.T
    improve_test.columns = ['INPROVE', 'BORO']       #group by boro
    result = improve_test.groupby('BORO').INPROVE.sum()
    f = open('testScore.txt', 'a+')
    f.write(str(result))                             # save in the file
    f.close()


def date_format(date_str_list):
    '''
    input is a list of date str like this :mm/dd/yyyy,
    this function will turn it to a list of numpy-datetime64 date
    return the list
    '''
    
    year_list = [int(x[-4:]) for x in date_str_list]     # year in the list 
    month_list = [int(x[:2]) for x in date_str_list]     # month in teh list
    day_list = [int(x[3:5]) for x in date_str_list]      # day in the list 
    date = [pd.datetime(year_list[i], month_list[i], day_list[i]) for i in xrange(len(year_list))]
    return date


def grade_plot(df, title):
    """
    input a data frame and a title. 
    this function will first compute the number of restaurant for each grade and each date
    then plot the number versus date and save the plot with the title
    """
    data = df[['CAMIS', 'GRADE', 'GRADE DATE']]
    date_str = list(data.loc[:, 'GRADE DATE'])
    date_list = date_format(date_str)
    data.loc[:,'DATE'] = date_list                              #transform the date type
    date_group = data.groupby('DATE')
    date_df = pd.DataFrame(columns=['A', 'B', 'C'], index=date_group.groups.keys()) 
    
    rest_series = pd.Series(index=data.groupby('CAMIS').groups.keys())
    for date, grade_groups in date_group:
        rest_series.ix[list(grade_groups['CAMIS'])] = list(grade_groups['GRADE'])
        a = sum(rest_series == 'A')
        date_df.ix[date, 'A'] = a
        date_df.ix[date, 'B'] = sum(rest_series == 'B')
        date_df.ix[date, 'C'] = sum(rest_series == 'C')
        #print ">",
    plt.figure(figsize=(8, 6))
    date_df.plot()
    plt.title('grade_improvement_%s'%(title))
    plt.xlabel('Date')
    plt.ylabel('grade score')
    plt.savefig('grade_improvement_%s.pdf'%(title))
